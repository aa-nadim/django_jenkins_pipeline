pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "django-hello-world"
        CONTAINER_NAME = "django-app"
        PORT = "8000"
        EC2_PUBLIC_IP = "52.91.21.162"
    }
    
    stages {
        stage('🚀 Quick Deploy') {
            steps {
                echo '⚡ Starting FAST CI/CD Pipeline...'
                
                sh '''
                    # Quick cleanup (parallel)
                    (docker stop $CONTAINER_NAME || true) &
                    (docker rmi $DOCKER_IMAGE || true) &
                    wait
                    docker rm $CONTAINER_NAME || true
                    
                    echo "⚡ Building optimized image..."
                    # Build with caching enabled
                    docker build -t $DOCKER_IMAGE . --quiet
                    
                    echo "⚡ Running quick tests..."
                    # Run tests quickly in temporary container
                    docker run --rm $DOCKER_IMAGE python manage.py test --verbosity=1 --keepdb
                    
                    echo "⚡ Deploying instantly..."
                    # Deploy immediately
                    docker run -d \
                        --name $CONTAINER_NAME \
                        -p $PORT:8000 \
                        --restart unless-stopped \
                        $DOCKER_IMAGE
                    
                    # Quick health check (5 seconds only)
                    sleep 5
                    
                    if docker ps | grep -q $CONTAINER_NAME; then
                        echo "✅ DEPLOYED in under 60 seconds!"
                        echo "🌐 App: http://$EC2_PUBLIC_IP:$PORT"
                        echo "❤️ Health: http://$EC2_PUBLIC_IP:$PORT/health/"
                    else
                        echo "❌ Quick deploy failed"
                        exit 1
                    fi
                '''
            }
        }
    }
    
    post {
        success {
            echo '🎉 LIGHTNING FAST SUCCESS! Total time: ~30-60 seconds'
            echo "Visit: http://${EC2_PUBLIC_IP}:8000"
        }
        failure {
            echo '❌ Fast pipeline failed'
            sh 'docker stop $CONTAINER_NAME || true && docker rm $CONTAINER_NAME || true'
        }
    }
}