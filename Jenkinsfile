pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'pytest test_app.py'
            }
        }
        stage('Code Quality') {
            steps {
                sh 'python -m py_compile app.py'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker build -t my-flask-api .'
                sh 'docker run -d -p 5000:5000 my-flask-api'
            }
        }
    }
}

