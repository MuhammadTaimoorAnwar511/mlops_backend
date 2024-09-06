import yfinance as yf  # For fetching Bitcoin price data
import pandas as pd  # For data manipulation
from sklearn.model_selection import train_test_split  # For splitting the dataset
from sklearn.linear_model import LinearRegression  # For model training
import joblib  # For saving the trained model

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

try:
    model = LinearRegression()
    model.fit(X_train, y_train)
    joblib.dump(model, "bitcoin_model.pkl", compress=3)
except Exception as e:
    print(f"Error during training or saving model: {e}")
