@app.route('/config')
def config():
    return jsonify({'apiUrl': os.getenv('API_URL', 'http://127.0.0.1:5000/predict')})
