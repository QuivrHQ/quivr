from datetime import datetime, timedelta

# -- Create a table called "stats"
# create table
#   stats (
#     -- A column called "time" with data type "timestamp"
#     time timestamp,
#     -- A column called "details" with data type "text"
#     chat boolean,
#     embedding boolean,
#     details text,
#     metadata jsonb,
#     -- An "integer" primary key column called "id" that is generated always as identity
#     id integer primary key generated always as identity
#   );


def get_usage_today(supabase):
    # Returns the number of rows in the stats table for the last 24 hours
    response = supabase.table("stats").select("id", count="exact").gte("time", datetime.now() - timedelta(hours=24)).execute()
    return response.count

def add_usage(supabase, type, details, metadata):
    # Adds a row to the stats table
    supabase.table("stats").insert({
        "time": datetime.now().isoformat(),
        "chat": type == "chat",
        "embedding": type == "embedding",
        "details": details,
        "metadata": metadata
    }).execute()
