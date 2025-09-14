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
        
    stages {
        stage('⚡Deploy') {
            steps {
                echo '⚡ SUPER FAST CI/CD - Direct Deploy!'
                
                sh '''
                    # Kill any existing Django process
                    pkill -f "manage.py runserver" || true
                    
                    # Update code
                    cd /tmp
                    rm -rf django_jenkins_pipeline || true
                    git clone https://github.com/aa-nadim/django_jenkins_pipeline.git
                    cd django_jenkins_pipeline
                    
                    # Quick setup
                    pip3 install -r requirements.txt --quiet
                    python3 manage.py makemigrations --noinput
                    python3 manage.py migrate --noinput
                    
                    # Run tests quickly
                    python3 manage.py test --verbosity=1 --keepdb
                    
                    # Start Django in background
                    nohup python3 manage.py runserver 0.0.0.0:$PORT > /tmp/django.log 2>&1 &
                    
                    # Quick verification
                    sleep 3
                    if curl -f -s http://localhost:$PORT/health/ > /dev/null; then
                        echo "✅ SUPER FAST DEPLOY SUCCESS!"
                        echo "🌐 Live at: http://$EC2_PUBLIC_IP:$PORT"
                        echo "⚡ Total time: ~10-20 seconds!"
                    else
                        echo "❌ Deploy failed"
                        tail /tmp/django.log
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