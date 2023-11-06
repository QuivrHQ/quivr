---
sidebar_position: 2
title: Install Quivr
---

# Prerequisites 📋

Before you begin, make sure you have the following tools and accounts installed and set up:

- Docker
- Docker Compose
- A Supabase account with:
  - A new Supabase project
  - Supabase Project API key
  - Supabase Project URL

## Installation Steps 💽

Follow these steps to install and set up the Quivr project:

### Step 0: Installation Video (Optional)

If needed, you can watch the installation process on YouTube [here](https://www.youtube.com/watch?v=rC-s4QdfY80&feature=youtu.be).

### Step 1: Clone the Repository

Use one of the following commands to clone the Quivr repository:

- If you don't have an SSH key set up:

  ```
  git clone https://github.com/StanGirard/Quivr.git
  cd Quivr
  ```

- If you have an SSH key set up or want to add it (guide [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)):

  ```
  git clone git@github.com:StanGirard/Quivr.git
  cd Quivr
  ```

### Step 2: Use the Install Helper Script

Run the install_helper.sh script to automate the setup process. This script will help you set up your environment files and execute the necessary migrations. Ensure you have the following prerequisites installed:

```bash
  brew install gum # Windows (via Scoop) scoop install charm-gum
  brew install postgresql # Windows (via Scoop) scoop install postgresql
```

```bash
chmod +x install_helper.sh
./install_helper.sh
```

If you prefer manual setup, you can follow the steps below.

### Step 2 - Additional Configuration: Copy Environment Files

Copy the environment files as follows:

- Copy .backend_env.example to backend/.env
- Copy .frontend_env.example to frontend/.env

### Step 3: Update Environment Variables

Edit the backend/.env and frontend/.env files with the following information:

- `supabase_service_key`: Found in your Supabase dashboard under Project Settings -> API (Use the anon public key from the Project API keys section).
- `JWT_SECRET_KEY`: Found in your Supabase settings under Project Settings -> API -> JWT Settings -> JWT Secret.
- `NEXT_PUBLIC_BACKEND_URL`: Set to localhost:5050 for Docker. Update if your backend is running on a different machine.

### Step 4: Run Migration Scripts

Run the migration.sh script to execute the migration scripts. You have two options:

- `Create all tables`: For the first-time setup.
- `Run migrations`: When updating your database.

You can also run the script on the Supabase database via the web interface (SQL Editor -> New query -> paste the script -> Run). All migration scripts can be found in the scripts folder.

If you're migrating from an old version of Quivr, run the scripts in the migration script to update your data in chronological order.

### Step 5: Launch the Application

Run the following command to launch the application:

```
docker compose -f docker-compose.dev.yml up --build
```

### Step 6: Navigate to localhost:3000 in your browser

Open your web browser and navigate to [localhost:3000](http://localhost:3000).
