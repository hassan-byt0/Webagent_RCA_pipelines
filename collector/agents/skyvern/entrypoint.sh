#!/bin/bash
set -e

cd "$(dirname "$0")" || exit

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

run_alembic_upgrade() {
    echo "Running Alembic upgrade..."
    alembic upgrade head
}

setup_postgresql() {
    echo "Initializing local PostgreSQL server..."

    chown -R postgres:postgres /var/lib/postgresql
    chown -R postgres:postgres /var/run/postgresql
    mkdir -p /var/run/postgresql && chown postgres:postgres /var/run/postgresql

    # Start PostgreSQL in the background
    service postgresql start

    # Wait for PostgreSQL to become ready
    until pg_isready -h localhost > /dev/null 2>&1; do
        echo "Waiting for PostgreSQL to start..."
        sleep 1
    done

    echo "PostgreSQL is running."

    local db_user="skyvern"
    local db_name="skyvern"

    # Create user and database as the postgres OS user (peer auth)
    if ! su - postgres -c "psql -tAc \"SELECT 1 FROM pg_roles WHERE rolname='$db_user'\"" | grep -q 1; then
        echo "Creating database user '$db_user'..."
        su - postgres -c "psql -c \"CREATE USER $db_user;\""
    else
        echo "Database user '$db_user' exists."
    fi

    if ! su - postgres -c "psql -lqt" | cut -d \| -f 1 | grep -qw $db_name; then
        echo "Creating database '$db_name'..."
        su - postgres -c "createdb $db_name -O $db_user"
        echo "Database '$db_name' created successfully."
    else
        echo "Database '$db_name' exists."
    fi

    # Grant privileges
    su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE $db_name TO $db_user;\""

    # Update .env file with database credentialupdate_or_add_env_vars
    update_or_add_env_var "DATABASE_USERNAME" "$db_user"
    update_or_add_env_var "DATABASE_PASSWORD" ""
    update_or_add_env_var "DATABASE_HOST" "localhost"
    update_or_add_env_var "DATABASE_PORT" "5432"
    update_or_add_env_var "DATABASE_NAME" "$db_name"

    echo "Configuring PostgreSQL to use 'trust' authentication method..."

    local pg_hba_conf="/etc/postgresql/14/main/pg_hba.conf"
    cp "$pg_hba_conf" "${pg_hba_conf}.backup"

    sed -i "s/^local\s\+all\s\+all\s\+.*/local   all             all                                     trust/" "$pg_hba_conf"

    sed -i "/^host\s\+all\s\+all\s\+127\.0\.0\.1\/32/d" "$pg_hba_conf"
    sed -i "/^host\s\+all\s\+all\s\+::1\/128/d" "$pg_hba_conf"

    sed -i "/^local   all\s\+all\s\+trust/a host    all             all             127.0.0.1/32            trust\nhost    all             all             ::1/128                 trust" "$pg_hba_conf"

    grep -q "^host\s\+all\s\+all\s\+0\.0\.0\.0/0\s\+trust" "$pg_hba_conf" || echo "host all all 0.0.0.0/0 trust" >> "$pg_hba_conf"
    grep -q "^host\s\+all\s\+all\s+::/0\s\+trust" "$pg_hba_conf" || echo "host all all ::/0 trust" >> "$pg_hba_conf"

    echo "Configuring PostgreSQL to listen on all interfaces..."
    sed -i "s/^#listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/14/main/postgresql.conf

    echo "Restarting PostgreSQL to apply authentication..."
    service postgresql restart

    until pg_isready -h localhost > /dev/null 2>&1; do
        echo "Waiting for PostgreSQL to restart..."
        sleep 1
    done

    echo "PostgreSQL restarted."
}

