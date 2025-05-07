#!/bin/sh

if [ "$DATABASE" = "pgdb" ]
then
    echo "Waiting for pgdb..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "Starting api service in...: $ENVIRONMENT_AREA"
if [ "$ENVIRONMENT_AREA" = "DEVELOPMENT" ]; then
    uvicorn src:app --port 8000 --host 0.0.0.0 --reload
else
    echo "Invalid ENVIRONMENT_AREA value. Please set it to DEVELOPMENT, PRODUCTION, or STAGING."
    exit 1
fi

exec "$@"
