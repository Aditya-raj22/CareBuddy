# backend/app/api/routes.py
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends, Request, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.config import settings
from app.db.models import Doctor, CareBuddy, Conversation, UserSession, Document
from app.db.database import get_db
from app.services.whatsapp import whatsapp_client
from app.services.carebuddy_rag import rag_system
from datetime import datetime, timezone, timedelta
import logging
import json

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["api"])

# Mock doctor ID for development
MOCK_DOCTOR_ID = 1
WHATSAPP_NUMBER = "YOUR_WHATSAPP_NUMBER"  # Replace with your number

@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
    hub_challenge: str = Query(..., alias="hub.challenge"),
):
    """Handle webhook verification from Meta"""
    logger.debug(f"Webhook verification request: mode={hub_mode}, token={hub_verify_token}, challenge={hub_challenge}")
    
    if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_WEBHOOK_TOKEN:
        logger.info("Webhook verified successfully")
        return int(hub_challenge)
    
    raise HTTPException(status_code=403, detail="Verification failed")

@router.get("/buddies")
async def get_buddies(db: Session = Depends(get_db)):
    """Get all buddies"""
    logger.debug("Fetching buddies")
    try:
        buddies = db.query(CareBuddy).filter(
            CareBuddy.doctor_id == MOCK_DOCTOR_ID
        ).all()
        return [{"id": buddy.bid, "name": buddy.name} for buddy in buddies]
    except Exception as e:
        logger.error(f"Error fetching buddies: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/buddy/{buddy_id}")
