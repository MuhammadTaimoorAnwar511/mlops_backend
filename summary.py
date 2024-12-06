import tensorflow as tf  # Import TensorFlow as tf
from tensorflow.keras.models import load_model

# Path to your LSTM model
MODEL_PATH = "Model/bitcoin_lstm_model.h5"

# Load the model
model = load_model(MODEL_PATH)
print(model.summary())  # Print the model summary

# Print TensorFlow version
print(f"TensorFlow Version: {tf.__version__}")

# Load the model without compiling
model = load_model(MODEL_PATH, compile=False)
print("TensorFlow is using GPU:", tf.config.list_physical_devices('GPU'))