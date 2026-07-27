pipeline {
    agent any

    environment {
        REGISTRY = "registry.company.com/ml"
        IMAGE_NAME = "vehicle-predictor"
        IMAGE_TAG = "${BUILD_NUMBER}"

        MLFLOW_TRACKING_URI = "http://mlflow.company.com"
        MODEL_NAME = "vehicle_classifier"

        KUBE_NAMESPACE = "ml-prod"

        PYTHON = "python3"
    }

    options {
        timestamps()
        ansiColor('xterm')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Code Quality') {
            parallel {

                stage('Lint') {
                    steps {
                        sh '''
                        . venv/bin/activate
                        flake8 src/
                        '''
                    }
                }

                stage('Unit Tests') {
                    steps {
                        sh '''
                        . venv/bin/activate
                        pytest tests/
                        '''
                    }
                }
            }
        }

        stage('Data Validation') {
            steps {
                sh '''
                . venv/bin/activate
                python pipelines/validate_data.py
                '''
            }
        }

        stage('Data Versioning') {
            steps {
                sh '''
                . venv/bin/activate
                dvc pull
                '''
            }
        }

        stage('Feature Engineering') {
            steps {
                sh '''
                . venv/bin/activate
                python pipelines/feature_engineering.py
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                . venv/bin/activate
                python pipelines/train.py
                '''
            }
        }

        stage('Evaluate Model') {
            steps {
                sh '''
                . venv/bin/activate
                python pipelines/evaluate.py
                '''
            }
        }

        stage('Register Model') {
            steps {
                sh '''
                . venv/bin/activate

                export MLFLOW_TRACKING_URI=${MLFLOW_TRACKING_URI}

                python pipelines/register_model.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build \
                -t ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} .
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                sh """
                docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Deploy to Staging') {
            steps {
                sh """
                helm upgrade --install vehicle-api \
                helm/vehicle-api \
                --namespace staging \
                --set image.repository=${REGISTRY}/${IMAGE_NAME} \
                --set image.tag=${IMAGE_TAG}
                """
            }
        }

        stage('Integration Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest integration/
                '''
            }
        }

        stage('Approval') {
            steps {
                input "Deploy model to Production?"
            }
        }

        stage('Deploy Production') {
            steps {
                sh """
                helm upgrade --install vehicle-api \
                helm/vehicle-api \
                --namespace ${KUBE_NAMESPACE} \
                --set image.repository=${REGISTRY}/${IMAGE_NAME} \
                --set image.tag=${IMAGE_TAG}
                """
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                python scripts/smoke_test.py
                '''
            }
        }

        stage('Publish Metrics') {
            steps {
                sh '''
                python monitoring/publish_metrics.py
                '''
            }
        }
    }

    post {

        success {
            echo "Pipeline completed successfully."
        }

        failure {
            echo "Pipeline failed."
        }

        always {
            archiveArtifacts artifacts: 'models/**'
            junit 'reports/*.xml'
        }
    }
}