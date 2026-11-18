#!/bin/bash
# Creates one database and one role per service, isolated from each other.
#
# Runs ONCE, when the data volume is empty. Editing this file after a
# successful `up` does nothing until `docker compose down -v`.
set -euo pipefail

create_service_database() {
  local db="$1" role="$2" password="$3"

  echo "==> ${db} (owner ${role})"

  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres <<-SQL
    CREATE ROLE ${role} WITH LOGIN PASSWORD '${password}';

    -- The role OWNS the database. Since Postgres 15 the public schema is
    -- owned by pg_database_owner, so ownership is what lets the role create
    -- tables. Without it Flyway fails with a permission error that reads
    -- like a Flyway bug.
    CREATE DATABASE ${db} OWNER ${role};

    -- Postgres grants CONNECT on every database to PUBLIC by default, so
    -- four roles and four databases are NOT isolation until this revoke
    -- happens. This line is the whole point of the exercise.
    REVOKE CONNECT ON DATABASE ${db} FROM PUBLIC;
    GRANT CONNECT ON DATABASE ${db} TO ${role};
SQL
}

create_service_database fm_auth       fm_auth       "${AUTH_DB_PASSWORD}"
create_service_database fm_expense    fm_expense    "${EXPENSE_DB_PASSWORD}"
create_service_database fm_investment fm_investment "${INVESTMENT_DB_PASSWORD}"
create_service_database fm_analytics  fm_analytics  "${ANALYTICS_DB_PASSWORD}"

echo "==> four databases created, cross-database access revoked"
