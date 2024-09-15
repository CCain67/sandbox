#!/bin/bash

# Define a marker file to indicate that initialization has been done
INIT_MARKER="/opt/airflow/.airflow_initialized"

# Wait for the Postgres database to be ready
echo "Waiting for the Postgres database..."
while ! pg_isready -h pgdb -p 5432 -U postgres; do
    sleep 1
done

if [ ! -f $INIT_MARKER ]; then
    echo "Initializing Airflow database..."
    airflow db init

    echo "Creating Airflow user..."
    airflow users create \
        --username chase \
        --firstname Chase \
        --lastname Cain \
        --role Admin \
        --email charlescain0607@gmail.com \
        --password admin

    # Create the marker file
    touch $INIT_MARKER
fi

echo "Starting the Airflow scheduler..."
airflow scheduler &

echo "Starting the Airflow webserver..."
exec airflow webserver
