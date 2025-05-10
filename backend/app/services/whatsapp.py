# backend/app/services/whatsapp.py
import httpx
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class WhatsAppClient:
    def __init__(self):
        self.access_token = settings.WHATSAPP_ACCESS_TOKEN
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.api_version = "v17.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}"

    async def send_message(self, to: str, message: str):
        """Send a message via WhatsApp"""
        try:
            url = f"{self.base_url}/messages"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to,
                "type": "text",
                "text": {"body": message}
            }

            logger.debug(f"Sending WhatsApp message to {to}: {message}")
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                logger.debug(f"WhatsApp message sent successfully: {response.json()}")
                return response.json()
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {str(e)}")
            raise

whatsapp_client = WhatsAppClient()