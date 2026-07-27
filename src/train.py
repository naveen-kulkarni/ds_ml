from pathlib import Path
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Data and model paths
DATA_FILE = BASE_DIR / "data" / "cars.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_FILE)

X = df[["year", "mileage", "engine", "horsepower"]]
y = df["price"]

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, MODEL_DIR / "model.pkl")

print("Model trained successfully.")
print(f"Model saved to {MODEL_DIR / 'model.pkl'}")