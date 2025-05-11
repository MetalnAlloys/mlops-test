#! /bin/bash

# To run psql from this script
export PGPASSWORD=$POSTGRES_PASSWORD
export PGUSER=postgres
export PGHOST=$MLOPS_DB_HOST
export PGPORT=$MLOPS_DB_SERVICE_PORT

# Make sure Django doesn't try to connect to DB before it is fully online
echo "Waiting for DB to come online!"
#sleep 10
while ! pg_isready -d postgres -h ${PGHOST} -p ${PGPORT} -U ${PGUSER}; do sleep 1; done
echo "DB is online!"

# Check for Postgres DB and USER existence
#ans=$(psql -tc "SELECT 1 FROM pg_roles WHERE rolname='$MLOPS_DB_USER';")
#postgres_db_exits=$(psql  -tc "select * from pg_database where datname = '$MLOPS_DB_NAME';" \
#    | grep -o $MLOPS_DB_NAME)


## Conditionally run the following script if DB and user does not exist
#if [[ -z $postgres_user_exits && -z $postgres_db_exits ]]; then
#    printf "User: %s and DB: %s not found! Initializing DB ...\n" "$MLOPS_DB_USER" "$MLOPS_DB_NAME"

#elif [[ $ans -eq 1 && $postgres_db_exits == "$MLOPS_DB_NAME" ]]; then
#    printf "User: %s and DB: %s exists! Skipping DB setup ...\n" "$MLOPS_DB_USER" "$MLOPS_DB_NAME"
#fi


cd ml_server
python3 ./manage.py makemigrations
python3 ./manage.py migrate

if [ "$RUN_MODE" = "prod" ]; then
    python3 ./manage.py collectstatic --verbosity 1 --noinput
    gunicorn --chdir=ml_server ml_server.wsgi --bind "0.0.0.0:8000" --workers 4 --threads 4
else
    python3 ./manage.py runserver "0.0.0.0:8000"
fi

