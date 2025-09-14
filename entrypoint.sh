#!/bin/bash

# Django startup script

echo "🚀 Starting Django Hello World Application..."

echo "📋 Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput || echo "No static files to collect"

echo "✅ Setup completed! Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000