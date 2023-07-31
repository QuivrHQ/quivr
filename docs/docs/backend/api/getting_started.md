---
sidebar_position: 1
---

# How to use the API

**URL**: https://api.quivr.app

**Swagger**: https://api.quivr.app/docs

## Overview

This documentation outlines the key points and usage instructions for interacting with the API backend. Please follow the guidelines below to use the backend services effectively.

## Usage Instructions

1. Standalone Backend

   - The backend can now be used independently without the frontend application.
   - Users can interact with the API endpoints directly using API testing tools like Postman.

2. Generating API Key

   - To access the backend services, you need to sign in to the frontend application.
   - Once signed in, navigate to the `/user` page to generate a new API key.
   - The API key will be required to authenticate your requests to the backend.

3. Authenticating Requests

   - When making requests to the backend API, include the following header:
     - `Authorization: Bearer {api_key}`
     - Replace `{api_key}` with the generated API key obtained from the frontend.

4. Future Plans

   - The development team has plans to introduce additional features and improvements.
   - These include the ability to delete API keys and view the list of active keys.
   - The GitHub roadmap will provide more details on upcoming features, including addressing active issues.

5. API Key Expiration
   - Each API key has a daily expiration.
   - The expiration is based on Coordinated Universal Time (UTC) to avoid timezone issues.
   - After the expiration time, typically at midnight UTC, you will need to regenerate the API key to continue using the backend services.
   - Once the capability to delete keys is implemented, you will have the option to delete keys manually.

Please refer to the official GitHub repository and the project roadmap for more information and updates on the backend services.
