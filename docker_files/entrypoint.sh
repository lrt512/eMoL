#!/bin/bash
# Redirect script output to stdout for logging
exec > >(tee -ia /var/log/entrypoint.log)
exec 2>&1

DID_POSTGRES_CONFIGURE=0

# Replace these with values obtained from your secrets manager later
POSTGRES_PASSWORD=abc123  # Use a more secure method in production
DJANGO_SECRET_KEY=xyz789

export DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY

emol_table_exists() {
    exists=$(su - postgres -c "psql -d emol -tAc \"SELECT 1 FROM information_schema.tables WHERE table_name = 'cards_combatant'\"")
    if [ "$exists" = "1" ]; then
        return 0
    fi
    return 1
}

emol_role_exists() {
    exists=$(su - postgres -c "psql -tAc \"SELECT 1 FROM pg_roles WHERE rolname = 'emol_db_user'\"")
    if [ "$exists" = "1" ]; then
        return 0
    fi
    return 1
}

is_postgres_configured() {
    if emol_role_exists && emol_table_exists; then
        return 0
    fi
    return 1
}

sudo_psql() {
    su - postgres -c "psql -c \"$1\""
}

create_emol_database() {
    sudo_psql "SELECT 1 FROM pg_database WHERE datname = '$1'" | grep -q 1 || sudo_psql "CREATE DATABASE $1;"
    sudo_psql "GRANT ALL PRIVILEGES ON DATABASE $1 TO emol_db_user;"
    sudo_psql "ALTER DATABASE $1 OWNER TO emol_db_user;"
}

# Function to configure PostgreSQL
configure_postgres() {
    echo "PostgreSQL is not configured. Configuring..."
    sudo_psql "ALTER USER postgres WITH PASSWORD '$POSTGRES_PASSWORD';"
    sudo_psql "DROP DATABASE IF EXISTS test;"
    
    # Check if emol_db_user exists before creating
    if emol_role_exists; then
        echo "emol_db_user exists."
    else
        echo "Creating emol_db_user..."
        sudo_psql "CREATE ROLE emol_db_user LOGIN PASSWORD 'temp_password';"
        sudo_psql "ALTER ROLE emol_db_user SET client_encoding TO 'utf8';"
        sudo_psql "ALTER ROLE emol_db_user SET default_transaction_isolation TO 'read committed';"
        sudo_psql "ALTER ROLE emol_db_user SET timezone TO 'UTC';"
    fi

    create_emol_database emol
    create_emol_database emol_cache
    DID_POSTGRES_CONFIGURE=1
    echo "Done configuring PostgreSQL."
}

ensure_emol_db_user() {
    # Generate a new random password for emol db user
    EMOL_DB_PASSWORD=$(openssl rand -base64 32)
    export EMOL_DB_PASSWORD=$EMOL_DB_PASSWORD
    sudo_psql "ALTER USER emol_db_user WITH PASSWORD '$EMOL_DB_PASSWORD';"
}

# Start PostgreSQL service
echo "Starting PostgreSQL..."
service postgresql start

# Wait for PostgreSQL to start up
until pg_isready -h localhost -U postgres; do
    echo 'Waiting for PostgreSQL to start...'
    sleep 1
done

if is_postgres_configured; then
    echo "PostgreSQL is already configured."
else
    configure_postgres
fi

# Reset emol_db_user password every time
ensure_emol_db_user

# Fire up nginx
echo "Testing nginx..."
nginx -t

# Exit if nginx test fails
if [ $? -ne 0 ]; then
    echo "Nginx test failed. Exiting."
    exit 1
fi

echo "Starting nginx..."
service nginx start

# Health check for Nginx
until service nginx status | grep -q 'is running'; do
    echo "Waiting for Nginx to start..."
    sleep 1
done
echo "Nginx started successfully."

cd /app
echo "Apply migrations"
/venv/bin/python manage.py migrate

echo "Collect static files"
/venv/bin/python manage.py collectstatic --noinput

echo "Create cache table"
/venv/bin/python manage.py createcachetable

if [[ $DID_POSTGRES_CONFIGURE -eq 1 ]]; then
    echo -e "\n"
    echo -e "🚨 \033[1;96mDon't forget to shell in and finish configuration!\033[0m 🚨"
    echo -e "\n"
fi

echo "Starting Gunicorn..."
exec /venv/bin/python /venv/bin/gunicorn \
    --access-logfile - \
    --workers 3 \
    --bind unix:/app/emol.sock \
    emol.wsgi:application
