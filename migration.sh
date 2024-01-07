#!/bin/bash

# Exit script immediately on first error.
set -e 

# Function to run SQL file
run_sql_file() {
    local file="$1"
    PGPASSWORD=${DB_PASSWORD} psql -h "${DB_HOST}" -p "${DB_PORT}" -d "${DB_NAME}" -U "${DB_USER}" -f "$file"
}

# Flag to indicate whether to prompt for DB info
prompt_for_db_info=false

# Check if .migration_info exists and source it
if [ -f .migration_info ]; then
    source .migration_info
    # Check if any of the variables are empty
    if [ -z "$DB_HOST" ] || [ -z "$DB_NAME" ] || [ -z "$DB_PORT" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ]; then
        prompt_for_db_info=true # Some values are empty, so prompt user for values
    fi
else
    prompt_for_db_info=true # No .migration_info file, so prompt user for values
fi

# If .migration_info doesn't exist or any of the variables are empty, prompt for DB info
if $prompt_for_db_info ; then
    echo "Please enter the following database connection information that can be found in Supabase in Settings -> database:"
    DB_HOST=$(gum input --placeholder "Host - e.g. db.<your-project>.supabase.co")
    DB_NAME=$(gum input --placeholder "Database name: always postgres")
    DB_PORT=$(gum input --placeholder "Port: always 5432")
    DB_USER=$(gum input --placeholder "User: always postgres")
    DB_PASSWORD=$(gum input --placeholder "Password: the one you used at inti" --password)

    # Save the inputs in .migration_info file
    echo "DB_HOST=$DB_HOST" > .migration_info
    echo "DB_NAME=$DB_NAME" >> .migration_info
    echo "DB_PORT=$DB_PORT" >> .migration_info
    echo "DB_USER=$DB_USER" >> .migration_info
    echo "DB_PASSWORD=$DB_PASSWORD" >> .migration_info
fi

# Ask user whether to create tables or run migrations
CHOICE=$(gum choose --header "Choose an option" "Create all tables (First Time)" "Run Migrations (After updating Quivr)")

if [ "$CHOICE" == "Create all tables (First Time)" ]; then
    # Running the tables.sql file to create tables
    run_sql_file "scripts/tables.sql"
else

    # Get the last migration that was executed
    LAST_MIGRATION=$(PGPASSWORD=${DB_PASSWORD} psql -h "${DB_HOST}" -p "${DB_PORT}" -d "${DB_NAME}" -U "${DB_USER}" -tAc "SELECT name FROM migrations ORDER BY executed_at DESC LIMIT 1;")
    
    echo "Last migration executed: $LAST_MIGRATION"
    # Iterate through the migration files
    for file in $(ls scripts | grep -E '^[0-9]+.*\.sql$' | sort); do
        MIGRATION_ID=$(basename "$file" ".sql")
        
        # Only run migrations that are newer than the last executed migration
        if [ -z "$LAST_MIGRATION" ] || [ "$MIGRATION_ID" \> "$LAST_MIGRATION" ]; then
            # Run the migration
            echo "Running migration $file"
            run_sql_file "scripts/$file"
            # And record it as having been run
            PGPASSWORD=${DB_PASSWORD} psql -h "${DB_HOST}" -p "${DB_PORT}" -d "${DB_NAME}" -U "${DB_USER}" -c "INSERT INTO migrations (name) VALUES ('${MIGRATION_ID}');"
        fi
    done
fi

echo "Migration script completed."
