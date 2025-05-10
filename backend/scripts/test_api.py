# backend/scripts/test_api.py
import os
import sys
from pathlib import Path
import requests
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "http://localhost:8001/api"

def test_endpoints():
    """Test all API endpoints"""
    endpoints = [
        ("GET", "/buddies"),
        ("GET", "/doctor/impact"),
        ("POST", "/buddies/create", {"name": "Test Buddy"}),
    ]

    for method, endpoint, *args in endpoints:
        url = f"{API_URL}{endpoint}"
        try:
            if method == "GET":
                response = requests.get(url)
            elif method == "POST":
                data = args[0] if args else {}
                response = requests.post(url, json=data)
            
            logger.info(f"{method} {endpoint}: {response.status_code}")
            logger.info(f"Response: {response.json() if response.ok else response.text}")
        except Exception as e:
            logger.error(f"Error testing {method} {endpoint}: {e}")

if __name__ == "__main__":
    test_endpoints()