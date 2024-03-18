import requests
import json

def get_current_price(symbol):
    """
    Get the current price of a given symbol on Bybit.

    :param symbol: The trading pair symbol, e.g., 'BTCUSD'.
    :return: The current price as a float or None if an error occurs.
    """
    url = f"https://api.bybit.com/v2/public/tickers?symbol={symbol}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()
        
        if data['ret_code'] == 0:  # Check if the request was successful
            return float(data['result'][0]['last_price'])
        else:
            print(f"Error fetching price data: {data['ret_msg']}")
            return None
    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None