#!/bin/bash

# Set the project ID from environment variable
PROJECT_ID=$PROJECT_ID

# Set the supabase token from environment variable
SUPABASE_ACCESS_TOKEN=$SUPABASE_ACCESS_TOKEN

# Login to supabase
supabase login --token $SUPABASE_ACCESS_TOKEN

# Run supabase link
supabase link --project-ref $PROJECT_ID

# Run supabase db push
supabase db push --linked

