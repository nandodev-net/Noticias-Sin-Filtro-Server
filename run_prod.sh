#!/bin/bash
# Use this file to start the production server
echo "Shutting down active servers..."
docker-compose -f docker-compose.prod.yml down -v
echo "Building docker composer file..."
docker-compose -f docker-compose.prod.yml up -d --build
echo "Collecting static files..."
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear &&\
echo "Running migrations..."
echo "Ready to go!"
echo "to run migrations, use the following commnad:"
echo "docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput"
echo "You can test this server by requesting to localhost:1337/admin"