import yfinance as yf
import os
from datetime import datetime, timedelta

def fetch_bitcoin_data():
    # Calculate start date (6 months ago) and end date (today)
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=6*30)).strftime('%Y-%m-%d')  # Approx. 6 months

    # Fetch Bitcoin price data
    ticker = "BTC-USD"
    print(f"Fetching Bitcoin data from {start_date} to {end_date}...")
    data = yf.download(ticker, start=start_date, end=end_date, interval="1d")

    # Save to CSV
    os.makedirs("Data", exist_ok=True)  # Ensure the directory exists
    csv_file = "Data/bitcoin_prices.csv"
    data.to_csv(csv_file, index=True)
    print(f"Bitcoin data saved to {csv_file}")

if __name__ == "__main__":
    fetch_bitcoin_data()
