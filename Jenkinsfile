pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'my-flask-api'
        DOCKER_TAG = "${BUILD_NUMBER}"
        // Add paths where tools might be located
        PATH = "/usr/local/bin:/opt/homebrew/bin:/Applications/Docker.app/Contents/Resources/bin:${env.PATH}"
    }
    
    stages {
        stage('Build') {
            steps {
                echo 'Building the application...'
                
                // Install Python dependencies using virtual environment
                script {
                    if (isUnix()) {
                        sh '''
                            # Create virtual environment if it doesn't exist
                            if [ ! -d ".venv" ]; then
                                python3 -m venv .venv || python -m venv .venv
                            fi
                            
                            # Activate virtual environment and install dependencies
                            source .venv/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                        
                        // Build Docker images
                        sh '''
                            # Try different docker commands
                            if command -v docker &> /dev/null; then
                                docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                                docker build -t ${DOCKER_IMAGE}:latest .
                            elif command -v /usr/local/bin/docker &> /dev/null; then
                                /usr/local/bin/docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                                /usr/local/bin/docker build -t ${DOCKER_IMAGE}:latest .
                            elif command -v /Applications/Docker.app/Contents/Resources/bin/docker &> /dev/null; then
                                /Applications/Docker.app/Contents/Resources/bin/docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                                /Applications/Docker.app/Contents/Resources/bin/docker build -t ${DOCKER_IMAGE}:latest .
                            else
                                echo "Docker not found, skipping Docker build"
                            fi
                        '''
                    } else {
                        bat '''
                            pip install -r requirements.txt
                            docker build -t %DOCKER_IMAGE%:%DOCKER_TAG% .
                            docker build -t %DOCKER_IMAGE%:latest .
                        '''
                    }
                }
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests...'
                script {
                    if (isUnix()) {
                        sh '''
                            # Activate virtual environment and run tests
                            source .venv/bin/activate
                            python -m pytest test_app.py -v --tb=short
                        '''
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
                    if (isUnix()) {
                        sh '''
                            # Activate virtual environment and run code quality checks
                            source .venv/bin/activate
                            python -m py_compile app.py
                            python -c "import ast; ast.parse(open('app.py').read())"
                        '''
                    } else {
                        bat '''
                            python -m py_compile app.py
                            python -c "import ast; ast.parse(open('app.py').read())"
                        '''
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
                        sh '''
                            # Find docker command
                            DOCKER_CMD=""
                            if command -v docker &> /dev/null; then
                                DOCKER_CMD="docker"
                            elif command -v /usr/local/bin/docker &> /dev/null; then
                                DOCKER_CMD="/usr/local/bin/docker"
                            elif command -v /Applications/Docker.app/Contents/Resources/bin/docker &> /dev/null; then
                                DOCKER_CMD="/Applications/Docker.app/Contents/Resources/bin/docker"
                            else
                                echo "Docker not found, skipping deployment"
                                exit 1
                            fi
                            
                            # Deploy using found docker command
                            $DOCKER_CMD stop my-flask-api || true
                            $DOCKER_CMD rm my-flask-api || true
                            $DOCKER_CMD run -d --name my-flask-api -p 5000:5000 ${DOCKER_IMAGE}:latest
                            
                            # Wait for container to start
                            sleep 10
                            
                            # Test deployment
                            curl -f http://localhost:5000/health || exit 1
                        '''
                    } else {
                        bat '''
                            docker stop my-flask-api || exit 0
                            docker rm my-flask-api || exit 0
                            docker run -d --name my-flask-api -p 5000:5000 %DOCKER_IMAGE%:latest
                            timeout 10
                            curl -f http://localhost:5000/health
                        '''
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
                if (isUnix()) {
                    sh '''
                        # Try to clean up with different docker commands
                        if command -v docker &> /dev/null; then
                            docker system prune -f || true
                        elif command -v /usr/local/bin/docker &> /dev/null; then
                            /usr/local/bin/docker system prune -f || true
                        elif command -v /Applications/Docker.app/Contents/Resources/bin/docker &> /dev/null; then
                            /Applications/Docker.app/Contents/Resources/bin/docker system prune -f || true
                        else
                            echo "Docker not found for cleanup"
                        fi
                    '''
                } else {
                    bat 'docker system prune -f || exit 0'
                }
            }
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
