---
sidebar_position: 2
title: Update a Brain
---

To update a brain, you need to make a PUT request to the following endpoint:

`/brains/{brain_id}/`

Replace `{brain_id}` with the unique identifier of the brain you want to update.

### Request Parameters

You should include the following parameters in the request:

- **brain_id**: The unique identifier (UUID) of the brain you want to update.

- **Authorization Header**: You must include a valid bearer token in the Authorization header to authenticate the request. This token can be obtained by following the authentication process.

- **Brain Update Data**: In the request body, you should provide the data you want to update for the brain. You can include the following optional fields:

  - **name**: The name of the brain.

  - **description**: A description of the brain.

  - **temperature**: The temperature setting for the brain.

  - **model**: The model used by the brain.

  - **max_tokens**: The maximum number of tokens for generated responses.

  - **openai_api_key**: An optional API key associated with the brain.

  - **status**: The status of the brain, which can be "public" or "private."

  - **prompt_id**: An optional UUID that associates the brain with a specific prompt.

### Example Request

```http
PUT /brains/{brain_id}/ HTTP/1.1
Host: your-api-host.com
Authorization: Bearer {your_access_token}
Content-Type: application/json

{
    "name": "Updated Brain Name",
    "description": "Updated brain description.",
    "temperature": 0.7,
    "model": "gpt-3.5-turbo",
    "max_tokens": 150,
    "openai_api_key": "your-api-key",
    "status": "private",
    "prompt_id": "123e4567-e89b-12d3-a456-426655440000"
}
```
