import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import os
import json

def prepare_data(sequence, look_back=1):
    X, y = [], []
    for i in range(len(sequence) - look_back):
        X.append(sequence[i:i + look_back, 0])
        y.append(sequence[i + look_back, 0])
    return np.array(X), np.array(y)

def train_lstm_model():
    # Variables for training
    look_back = 7  # Number of previous time steps to use as input
    epochs = 50    # Number of epochs
    batch_size = 32  # Batch size

    # Load data
    csv_file = "Data/bitcoin_prices_cleaned.csv"
    data = pd.read_csv(csv_file)

    # Use only the 'Close' price
    data = data[['Close']].copy()

    # Scaling the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    # Save the scaler for inverse transformation
    os.makedirs("Model", exist_ok=True)
    scaler_file = "Model/bitcoin_scaler.pkl"
    joblib.dump(scaler, scaler_file)

    # Prepare data for LSTM
    X, y = prepare_data(scaled_data, look_back)

    # Reshape input for LSTM (samples, time steps, features)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Build the LSTM model
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(look_back, 1)),
        LSTM(50),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model and store training history
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test), verbose=1)

    # Save the trained model
    lstm_model_file = "Model/bitcoin_lstm_model.h5"
    model.save(lstm_model_file)
    print(f"LSTM model saved to {lstm_model_file}")

    # Model evaluation
    predictions = model.predict(X_test)
    predictions_inverse = scaler.inverse_transform(predictions)  # Inverse scale predictions
    y_test_inverse = scaler.inverse_transform(y_test.reshape(-1, 1))  # Inverse scale actual values

    # Print actual vs. predicted values
    print("\nActual vs Predicted (Inverse Scaled):")
    for actual, predicted in zip(y_test_inverse.flatten(), predictions_inverse.flatten()):
        print(f"Actual: {actual:.2f}, Predicted: {predicted:.2f}")

    # Calculate metrics
    mse = mean_squared_error(y_test_inverse, predictions_inverse)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test_inverse, predictions_inverse)
    mape = np.mean(np.abs((y_test_inverse - predictions_inverse) / y_test_inverse)) * 100
    r2 = r2_score(y_test_inverse, predictions_inverse)

    metrics = {
        "MSE": mse,
        "RMSE": rmse,
        "MAE": mae,
        "MAPE": mape,
        "R2": r2,
        "Epochs": epochs,
        "Batch Size": batch_size,
        "Look Back": look_back
    }

    # Save metrics and loss history to a JSON file
    metrics_file = "Model/lstm_model_metrics.json"
    metrics_with_history = {
        "metrics": metrics,
        "history": {
            "loss": history.history["loss"],
            "val_loss": history.history["val_loss"]
        }
    }
    with open(metrics_file, "w") as f:
        json.dump(metrics_with_history, f, indent=4)

    print(f"Model metrics and training history saved to {metrics_file}")

if __name__ == "__main__":
    train_lstm_model()
