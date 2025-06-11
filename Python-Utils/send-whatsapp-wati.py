"""
WATI WhatsApp API Integration Script
===================================

This script provides functions to send WhatsApp messages using WATI API:
1. Send approved template messages (with or without image headers)
2. Send session (manual) messages

Author: Assistant
Version: 1.5
Requirements: python-dotenv, requests
"""

import requests
import os
import logging
from typing import Dict, List, Optional
from dotenv import load_dotenv
from urllib.parse import urlparse, quote
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import random
import time

# Load environment variables from unified config.env file
load_dotenv('config.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wati_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WATIWhatsAppAPI:
    """WATI WhatsApp API Client Class"""

    def __init__(self, api_key: str = None, base_url: str = None, instance_id: str = None):
        self.api_key = api_key or os.getenv('WATI_API_KEY')
        self.base_url = base_url or os.getenv('WATI_BASE_URL')
        self.instance_id = instance_id or os.getenv('WATI_INSTANCE_ID')

        if not self.api_key:
            raise ValueError("WATI API key not found. Please set WATI_API_KEY in config.env")
        if not self.base_url:
            raise ValueError("WATI base URL not found. Please set WATI_BASE_URL in config.env")
        if not self.instance_id:
            raise ValueError("WATI instance ID not found. Please set WATI_INSTANCE_ID in config.env")

        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount('https://', adapter)
        self.session.mount('http://', adapter)

        logger.info("WATI API client initialized successfully")

    def _validate_phone_number(self, number: str) -> str:
        number = number.strip()
        return number.lstrip('+')

    def _make_request(self, endpoint: str, payload: Dict = None) -> Dict:
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        try:
            logger.info(f"Making request to: {url}")
            if payload:
                logger.info(f"Payload: {payload}")

            response = self.session.post(url, json=payload if payload else None, headers=self.headers, timeout=30)
            logger.info(f"Response status: {response.status_code}")

            try:
                response_data = response.json()
            except ValueError:
                response_data = response.text

            if response.status_code == 200:
                logger.info("Request successful")
                print(f"   \U0001f4cb API Response: {response_data}")
                return {'success': True, 'data': response_data, 'status_code': 200}
            else:
                error_msg = f"API Error {response.status_code}: {response_data}"
                logger.error(error_msg)
                return {'success': False, 'error': error_msg, 'status_code': response.status_code}
        except Exception as e:
            return {'success': False, 'error': f"Unexpected error: {str(e)}"}

    def send_template_message(self, phone_number: str, template_name: str, parameters: List[Dict[str, str]] = None, headerValues: Optional[List[Dict]] = None, broadcast_name: str = "wati_script_test") -> Dict:
        try:
            formatted_phone = self._validate_phone_number(phone_number)

            payload = {
                "template_name": template_name,
                "broadcast_name": broadcast_name
            }
            if parameters:
                payload["parameters"] = parameters
            if headerValues:
                payload["headerValues"] = headerValues

            endpoint = f"sendTemplateMessage?whatsappNumber={formatted_phone}"
            result = self._make_request(endpoint, payload)
            if result['success']:
                logger.info(f"Template message '{template_name}' sent to {formatted_phone}")
            return result
        except Exception as e:
            return {'success': False, 'error': f"Template message error: {str(e)}"}

    def send_session_message(self, phone_number: str, message_text: str) -> Dict:
        """
        Send a manual session message (non-template) to an active session
        """
        try:
            formatted_phone = self._validate_phone_number(phone_number)
            encoded_message = quote(message_text)
            endpoint = f"sendSessionMessage/{formatted_phone}?messageText={encoded_message}"
            return self._make_request(endpoint)
        except Exception as e:
            return {'success': False, 'error': str(e)}

def load_wati_config_info():
    print("=== WATI WhatsApp Configuration ===")
    print(f"API Key: {'*' * 8 + os.getenv('WATI_API_KEY', 'Not set')[-4:] if os.getenv('WATI_API_KEY') else 'Not set'}")
    print(f"Base URL: {os.getenv('WATI_BASE_URL', 'Not set')}")
    print(f"Instance ID: {os.getenv('WATI_INSTANCE_ID', 'Not set')}")
    print(f"Default Phone: {os.getenv('DEFAULT_PHONE_NUMBER', 'Not set')}")
    print(f"Sender Name: {os.getenv('DEFAULT_SENDER_NAME', 'Not set')}")
    print("=" * 35)

if __name__ == "__main__":
    load_wati_config_info()
    default_phone = os.getenv('DEFAULT_PHONE_NUMBER', '+918128557443')

    try:
        wati_client = WATIWhatsAppAPI()

        # ✅ Option 1: Send template message with image header
        print("\n📋 Sending approved template message with header...")
        template_with_header = wati_client.send_template_message(
            phone_number=default_phone,
            template_name="test_image_message",
            parameters=[],
            headerValues=[
                {
                    "type": "IMAGE",
                    "media": {
                        "url": "https://via.placeholder.com/400x300.png?text=WATI+Header"
                    }
                }
            ]
        )
        print(template_with_header)
        time.sleep(20)  # Pause for 2 seconds

        # ✅ Option 2: Send template message without image header
        print("\n📋 Sending approved template message without header...")
        otp = str(random.randint(100000, 999999))
        otp_template_result = wati_client.send_template_message(
            phone_number=default_phone,
            template_name="test_text_otp",
            parameters=[
                {"name": "1", "value": otp}
            ],
            broadcast_name="wati_script_test"
        )
        print(otp_template_result)
        time.sleep(20)  # Pause for 2 seconds

        # ✅ Option 3: Send direct session message (non-template)
        print("\n✉️ Sending session message (non-template)...")
        session_result = wati_client.send_session_message(
            phone_number=default_phone,
            message_text="Hello! This is a direct message using the WATI session API."
        )
        print(session_result)

    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
