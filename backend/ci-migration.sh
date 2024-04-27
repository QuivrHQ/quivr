#!/bin/bash

echo "Setting the project ID from environment variable"
PROJECT_ID=$PROJECT_ID

echo "Setting the supabase token from environment variable"
SUPABASE_ACCESS_TOKEN=$SUPABASE_ACCESS_TOKEN

echo "Initializing supabase"
supabase init

echo "Logging in to supabase"
supabase login --token $SUPABASE_ACCESS_TOKEN

echo "Running supabase link"
supabase link --project-ref $PROJECT_ID

echo "Running supabase db push"
supabase db push --linked

