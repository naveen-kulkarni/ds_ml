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