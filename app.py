from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load the model (ensure the model file is correctly placed)
model = joblib.load("bitcoin_model.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    # Get the JSON data from the request
    data = request.get_json()
    features = np.array(data['features']).reshape(1, -1)
    
    # Predict the next day's closing price
    prediction = model.predict(features)
    
    # Return the prediction as a JSON response
    return jsonify({'prediction': prediction[0]})

@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)
