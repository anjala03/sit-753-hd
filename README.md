# Simple Flask REST API

This project is a beginner-friendly REST API for managing tasks, built with Flask. It includes unit tests, Docker support, and a Jenkins pipeline for CI/CD.

## How to Run Locally
1. Install Python 3.9+
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`

## How to Run Tests
`pytest test_app.py`

## How to Build Docker Image
`docker build -t my-flask-api .`

## How to Run Docker Container
`docker run -d -p 5000:5000 my-flask-api`

## Jenkins Pipeline
See `Jenkinsfile` for CI/CD stages.

# sit-753-hd
