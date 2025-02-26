#!/bin/sh
set -e

echo "Waiting for postgresdb to be available on port 5432..."
while ! nc -z postgresdb 5432; do
  sleep 1
done
echo "postgresdb is up - running migrations and collectstatic"

cd src
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "Starting Gunicorn"
exec gunicorn --workers 3 --bind 0.0.0.0:8000 enrolspwa.wsgi:application
