import mlflow
import joblib

mlflow.set_experiment("VehiclePricePrediction")

with mlflow.start_run():

    model=joblib.load("models/model.pkl")

    mlflow.sklearn.log_model(model,"vehicle-model")

    print("Registered")