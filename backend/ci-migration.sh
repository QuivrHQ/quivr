#!/bin/bash

echo "Setting the project ID from environment variable"
PROJECT_ID=$PROJECT_ID

echo "Setting the supabase token from environment variables"
SUPABASE_ACCESS_TOKEN=$SUPABASE_ACCESS_TOKEN 

echo "Setting the supabase db password from environment variable"
SUPABASE_DB_PASSWORD=$SUPABASE_DB_PASSWORD

echo "Logging in to supabase"
supabase login --token $SUPABASE_ACCESS_TOKEN

echo "Running supabase link"
supabase link --project-ref $PROJECT_ID --password $SUPABASE_DB_PASSWORD

echo "Running supabase db push"
supabase db push --linked --password $SUPABASE_DB_PASSWORD

