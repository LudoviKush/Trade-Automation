import time
from pybit.unified_trading import HTTP
from telegram_service import fetch_and_process_messages
import logging
from dotenv import load_dotenv
import os

# Configure logging
def configure_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables and initialize logging in your main.py as well
load_dotenv()


api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# Initialize the session with your credentials
session = HTTP(
    testnet=True,  # Change to False if you're using the mainnet
    api_key=api_key,
    api_secret=api_secret
)

def main():
    while True:
        fetch_and_process_messages(session)
        time.sleep(10)  # Add a delay before the next fetch

if __name__ == "__main__":
    main()