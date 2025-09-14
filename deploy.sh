#!/bin/bash

# Deployment script for Django Hello World application

CONTAINER_NAME="django-app"
IMAGE_NAME="django-hello-world"
PORT="8000"

echo "Starting deployment process..."

# Stop and remove existing container if it exists
if docker ps | grep -q $CONTAINER_NAME; then
    echo "Stopping existing container..."
    docker stop $CONTAINER_NAME
fi

if docker ps -a | grep -q $CONTAINER_NAME; then
    echo "Removing existing container..."
    docker rm $CONTAINER_NAME
fi

# Build new image
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

if [ $? -ne 0 ]; then
    echo "Docker build failed!"
    exit 1
fi

# Run new container
echo "Starting new container..."
docker run -d \
    --name $CONTAINER_NAME \
    -p $PORT:8000 \
    $IMAGE_NAME

if [ $? -ne 0 ]; then
    echo "Container start failed!"
    exit 1
fi

# Wait for container to start
sleep 10

# Check if container is running
if docker ps | grep -q $CONTAINER_NAME; then
    echo "✅ Deployment successful!"
    echo "🌐 Application is running at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):$PORT"
else
    echo "❌ Deployment failed - container is not running"
    docker logs $CONTAINER_NAME
    exit 1
fi