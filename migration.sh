#!/bin/bash

# Function to run SQL file
run_sql_file() {
    local file="$1"
    PGPASSWORD=${DB_PASSWORD} psql -h "${DB_HOST}" -p "${DB_PORT}" -d "${DB_NAME}" -U "${DB_USER}" -f "$file"
}

# Check if .migration_info exists and source it, otherwise ask user for inputs
if [ -f .migration_info ]; then
    source .migration_info
else
    echo "Please enter the following database connection information that can be found in Supabase in Settings -> database:"
    DB_HOST=$(gum input --placeholder "Host")
    DB_NAME=$(gum input --placeholder "Database name")
    DB_PORT=$(gum input --placeholder "Port")
    DB_USER=$(gum input --placeholder "User")
    DB_PASSWORD=$(gum input --placeholder "Password" --secret)
    
    # Save the inputs in .migration_info file
    echo "DB_HOST=$DB_HOST" > .migration_info
    echo "DB_NAME=$DB_NAME" >> .migration_info
    echo "DB_PORT=$DB_PORT" >> .migration_info
    echo "DB_USER=$DB_USER" >> .migration_info
    echo "DB_PASSWORD=$DB_PASSWORD" >> .migration_info
fi

# Ask user whether to create tables or run migrations
CHOICE=$(gum choose --header "Choose an option" "create_tables" "run_migrations")

if [ "$CHOICE" == "create_tables" ]; then
    # Running the tables.sql file to create tables
    run_sql_file "scripts/tables.sql"
else
    # Running migrations

    # Get the last migration that was executed
    LAST_MIGRATION=$(PGPASSWORD=${DB_PASSWORD} psql -h "${DB_HOST}" -p "${DB_PORT}" -d "${DB_NAME}" -U "${DB_USER}" -tAc "SELECT id FROM migrations ORDER BY executed_at DESC LIMIT 1;")
    
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
            PGPASSWORD=${DB_PASSWORD} psql -h "${DB_HOST}" -p "${DB_PORT}" -d "${DB_NAME}" -U "${DB_USER}" -c "INSERT INTO migrations (id) VALUES ('${MIGRATION_ID}');"
        fi
    done
fi

echo "Migration script completed."
