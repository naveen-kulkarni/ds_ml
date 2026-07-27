import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

df=pd.read_csv("data/cars.csv")

X=df[["year","mileage","engine","horsepower"]]
y=df["price"]

model=LinearRegression()

model.fit(X,y)

pred=model.predict(X)

print("Accuracy:",r2_score(y,pred))