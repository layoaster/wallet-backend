#!/bin/bash

# Reference script to create additionals users/dbs (if necessary).
# IMPORTANT: The script is ejecuted only once when there is no
# pre-existent database in the PostgresSQL data directory.
# More info: https://hub.docker.com/_/postgres

POSTGRES_TEST_DB="${POSTGRES_DB}_test"

set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL

    CREATE DATABASE $POSTGRES_TEST_DB;
    -- GRANT ALL PRIVILEGES ON DATABASE '$POSTGRES_TEST_DB' TO '$POSTGRES_USER';

EOSQL
