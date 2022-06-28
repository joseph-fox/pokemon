#!/bin/sh

echo "Ensure PostgreSQL is running..."

while ! nc -z $DB_URL $DB_PORT; do
    sleep 0.05
done

exec "$@"
