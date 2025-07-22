#!/bin/bash
set -e

# Create databases for each service
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE common_service;
    GRANT ALL PRIVILEGES ON DATABASE common_service TO $POSTGRES_USER;
EOSQL



echo "All databases created successfully!"
