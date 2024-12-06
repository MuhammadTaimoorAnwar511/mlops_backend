import requests

BASE_URL = "http://localhost:5000"

def test_signup_user_already_exists():
    response = requests.post(f"{BASE_URL}/signup", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 400
    assert response.json() == {"error": "Username already exists"}

def test_login_success():
    response = requests.post(f"{BASE_URL}/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_predict_route():
    # Login to get token
    login_response = requests.post(f"{BASE_URL}/login", json={"username": "testuser", "password": "testpass"})
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    data = {"features": [1000]}  # Example features
    response = requests.post(f"{BASE_URL}/predict", json=data, headers=headers)
    assert response.status_code == 200
    assert "predicted_price" in response.json()
