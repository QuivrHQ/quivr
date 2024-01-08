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

# create supabase user:

```
if CREATE_FIRST_USER := os.getenv("CREATE_FIRST_USER", "False").lower() == "true":
    try:
        from supabase import create_client

        supabase_client_auth = create_client(
            os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY")
        )
        res = supabase_client_auth.from_('users').select('*').eq('email', "admin@quivr.app").execute()
        if len(res.data) == 0:
            supabase_client_auth.auth.admin.create_user({"email": "admin@quivr.app","email_confirm": True, "password": "admin"})
            logger.info("👨‍💻 Created first user")
        else:
            logger.info("👨‍💻 First user already exists")
    except Exception as e:
        logger.error("👨‍💻 Error while creating first user")
        logger.error(e)
```

# Gum Installation

https://github.com/charmbracelet/gum

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://repo.charm.sh/apt/gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/charm.gpg
echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *" | sudo tee /etc/apt/sources.list.d/charm.list
sudo apt update && sudo apt install gum
```

# Docker stuff

docker stop $(docker ps -aq)
docker rm $(docker ps -aq)