# Function to create organization and API token
create_organization() {
    echo "Creating organization and API token..."
    local org_output api_token
    org_output=$(python scripts/create_organization.py Skyvern-Open-Source http://localhost:5001/callback)
    api_token=$(echo "$org_output" | awk '/token=/{gsub(/.*token='\''|'\''.*/, ""); print}')

    update_or_add_env_var_file "X_API_KEY" "$api_token" "../../.env"

    # Ensure .streamlit directory exists
    mkdir -p .streamlit

    # Check if secrets.toml exists and back it up
    if [ -f ".streamlit/secrets.toml" ]; then
        mv .streamlit/secrets.toml .streamlit/secrets.backup.toml
        echo "Existing secrets.toml file backed up as secrets.backup.toml"
    fi

    # Update the secrets-open-source.toml file
    echo -e "[skyvern]\nconfigs = [\n    {\"env\" = \"local\", \"host\" = \"http://127.0.0.1:8000/api/v1\", \"orgs\" = [{name=\"Skyvern\", cred=\"$api_token\"}]}\n]" > .streamlit/secrets.toml
    echo ".streamlit/secrets.toml file updated with organization details."

    # Check if skyvern-frontend/.env exists and back it up
    # This is redundant for first time set up but useful for subsequent runs
    if [ -f "skyvern-frontend/.env" ]; then
        mv skyvern-frontend/.env skyvern-frontend/.env.backup
        echo "Existing skyvern-frontend/.env file backed up as skyvern-frontend/.env.backup"
        cp skyvern-frontend/.env.example skyvern-frontend/.env
    fi

    # Update the skyvern-frontend/.env file
    # sed wants a backup file extension, and providing empty string doesn't work on all platforms
    sed -i".old" -e "s/YOUR_API_KEY/$api_token/g" skyvern-frontend/.env
    echo "skyvern-frontend/.env file updated with API token."
}

# Function to update or add environment variable in .env file
update_or_add_env_var() {
    local key=$1
    local value=$2
    if grep -q "^$key=" .env; then
        # Update existing variable
        sed -i.bak "s/^$key=.*/$key=$value/" .env && rm -f .env.bak
    else
        # Add new variable
        echo "$key=$value" >> .env
    fi
}

# Update or add environment variables in a specified file
update_or_add_env_var_file() {
    echo "Updating or adding environment variable in file..."
    local key=$1
    local value=$2
    local file=$3
    if grep -q "^$key=" "$file"; then
        # Update existing variable
        sed -i.bak "s/^$key=.*/$key=$value/" "$file" && rm -f "$file".bak
    else
        # Add new variable with a newline
        echo -e "\n$key=$value" >> "$file"
    fi
}

setup_llm_providers() {
    echo "Configuring Large Language Model (LLM) Providers..."
    echo "Enabling OpenAI with hardcoded API key."

    local openai_api_key="${OPENAI_API_KEY:-}"  # Set via environment variable

    update_or_add_env_var "OPENAI_API_KEY" "$openai_api_key"
    update_or_add_env_var "ENABLE_OPENAI" "true"
    update_or_add_env_var "ENABLE_ANTHROPIC" "false"
    update_or_add_env_var "ENABLE_AZURE" "false"
    update_or_add_env_var "ENABLE_GEMINI" "false"
    update_or_add_env_var "ENABLE_OPENROUTER" "false"
    update_or_add_env_var "ENABLE_GROQ" "false"
    update_or_add_env_var "ENABLE_NOVITA" "false"
    # Enable Hugging Face
    update_or_add_env_var "ENABLE_HUGGING_FACE" "false"
    
    local chosen_model="OPENAI_GPT4_1"
    echo "Chosen LLM Model: $chosen_model"
    update_or_add_env_var "LLM_KEY" "$chosen_model"

    echo "LLM provider configurations updated in .env."
}

# Function to initialize .env file
initialize_env_file() {
    # if [ -f ".env" ]; then
    #     echo ".env file already exists, skipping initialization."
    # fi

    echo "Initializing .env file..."
    cp .env.example .env
    setup_llm_providers

    echo ".env file has been initialized."
}

initialize_frontend_env_file() {
    # if [ -f "skyvern-frontend/.env" ]; then
    #     echo "skyvern-frontend/.env file already exists, skipping initialization."
    #     return
    # fi

    echo "Initializing skyvern-frontend/.env file..."
    cp skyvern-frontend/.env.example skyvern-frontend/.env
    echo "skyvern-frontend/.env file has been initialized."
}

start_virtual_display() {
    echo "Setting Xvfb display"
    Xvfb :99 -screen 0 1920x1080x24 &
    sleep 2
    export DISPLAY=:99
}

main() {
    initialize_env_file
    initialize_frontend_env_file
    setup_postgresql
    run_alembic_upgrade
    create_organization
    start_virtual_display
    exec "$@"
}

main "$@"
