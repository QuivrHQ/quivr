---
sidebar_position: 1
title: Install on your Server
---

# Quivr Installation Guide on Ubuntu 22 Server

Welcome to the installation guide for Quivr, your go-to open-source project . This tutorial will walk you through the process of setting up Quivr on an Ubuntu 22.04 server with Docker and Traefik, ensuring a secure HTTPS connection for your domains.

## Table of Contents

- [Quivr Installation Guide on Ubuntu 22 Server](#quivr-installation-guide-on-ubuntu-22-server)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Step-by-Step Installation](#step-by-step-installation)
    - [Step 1: Clone Quivr Repository](#step-1-clone-quivr-repository)
    - [Step 2: Create `.env` File](#step-2-create-env-file)
    - [Step 3: Configure `.env` Files for Backend and Frontend](#step-3-configure-env-files-for-backend-and-frontend)
    - [Step 4: Launch Quivr with Docker Compose](#step-4-launch-quivr-with-docker-compose)
    - [Step 5: Verify Installation](#step-5-verify-installation)
  - [Additional Information](#additional-information)

## Prerequisites

Before diving into the installation process, please ensure you have the following ready:

- An **Ubuntu 22.04 server** with at least **20 GB of free disk space**.
- **Docker** installed. If you haven't done this yet, no worries! Follow the official [Docker Installation Guide for Ubuntu](https://docs.docker.com/engine/install/ubuntu/).
- **DNS records** configured to point to your server. You will need records for the following:
  - `flower.api.yourdomain`
  - `api.yourdomain`
  - `yourdomain`

> Replace `<yourdomain>` with your actual domain name throughout this guide. This domain also could be a subdomain like `bot.<yourdomain>.com`. In this case in your DNS configuration make sure that `bot.<yourdomain.com>` is also pointing to the IP address of your server, like you did with "flower.api" and "api".

## Step-by-Step Installation

### Step 1: Clone Quivr Repository

Let's get started by cloning the Quivr repository onto your server. Open your terminal and run:

```bash
git clone https://github.com/StanGirard/quivr.git
cd quivr
```

### Step 2: Create `.env` File

Now, let's set up your environment variables. In the root directory of the Quivr project, create a `.env` file:

```bash
nano .env
```

Add the following lines, making sure to replace the placeholders with your information:

```
EMAIL=your-email@example.com
DOMAIN_NAME=yourdomain.com
API_DOMAIN_NAME=api.yourdomain.com
```

note: in this file if you used a subdomain, DOMAIN_NAME would be `bot.<yourdomain.com>` and API_DOMAIN_NAME would be `api.<yourdomain.com>`

Don't forget to save your changes (`Ctrl+X`, then `Y`, and `Enter`).

### Step 3: Configure `.env` Files for Backend and Frontend

Next, configure the `backend/.env` and `frontend/.env` files as per the Quivr documentation. You'll fill in various settings specific to your setup.

### Step 4: Launch Quivr with Docker Compose

With your `.env` files ready, it's time to start up Quivr using Docker Compose. This step is exciting because it's when things come to life!

```bash
docker-compose -f docker-compose.local.yml up
```

The `docker-compose.local.yml` file includes **Traefik**, which automagically handles HTTPS certificates for you.

### Step 5: Verify Installation

Once everything is up and running, give yourself a pat on the back and verify that the services are accessible:

- Visit `https://yourdomain.com` or `https://bot.yourdomain.com`
- And `https://api.yourdomain.com`

You should be greeted by your new Quivr setup, all shiny and secure!

## Additional Information

- **Firewall Settings**: Ensure that ports 80 (HTTP) and 443 (HTTPS) are open. Traefik will handle the rest, including redirecting HTTP to HTTPS for you.
- **Updates**: Keep an eye on the [Quivr GitHub repository](https://github.com/StanGirard/quivr) for any updates to maintain security and performance.

> Always use HTTPS for production environments to ensure the security of your data and communications.

**Congratulations!** Your Quivr server should now be successfully installed and secured with HTTPS. Happy project managing!
