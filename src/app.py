from flask import Flask,request,jsonify
import joblib
import pandas as pd

app=Flask(__name__)

model=joblib.load("models/model.pkl")

@app.route("/predict",methods=["POST"])
def predict():

    data=request.json

    df=pd.DataFrame([data])

    prediction=model.predict(df)

    return jsonify({
        "predicted_price":float(prediction[0])
    })


@app.route("/")
def home():
    return {
        "service": "Vehicle Price Prediction",
        "status": "UP"
    }

@app.route("/health")
def health():
    return {
        "status": "healthy"
    }

app.run(host="0.0.0.0",port=5000)