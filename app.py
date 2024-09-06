from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the model (ensure the model file is correctly placed)
model = joblib.load("bitcoin_model.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data or 'features' not in data:
            raise ValueError("Invalid input data")
        
        features = np.array(data['features']).reshape(1, -1)
        prediction = model.predict(features)
        
        return jsonify({'prediction': prediction[0]})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)