#!/bin/bash

# LOG_LEVEL=info rye run uvicorn quivr_api.main:app --log-level info --host 0.0.0.0 --port 5050 --workers 5 --loop uvloop
# supabase db reset && supabase stop && supabase start
# rm benchmarks/data.json
# rye run python benchmarks/load_data.py
LOG_LEVEL=info rye run uvicorn quivr_api.main:app --log-level info --host 0.0.0.0 --port 5050 --workers 5 --loop uvloop&
rye run locust -f benchmarks/locustfile_kms.py -H http://localhost:5050
