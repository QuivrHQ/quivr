#!/bin/sh

# Function to print error message and exit
error_exit() {
    echo "$1" >&2
    exit 1
}

# Function to replace variables in files
replace_in_file() {
    local file="$1"
    local search="$2"
    local replace="$3"
    if [ "$(uname)" = "Darwin" ]; then
        # macOS
        sed -i "" "s|${search}|${replace}|" "$file"
    else
        # Linux/Unix and Windows (Git Bash)
        sed -i "s|${search}|${replace}|" "$file"
    fi
}

# Step 2: Copy the .XXXXX_env files if they don't exist
if [ ! -f backend/.env ]; then
    echo "Copying backend-core .env example file..."
    cp .backend_env.example backend/.env
fi

if [ ! -f frontend/.env ]; then
    echo "Copying frontend .env example file..."
    cp .frontend_env.example frontend/.env
fi

# Step 3: Ask the user for environment variables and update .env files
# only if they haven't been set.

# Update backend/.env
if grep -q "SUPABASE_URL=<change-me>" backend/.env; then
    echo "SUPABASE_URL can be found in your Supabase dashboard under Settings > API."
    SUPABASE_URL=$(gum input --placeholder "Enter SUPABASE_URL for backend")
    replace_in_file backend/.env "SUPABASE_URL=.*" "SUPABASE_URL=${SUPABASE_URL}"
fi

if grep -q "SUPABASE_SERVICE_KEY=<change-me>" backend/.env; then
    echo "SUPABASE_SERVICE_KEY can be found in your Supabase dashboard under Settings > API. Use the anon public key found in the Project API keys section."
    SUPABASE_SERVICE_KEY=$(gum input --placeholder "Enter SUPABASE_SERVICE_KEY for backend")
    replace_in_file backend/.env "SUPABASE_SERVICE_KEY=.*" "SUPABASE_SERVICE_KEY=${SUPABASE_SERVICE_KEY}"
fi

if grep -q "PG_DATABASE_URL=<change-me>" backend/.env; then
    echo "PG_DATABASE_URL can be found in your Postgres provider Settings > API."
    PG_DATABASE_URL=$(gum input --placeholder "Enter PG_DATABASE_URL for backend")
    replace_in_file backend/.env "PG_DATABASE_URL=.*" "PG_DATABASE_URL=${PG_DATABASE_URL}"
fi

if grep -q "OPENAI_API_KEY=<change-me>" backend/.env; then
    echo "OPENAI_API_KEY is the API key from OpenAI, if you are using OpenAI services."
    OPENAI_API_KEY=$(gum input --placeholder "Enter OPENAI_API_KEY for backend")
    replace_in_file backend/.env "OPENAI_API_KEY=.*" "OPENAI_API_KEY=${OPENAI_API_KEY}"
fi

if grep -q "JWT_SECRET_KEY=<change-me>" backend/.env; then
    echo "JWT_SECRET_KEY can be found in your Supabase project dashboard under Settings > API > JWT Settings > JWT Secret."
    JWT_SECRET_KEY=$(gum input --placeholder "Enter JWT_SECRET_KEY for backend")
    replace_in_file backend/.env "JWT_SECRET_KEY=.*" "JWT_SECRET_KEY=${JWT_SECRET_KEY}"
fi

# Update frontend/.env using the same SUPABASE_URL and SUPABASE_SERVICE_KEY
if grep -q "NEXT_PUBLIC_SUPABASE_URL=<change-me>" frontend/.env; then
    replace_in_file frontend/.env "NEXT_PUBLIC_SUPABASE_URL=.*" "NEXT_PUBLIC_SUPABASE_URL=${SUPABASE_URL}"
fi

if grep -q "NEXT_PUBLIC_SUPABASE_ANON_KEY=<change-me>" frontend/.env; then
    replace_in_file frontend/.env "NEXT_PUBLIC_SUPABASE_ANON_KEY=.*" "NEXT_PUBLIC_SUPABASE_ANON_KEY=${SUPABASE_SERVICE_KEY}"
fi

# Step 4: Run the migration scripts (this is supposed to be done manually as per the instructions)
echo "Running the migration scripts..."
./migration.sh || error_exit "Error running migration scripts."

# Step 5: Launch the app
echo "Launching the app..."
docker compose up --build || error_exit "Error running docker compose."

# Final message
echo "Navigate to localhost:3000 in your browser to access the app."
