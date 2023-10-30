---
sidebar_position: 1
title: Architecture
---

Quivr is using FastAPI to provide a RESTful API for the backend. The API is currently in beta and is subject to change. The API is available at [https://api.quivr.app](https://api.quivr.app).

You can find the Swagger documentation for the API at [https://api.quivr.app/docs](https://api.quivr.app/docs).

## Overview

This documentation outlines the key points and usage instructions for interacting with the API backend. Please follow the guidelines below to use the backend services effectively.


## FastAPI

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. FastAPI is a class-based API framework that is built on top of Starlette and Pydantic. FastAPI is a great choice for building APIs because it is easy to use, fast, and has a lot of great features.

We decided to choose FastAPI because it is a modern, fast, and easy-to-use API framework. FastAPI is also very well documented and has a lot of great features that make it easy to build APIs. FastAPI is also very well supported by the community and has a lot of great features that make it easy to build APIs.


## Authentication

The API uses API keys for authentication. You can generate an API key by signing in to the frontend application and navigating to the `/config` page. The API key will be required to authenticate your requests to the backend.

When making requests to the backend API, include the following header:

```http
Authorization: Bearer {api_key}
```

Replace `{api_key}` with the generated API key obtained from the frontend

You can find more information in the [Authentication](/docs/backend/api/getting_started) section of the documentation.

