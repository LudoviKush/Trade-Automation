import requests
import logging
from spacy_extraction import trade_details_extraction
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Constants
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_CHANNELS = ['-4187890246']
processed_update_ids = set()
last_update_ids = {channel: 0 for channel in TELEGRAM_CHANNELS}

def remove_leading_slash(text):
    return text[1:] if text and text.startswith("/") else text

def fetch_and_process_messages(session):
    for channel in TELEGRAM_CHANNELS:
        print(f"Fetching messages from Telegram channel {channel}...")
        response = requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?offset={last_update_ids[channel] + 1}&timeout=60"
        )
        updates = response.json().get("result", [])
        print(
            f"Received {len(updates)} updates from Telegram for channel {channel}."
        )

        max_update_id = last_update_ids[channel]
        for update in updates:
            if update["update_id"] in processed_update_ids:
                continue

            message = update.get("channel_post") or update.get("message")

            if not message:
                continue

            text = remove_leading_slash(message.get("text"))

            # Inside fetch_and_process_messages function
            if text:
                print(f"Text message from channel {channel}: {text}")
                extracted_info = trade_details_extraction(text)
                print(f"Extracted information: {extracted_info}")
                
                try:
                    # Place a limit order using the extracted values
                    response = session.place_order(
                        category="linear",  # Use "inverse" for inverse contracts if needed
                        symbol=extracted_info['couple'],  # Correctly reference the extracted symbol
                        side=extracted_info['side'],  # Dynamically set based on management
                        orderType="Limit",  # "Market" for market orders
                        qty="1",  # Quantity of the order, adjust as needed
                        price=extracted_info['target_5'],  # Using target 5 as the price for the limit order
                        timeInForce="GTC"  # Good Till Cancelled
                    )
                    logging.info(response)
                except Exception as e:
                    logging.error(f"An error occurred while placing the order: {e}")

            max_update_id = max(max_update_id, update["update_id"])
            processed_update_ids.add(update["update_id"])

        last_update_ids[channel] = max_update_id