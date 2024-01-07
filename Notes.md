Copy logs from a container to some file for analysis.

docker logs c67d7a8980a8 > backend_container_logs.txt 2>&1
docker logs 491601e9ad33 > worker_container_logs.txt 2>&1

# Size comparison:

Old:
quivr-backend-core   latest    056750d86247   2 minutes ago   13.4GB
New:
quivr-backend-core   latest    742c5d235313   15 hours ago    13.5GB

# Generating ANON_KEY and SERVICE_KEY for local supabase

https://supabase.com/docs/guides/self-hosting/docker#generate-api-keys

