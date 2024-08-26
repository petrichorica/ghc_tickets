import requests
import logging
from dotenv import load_dotenv
import os

load_dotenv()
WEBHOOK = os.getenv("WEBHOOK")

def send_discord_notification(message):
    webhook_url = WEBHOOK
    data = {"content": message}
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            logging.info("Successfully sent discord notification")
        else:
            logging.error(f"Failed to send discord notification, status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Error during send_discord_notification: {str(e)}")

if __name__ == "__main__":
    send_discord_notification("Test notification from discord_notify.py")
