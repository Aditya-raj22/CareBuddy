# backend/app/services/carebuddy_rag.py
from typing import Optional, Dict, List
import os
import logging
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain.chains import ConversationalRetrievalChain
from pinecone import Pinecone, ServerlessSpec

logger = logging.getLogger(__name__)

class CareBuddyRAG:
    def __init__(self):
        load_dotenv()
        logger.info("Initializing CareBuddyRAG")
        
        # Initialize OpenAI
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(
            temperature=0.1,  # Low temperature for medical advice
            model_name="gpt-4"  # Using GPT-4 for higher accuracy
        )
        
        # Initialize Pinecone
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = "carebuddy-docs"
        
        # Create index if it doesn't exist
        existing_indexes = self.pc.list_indexes()
        if not any(index.name == self.index_name for index in existing_indexes):
            logger.info(f"Creating new Pinecone index: {self.index_name}")
            self.pc.create_index(
                name=self.index_name,
                dimension=1536,  # OpenAI embedding dimension
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
        
        # Get the index
        self.index = self.pc.Index(self.index_name)
        
        # Initialize the vectorstore
        self.vectorstore = PineconeVectorStore(
            embedding=self.embeddings,
            index=self.index,
            text_key="text",
            namespace="medical"
        )
        
        # Initialize the retrieval chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 3}  # Retrieve top 3 most relevant chunks
            )
        )
        
        # Medical-specific text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n", "\n", ". ", "? ", "! ", ";"]
        )
        
        logger.info("CareBuddyRAG initialization complete")

    def process_doctor_document(self, doc_text: str, doc_id: str) -> bool:
        """Process and store a doctor's document"""
        try:
            logger.debug(f"Processing document {doc_id}")
            logger.debug(f"Document content preview: {doc_text[:200]}...")
            
            # Split the document into chunks
            chunks = self.text_splitter.split_text(doc_text)
            logger.debug(f"Split into {len(chunks)} chunks")
            logger.debug(f"First chunk sample: {chunks[0][:100]}...")
            
            # Add metadata to each chunk
            texts_with_metadata = [
                {
                    "text": chunk,
                    "doc_id": doc_id,
                    "chunk_index": i,
                    "source": "doctor_document"  # Add source
                }
                for i, chunk in enumerate(chunks)
            ]
            
            # Get embeddings for debugging
            first_embedding = self.embeddings.embed_query(chunks[0])
            logger.debug(f"First embedding shape: {len(first_embedding)}")
            
            # Store in vector database with explicit namespace
            try:
                self.vectorstore.add_texts(
                    texts=[t["text"] for t in texts_with_metadata],
                    metadatas=texts_with_metadata,
                    namespace="medical"
                )
                logger.info(f"Successfully processed and stored document {doc_id}")
                
                # Verify storage
                results = self.vectorstore.similarity_search(
                    chunks[0][:100],
                    k=1,
                    namespace="medical"
                )
                logger.debug(f"Verification search results: {results}")
                
                return True
            except Exception as e:
                logger.error(f"Error storing in vectorstore: {str(e)}", exc_info=True)
                return False
                
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}", exc_info=True)
            return False

    def get_response(self, query: str, chat_history: List[Dict] = None) -> str:
        """Get a response for a user query"""
        try:
            logger.debug(f"Processing query: {query}")
            
            # First try a direct similarity search for debugging
            similar_docs = self.vectorstore.similarity_search(
                query,
                k=3,
                namespace="medical"
            )
            logger.debug(f"Similar docs found: {len(similar_docs)}")
            for i, doc in enumerate(similar_docs):
                logger.debug(f"Doc {i} content: {doc.page_content[:200]}...")
                logger.debug(f"Doc {i} metadata: {doc.metadata}")
            
            # Format chat history if provided
            formatted_history = []
            if chat_history:
                for msg in chat_history:
                    formatted_history.append((msg["user"], msg["assistant"]))
                    
            # Enhanced safety prompt
            safety_prompt = """
            You are a medical information assistant with access to specific doctor-provided documents.
            Analyze the retrieved documents carefully and:
            1. IF you find relevant information that DIRECTLY answers the query, provide it and cite the source
            2. IF you find related but indirect information, still provide a "no direct information" response
            3. IF you find NO relevant information, respond with the standard message
            
            Please scrutinize the following query against your available documents: {query}
            """
            
            # Get response from chain with enhanced logging
            try:
                response = self.chain(
                    {"question": safety_prompt.format(query=query),
                    "chat_history": formatted_history}
                )
                logger.debug(f"Generated response: {response['answer']}")
                return response['answer']
                
            except Exception as e:
                logger.error(f"Error in chain response: {str(e)}", exc_info=True)
                return "I encountered an error processing your query. Please try again or contact your healthcare provider."
                
        except Exception as e:
            logger.error(f"Error getting response: {str(e)}", exc_info=True)
            return f"I apologize, but I encountered an error. Please try again or contact your healthcare provider."

    
    
rag_system = CareBuddyRAG()