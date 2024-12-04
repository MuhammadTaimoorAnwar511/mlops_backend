import requests
from requests.exceptions import ConnectionError
import pandas as pd
from datetime import datetime, timedelta
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
def fetch_binance_futures_data(symbol, interval, start_time, end_time):
    base_url = "https://fapi.binance.com"
    endpoint = "/fapi/v1/klines"
    
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": int(start_time.timestamp() * 1000),
        "endTime": int(end_time.timestamp() * 1000),
        "limit": 1000
    }
    
    retries = 3  # Reduced retries to 3
    for attempt in range(retries):
        try:
            response = requests.get(base_url + endpoint, params=params)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
        except ConnectionError as e:
            print(f"Connection error: {e}. Retrying in {2 ** attempt} seconds...")
            time.sleep(2 ** attempt)  # Exponential backoff
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {symbol} at {interval}: {e}")
            return None
    print(f"Failed to fetch data for {symbol} after {retries} attempts.")
    return None

def save_data_to_csv(data, symbol, interval, start_date, end_date):
    # Ensure the "Data" folder exists
    data_folder = "Data"
   
    df = pd.DataFrame(data, columns=[
        "Open Time", "Open", "High", "Low", "Close", "Volume",
        "Close Time", "Quote Asset Volume", "Number of Trades",
        "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume", "Ignore"
    ])
    
    # Select only needed columns
    df = df[["Open Time", "Open", "High", "Low", "Close", "Volume", "Quote Asset Volume"]]
    df["Open Time"] = pd.to_datetime(df["Open Time"], unit='ms')
    df.sort_values(by="Open Time", inplace=True)
        # Rename "Open Time" to "Date"
    df.rename(columns={"Open Time": "Date"}, inplace=True)
    file_name = "Data/bitcoin_prices.csv"
    
    # Save to CSV
    df.to_csv(file_name, index=False)
    print(f"Data saved to {file_name}")

def fetch_and_save(symbol, interval, start_date, end_date):
    current_date = start_date
    all_data = []

    # Fetch data 15 days at a time
    while current_date < end_date:
        next_date = min(current_date + timedelta(days=15), end_date)
        
        print(f"Fetching {interval} data for {symbol} from {current_date.strftime('%Y-%m-%d')} to {next_date.strftime('%Y-%m-%d')}")
        
        data = fetch_binance_futures_data(symbol, interval, current_date, next_date)
        if data:
            all_data.extend(data)
        
        current_date = next_date
        time.sleep(0.25)  # Small delay after each request to avoid API rate limits
    
    # Save the data if fetched
    if all_data:
        save_data_to_csv(all_data, symbol, interval, start_date, end_date)


def main():
    symbols = ["BTCUSDT"]
    intervals = ["1d"]  
    
    # Dynamically calculate the start_date and end_date
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1 * 30)  # Approximation of 6 months
    
    # Use ThreadPoolExecutor for parallel data fetching
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        
        for symbol in symbols:
            for interval in intervals:
                futures.append(executor.submit(fetch_and_save, symbol, interval, start_date, end_date))
        
        # Wait for all tasks to complete
        for future in as_completed(futures):
            future.result()  

if __name__ == "__main__":
    main()
