from pybit.unified_trading import HTTP
import os
from dotenv import load_dotenv

load_dotenv()  # This loads the environment variables from .env

# Now you can access your API keys as environment variables
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# Initialize the session with your credentials
session = HTTP(
    testnet=True,  # Change to False if you're using the mainnet
    api_key=api_key,
    api_secret=api_secret
)

try:
    # Place a limit order
    response = session.place_order(
        category="linear",  # Use "inverse" for inverse contracts
        symbol="BTCUSDT",  # The trading pair
        side="Buy",  # "Sell" for selling
        orderType="Limit",  # "Market" for market orders
        qty="0.01",  # Quantity of the order
        price="25000",  # Price to buy/sell at
        timeInForce="GTC"  # Good Till Cancelled
    )
    print(response)
except Exception as e:
    error_message = str(e)
    if "InsufficientAB" in error_message:
        print("Insufficient available balance to place the order.")
    else:
        print(f"An error occurred: {error_message}")