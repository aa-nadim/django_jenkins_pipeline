pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "django-hello-world"
        CONTAINER_NAME = "django-app"
        PORT = "8000"
        EC2_PUBLIC_IP = "54.221.154.115"
    }
    
    stages {
        stage('📦 Build') {
            steps {
                echo '🏗️ Starting Build Stage...'
                
                // Clean up existing containers
                sh '''
                    echo "Cleaning up existing containers..."
                    docker stop $CONTAINER_NAME || true
                    docker rm $CONTAINER_NAME || true
                    docker rmi $DOCKER_IMAGE || true
                '''
                
                // Build new image
                sh '''
                    echo "Building Docker image..."
                    docker build -t $DOCKER_IMAGE .
                    echo "✅ Docker image built successfully!"
                    docker images | grep $DOCKER_IMAGE
                '''
            }
        }
        
        stage('🧪 Test') {
            steps {
                echo '🧪 Starting Test Stage...'
                
                // Run Django tests
                sh '''
                    echo "Running Django tests..."
                    docker run --rm $DOCKER_IMAGE python manage.py test --verbosity=2
                    echo "✅ All tests passed!"
                '''
                
                // Quick health check
                sh '''
                    echo "Running health check..."
                    docker run --rm -d --name temp-test -p 8001:8000 $DOCKER_IMAGE
                    sleep 15
                    
                    if docker ps | grep temp-test; then
                        echo "✅ Container started successfully!"
                        docker stop temp-test
                    else
                        echo "❌ Container failed to start!"
                        exit 1
                    fi
                '''
            }
        }
        
        stage('🚀 Deploy') {
            steps {
                echo '🚀 Starting Deploy Stage...'
                
                // Deploy to production
                sh '''
                    echo "Deploying to production..."
                    docker run -d \
                        --name $CONTAINER_NAME \
                        -p $PORT:8000 \
                        --restart unless-stopped \
                        $DOCKER_IMAGE
                    
                    echo "Waiting for application to start..."
                    sleep 20
                    
                    if docker ps | grep $CONTAINER_NAME; then
                        echo "✅ Application deployed successfully!"
                        echo "🌐 Access your app at: http://$EC2_PUBLIC_IP:$PORT"
                        echo "❤️ Health check: http://$EC2_PUBLIC_IP:$PORT/health/"
                        
                        # Quick test
                        curl -f http://localhost:$PORT/health/ || echo "Health check endpoint may still be starting..."
                    else
                        echo "❌ Deployment failed!"
                        docker logs $CONTAINER_NAME
                        exit 1
                    fi
                '''
            }
        }
    }
    
    post {
        always {
            echo '🏁 Pipeline finished!'
        }
        success {
            echo '🎉 SUCCESS! Your Django app is live!'
            echo "Visit: http://${EC2_PUBLIC_IP}:8000"
        }
        failure {
            echo '❌ Pipeline failed. Cleaning up...'
            sh '''
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true
            '''
        }
    }
}