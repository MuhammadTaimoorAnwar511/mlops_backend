# & "C:/Program Files/Python312/python.exe" "c:/Users/LOQ/Desktop/7 SEMESTER/MLOPS/ClassTask_01/test_prediction.py"
import requests

url = "http://127.0.0.1:5000/predict"
data = {"features": [40000]} 

response = requests.post(url, json=data)
print("next day closing will be ")
print(response.json())
