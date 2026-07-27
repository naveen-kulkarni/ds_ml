Directory structure
mkdir -p src
mkdir -p tests
mkdir -p pipelines
mkdir -p models
mkdir -p data
mkdir -p monitoring
mkdir -p integration
mkdir -p helm/vehicle-api
mkdir -p scripts

touch Jenkinsfile
touch Dockerfile
touch requirements.txt
touch README.md

touch src/model.py
touch src/predictor.py
touch src/utils.py

touch pipelines/train.py
touch pipelines/evaluate.py
touch pipelines/register_model.py


pip3 install -r requirements.txt

python3 src/train.py
Model trained successfully.
Model saved to /Users/naveen.kulkarni/Desktop/ds_ml/ds_ml/models/model.pkl

mlflow ui


 python3 src/app.py

 curl -X POST http://localhost:5000/predict \
-H "Content-Type: application/json" \
-d '{
"year":2020,
"mileage":15000,
"engine":2.0,
"horsepower":200
}'

Output:
{"predicted_price":25416.529122052714}

127.0.0.1 - - [27/Jul/2026 16:04:48] "POST /predict HTTP/1.1" 200 -


One more curl:
curl http://localhost:5000/health
{"status":"healthy"}



docker build -t vehicle-api .

docker run -p 5000:5000 vehicle-api

python3 pipelines/register_model.py
2026/07/27 16:12:37 INFO mlflow.tracking.fluent: Experiment with name 'VehiclePricePrediction' does not exist. Creating a new experiment.
2026/07/27 16:12:39 WARNING mlflow.models.model: `artifact_path` is deprecated. Please use `name` instead.
Registered
You should see an experiment named VehiclePricePrediction with the logged model.


kubectl apply -f deployment.yaml

