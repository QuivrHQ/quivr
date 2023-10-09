---
sidebar_position: 1
title: Testing Strategies
---

## Backend

- E2E Test
  - User journeys
- Unit Test
  - Test base classes for models for breaking change (Vectorstore, Brainpicking, etc...)
  - Test endpoints
  - Test utility functions
  - Test critical functions
    - Chat related functions

How:

- Pytest

### 🐛 Debugging the backend

The backend is running in a docker container. To debug the backend, you can attach a debugger to the container. The debugger server runs on port `5678`. The backend is started in dev mode with `make dev`.

#### Debug with VSCode

The configuration for this is already set up in the `launch.json` file in the `.vscode` folder. After you started the project in dev mode with `make dev` you can run a debugging session using the `Python: Remote attach` configuration.

## Frontend

- Functional tests
  - Good rendering of components
  - Backend call is made
  - State is updated
  - User can interact with the component

How:

- Vitest
- RTL (React Testing Library)
