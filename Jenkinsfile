pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'my-flask-api'
        DOCKER_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building the application...'

                // Install Python dependencies
                script {
                    if (isUnix()) {
                        sh 'pip install -r requirements.txt'
                        sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                        sh "docker build -t ${DOCKER_IMAGE}:latest ."
                    } else {
                        bat 'pip install -r requirements.txt'
                        bat "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                        bat "docker build -t ${DOCKER_IMAGE}:latest ."
                    }
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                script {
                    if (isUnix()) {
                        sh 'python -m pytest test_app.py -v --tb=short'
                    } else {
                        bat 'python -m pytest test_app.py -v --tb=short'
                    }
                }
            }
        }

        stage('Code Quality') {
            steps {
                echo 'Running code quality checks...'
                script {
                    // Basic code quality checks using Python built-in tools
                    if (isUnix()) {
                        sh 'python -m py_compile app.py'
                        sh 'python -c "import ast; ast.parse(open(\'app.py\').read())"'
                    } else {
                        bat 'python -m py_compile app.py'
                        bat 'python -c "import ast; ast.parse(open(\'app.py\').read())"'
                    }
                }
                echo 'Code quality checks passed!'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying to test environment...'
                script {
                    if (isUnix()) {
                        sh 'docker stop my-flask-api || true'
                        sh 'docker rm my-flask-api || true'
                        sh "docker run -d --name my-flask-api -p 5000:5000 ${DOCKER_IMAGE}:latest"

                        // Wait for container to start
                        sh 'sleep 10'

                        // Test deployment
                        sh 'curl -f http://localhost:5000/health || exit 1'
                    } else {
                        bat 'docker stop my-flask-api || exit 0'
                        bat 'docker rm my-flask-api || exit 0'
                        bat "docker run -d --name my-flask-api -p 5000:5000 ${DOCKER_IMAGE}:latest"

                        // Wait for container to start
                        bat 'timeout 10'

                        // Test deployment (for Windows)
                        bat 'curl -f http://localhost:5000/health'
                    }
                }
                echo 'Deployment successful!'
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed!'
            script {
                // Clean up Docker containers (optional)
                if (isUnix()) {
                    sh 'docker system prune -f || true'
                } else {
                    bat 'docker system prune -f || exit 0'
                }
            }
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed! '
        }
    }
}