async def get_buddy_details(buddy_id: str, db: Session = Depends(get_db)):
    """Get details for a specific buddy"""
    logger.debug(f"Fetching details for buddy: {buddy_id}")
    try:
        buddy = db.query(CareBuddy).filter(
            CareBuddy.bid == buddy_id,
            CareBuddy.doctor_id == MOCK_DOCTOR_ID
        ).first()
        
        if not buddy:
            raise HTTPException(status_code=404, detail="Buddy not found")

        # Get statistics
        conversations = db.query(Conversation).filter(
            Conversation.buddy_id == buddy.id
        ).all()

        active_patients = db.query(UserSession).filter(
            UserSession.buddy_id == buddy.id,
            UserSession.last_active >= datetime.now(timezone.utc) - timedelta(days=30)
        ).count()

        helpful_responses = sum(1 for c in conversations if c.helpful is True)
        total_rated = sum(1 for c in conversations if c.helpful is not None)

        # Get documents
        documents = db.query(Document).filter(
            Document.buddy_id == buddy.id
        ).all()

        return {
            "id": buddy.bid,
            "name": buddy.name,
            "creation_date": buddy.creation_date.isoformat(),
            "whatsapp_number": WHATSAPP_NUMBER,
            "stats": {
                "total_questions": len(conversations),
                "active_patients": active_patients,
                "response_rate": round((helpful_responses / total_rated * 100) if total_rated > 0 else 0, 1),
                "average_rating": round((helpful_responses / total_rated * 5) if total_rated > 0 else 0, 1)
            },
            "documents": [
                {
                    "id": doc.id,
                    "name": doc.filename,
                    "uploaded_at": doc.upload_date.isoformat()
                }
                for doc in documents
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching buddy details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/doctor/impact")
async def get_doctor_impact(timespan: str = "month", db: Session = Depends(get_db)):
    """Get doctor's impact metrics"""
    logger.debug(f"Fetching impact metrics for timespan: {timespan}")
    try:
        total_buddies = db.query(CareBuddy).filter(
            CareBuddy.doctor_id == MOCK_DOCTOR_ID
        ).count()

        now = datetime.now(timezone.utc)
        if timespan == "today":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif timespan == "week":
            start_date = now - timedelta(days=7)
        else:  # month
            start_date = now - timedelta(days=30)

        conversations = db.query(Conversation).join(
            CareBuddy
        ).filter(
            CareBuddy.doctor_id == MOCK_DOCTOR_ID,
            Conversation.timestamp >= start_date
        ).all()

        total_conversations = len(conversations)
        helpful_conversations = sum(1 for c in conversations if c.helpful is True)

        return {
            "total_buddies": total_buddies,
            "total_conversations": total_conversations,
            "total_patients": db.query(UserSession.id).distinct().count(),
            "average_rating": (helpful_conversations / total_conversations * 5) if total_conversations > 0 else 0
        }
    except Exception as e:
        logger.error(f"Error fetching impact metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/buddies/create")
async def create_buddy(name: str = Form(...), db: Session = Depends(get_db)):
    """Create a new buddy"""
    logger.debug(f"Creating new buddy with name: {name}")
    try:
        timestamp = str(int(datetime.now().timestamp()))[-2:]
        bid = f"BD{timestamp}"
        
        buddy = CareBuddy(
            bid=bid,
            name=name,
            doctor_id=MOCK_DOCTOR_ID,
            creation_date=datetime.now(timezone.utc)
        )
        db.add(buddy)
        db.commit()
        
        logger.debug(f"Successfully created buddy with ID: {bid}")
        return {
            "buddy_id": buddy.bid,
            "name": buddy.name
        }
    except Exception as e:
        logger.error(f"Error creating buddy: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/buddy/{buddy_id}/documents")
async def upload_documents(
    buddy_id: str,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """Upload documents for a buddy"""
    logger.debug(f"Uploading documents for buddy: {buddy_id}")
    try:
        buddy = db.query(CareBuddy).filter(
            CareBuddy.bid == buddy_id,
            CareBuddy.doctor_id == MOCK_DOCTOR_ID
        ).first()
        
        if not buddy:
            raise HTTPException(status_code=404, detail="Buddy not found")
        
        uploaded_docs = []
        for file in files:
            content = await file.read()
            text_content = content.decode('utf-8', errors='ignore')
            
            # Log document content for debugging
            logger.debug(f"Document content preview: {text_content[:500]}...")
            
            # Process with RAG
            rag_success = rag_system.process_doctor_document(
                doc_text=text_content,
                doc_id=f"{buddy_id}-{len(uploaded_docs)}"
            )
            
            if not rag_success:
                logger.error("Failed to process document with RAG system")
                raise HTTPException(status_code=500, detail="Failed to process document")
            
            # Save to database
            doc = Document(
                buddy_id=buddy.id,
                filename=file.filename,
                content=text_content,
                upload_date=datetime.now(timezone.utc)
            )
            db.add(doc)
            uploaded_docs.append({
                "id": doc.id,
                "name": doc.filename
            })
        
        db.commit()
        logger.debug(f"Successfully uploaded {len(uploaded_docs)} documents")
        return {
            "status": "success",
            "documents": uploaded_docs
        }
    except Exception as e:
        logger.error(f"Error uploading documents: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def webhook_handler(request: Request, db: Session = Depends(get_db)):
    try:
        body = await request.json()
        logger.debug(f"Received webhook: {json.dumps(body, indent=2)}")

        if body.get("object") != "whatsapp_business_account":
            return {"status": "not a whatsapp message"}

        for entry in body.get("entry", []):
            for change in entry.get("changes", []):
                messages = change.get("value", {}).get("messages", [])
                if not messages:
                    logger.debug("No messages in webhook")
                    return {"status": "no messages"}

                for message in messages:
                    try:
                        if "text" not in message:
                            logger.debug("Message contains no text")
                            continue

                        from_number = message["from"]
                        message_body = message["text"]["body"]

                        logger.debug(f"Processing message from {from_number}: {message_body}")

                        # Handle CONNECT command
                        if message_body.upper().startswith("CONNECT"):
                            # ... existing CONNECT handling code ...
                            continue

                        else:
                            # Handle regular message
                            session = db.query(UserSession).filter_by(
                                phone_number=from_number
                            ).first()

                            if not session or not session.buddy_id:
                                await whatsapp_client.send_message(
                                    to=from_number,
                                    message="Please connect to a buddy first using 'CONNECT' followed by the buddy ID."
                                )
                                continue

                            # ADD THE NEW DEBUG LOGGING HERE
                            logger.debug(f"About to query RAG with message: {message_body}")
                            logger.debug(f"Current buddy_id: {session.buddy_id}")

                            # Get documents for this buddy
                            documents = db.query(Document).filter(
                                Document.buddy_id == session.buddy_id
                            ).all()
                            logger.debug(f"Found {len(documents)} documents for buddy")

                            # Log document content
                            for doc in documents:
                                logger.debug(f"Document {doc.id} content preview: {doc.content[:200]}")

                            # Create conversation record
                            conversation = Conversation(
                                buddy_id=session.buddy_id,
                                user_session_id=session.id,
                                query=message_body
                            )
                            db.add(conversation)
                            db.commit()

                            # Get response from RAG
                            response = rag_system.get_response(
                                query=message_body,
                                chat_history=[]
                            )
                            logger.debug(f"RAG response: {response}")

                            # Save response
                            conversation.response = response
                            db.commit()

                            # Send response
                            await whatsapp_client.send_message(
                                to=from_number,
                                message=response
                            )

                    except Exception as e:
                        logger.error(f"Error processing message: {str(e)}", exc_info=True)
                        try:
                            await whatsapp_client.send_message(
                                to=from_number,
                                message="Sorry, I encountered an error. Please try again."
                            )
                        except:
                            logger.error("Failed to send error message to user", exc_info=True)

        return {"status": "success"}

    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))