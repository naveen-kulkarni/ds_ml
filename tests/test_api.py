import requests

payload={

"year":2021,

"mileage":10000,

"engine":2.0,

"horsepower":210

}

response=requests.post(
"http://localhost:5000/predict",
json=payload
)

assert response.status_code==200