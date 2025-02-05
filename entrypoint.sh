#!/bin/sh

# Wait for database to be ready
echo "Waiting for PostgreSQL..."
# Use netcat to check if the database is available on the specified host and port
while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1  # Wait for 0.1 second before checking again
done
echo "PostgreSQL started"

# Make migrations
echo "Making migrations..."
# Create migrations for all apps
python manage.py makemigrations

# Apply database migrations
echo "Applying database migrations..."
# Apply migrations to the database
python manage.py migrate

# Create superuser
echo "Creating superuser..."
python manage.py createsuperuser_default

# Start server
echo "Starting server..."
# Run the Django development server on all interfaces (0.0.0.0) and port 8000
python manage.py runserver 0.0.0.0:8000