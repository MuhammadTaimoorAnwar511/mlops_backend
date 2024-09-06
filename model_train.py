import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

# Fetch Bitcoin price data
ticker = "BTC-USD"
data = yf.download(ticker, start="2023-05-01", end="2023-07-01", interval="1d")

# Use only the 'Close' price for simplicity
data = data[['Close']].copy()  # Make a copy to avoid SettingWithCopyWarning

# Prepare data
data['Target'] = data['Close'].shift(-1)  # Predicting the next day's close price
data = data.dropna()  # Drop missing values

X = data[['Close']]
y = data['Target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Save model with compression
joblib.dump(model, "bitcoin_model.pkl", compress=3)
