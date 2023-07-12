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

# Frontend

- Functional tests
  - Good rendering of components
  - Backend call is made
  - State is updated
  - User can interact with the component

How:
- Vitest
- RTL (React Testing Library)
