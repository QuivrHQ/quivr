#!/bin/bash

# Set the project ID from environment variable
PROJECT_ID=$PROJECT_ID

# Run supabase link
supabase link --project-ref $PROJECT_ID

# Run supabase db push
supabase db push --linked

