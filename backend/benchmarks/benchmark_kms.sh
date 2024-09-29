#!/bin/bash

# Function to handle cleanup on exit
cleanup() {
    echo "Cleaning up..."
    # Stop Uvicorn server if running
    if [[ ! -z "$UVICORN_PID" ]]; then
        kill "$UVICORN_PID"
        wait "$UVICORN_PID"
    fi
    exit 0
}

# Trap signals (like Ctrl+C, SIGTERM) to run the cleanup function
#trap cleanup SIGINT SIGTERM

# Reset and start Supabase
supabase db reset && supabase stop && supabase start

# Remove old benchmark data
rm -f benchmarks/data.json

# Load new data
rye run python benchmarks/load_data.py

# Start Uvicorn server in the background
LOG_LEVEL=info rye run uvicorn quivr_api.main:app --log-level info --host 0.0.0.0 --port 5050 --workers 5 --loop uvloop &
UVICORN_PID=$!

# Wait a bit to ensure the server is running
sleep 1

# Run Locust for benchmarking
rye run locust -f benchmarks/locustfile_kms.py -H http://localhost:5050 --processes 4

# Wait for all background processes (including Uvicorn) to finish
wait "$UVICORN_PID"
