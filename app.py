from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import os
from dotenv import load_dotenv
import joblib
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)
# MongoDB Atlas connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["MLOPS"]  # Database name
users_collection = db["users"]  # Users collection

# Bcrypt for password hashing
bcrypt = Bcrypt(app)

# JWT setup
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_secret_key")
jwt = JWTManager(app)

# Load LSTM model and scaler
MODEL_PATH = "Model/bitcoin_lstm_model.h5"
SCALER_PATH = "Model/bitcoin_scaler.pkl"

if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
    lstm_model = load_model(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
else:
    lstm_model = None
    scaler = None


@app.route("/signup", methods=["POST"])
def signup():
    """
    Endpoint for user signup.
    """
    data = request.json

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password are required"}), 400

    username = data["username"]
    password = data["password"]

    # Check if username already exists
    if users_collection.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    # Insert user into database
    users_collection.insert_one({"username": username, "password": hashed_password})

    return jsonify({"message": "Signup successful"}), 201


@app.route("/login", methods=["POST"])
def login():
    """
    Endpoint for user login.
    """
    data = request.json

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password are required"}), 400

    username = data["username"]
    password = data["password"]

    # Find user in database
    user = users_collection.find_one({"username": username})
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    # Check password
    if not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid username or password"}), 401

    # Create JWT token (pass username as a string)
    access_token = create_access_token(identity=username)

    return jsonify({"message": "Login successful", "access_token": access_token}), 200


@app.route("/predict", methods=["POST"])
@jwt_required()
def predict():
    """
    Endpoint for predicting Bitcoin prices using the LSTM model.
    Requires a valid JWT token.
    """
    try:
        # Debugging: Check if model and scaler are loaded
        if lstm_model is None or scaler is None:
            print("Debug: Model or scaler not found")  # Debugging statement
            return jsonify({"error": "Model or scaler not found"}), 500

        # Debugging: Check incoming data
        data = request.json
        print(f"Debug: Received data - {data}")  # Debugging statement

        if not data or "features" not in data:
            print("Debug: Features are missing in the request data")  # Debugging statement
            return jsonify({"error": "Features are required for prediction"}), 400

        # Reshape and scale input features
        features = np.array(data["features"], dtype=float).reshape(-1, 1)
        print(f"Debug: Features reshaped - {features}")  # Debugging statement

        scaled_features = scaler.transform(features)
        print(f"Debug: Features scaled - {scaled_features}")  # Debugging statement

        input_features = np.reshape(scaled_features, (1, scaled_features.shape[0], 1))
        print(f"Debug: Input features reshaped for prediction - {input_features}")  # Debugging statement

        # Perform prediction
        prediction = lstm_model.predict(input_features)
        print(f"Debug: Raw prediction from model - {prediction}")  # Debugging statement

        predicted_price = float(scaler.inverse_transform(prediction)[0][0])  # Ensure JSON serializable
        print(f"Debug: Predicted price - {predicted_price}")  # Debugging statement

        return jsonify({"predicted_price": predicted_price}), 200
    except Exception as e:
        # Debugging: Log exception details
        print(f"Debug: Exception occurred - {str(e)}")  # Debugging statement
        return jsonify({"error": str(e)}), 500


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    """
    Protected endpoint that requires a valid JWT token.
    """
    current_user = get_jwt_identity()  # Now, this returns a string (username)
    return jsonify({"message": f"Welcome, {current_user}! You have access to this protected route."}), 200




@app.route("/", methods=["GET"])
def home():
    """
    Home endpoint.
    """
    return jsonify({"message": "Welcome to the Bitcoin Prediction API!"}), 200


if __name__ == "__main__":
    #app.run(debug=True)
    app.run(debug=True, host="0.0.0.0")
