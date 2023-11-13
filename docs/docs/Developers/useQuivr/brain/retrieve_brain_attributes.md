---
sidebar_position: 4
title: Get a Brain
---

To get a brain, you need to make a GET request to the following endpoints.

### Retrieve a Specific Brain by ID

To retrieve details of a specific brain by its ID, make a GET request to the following endpoint:

```http
GET /brains/{brain_id}/
```

### Retrieve the Default Brain

When working with the default brain for the current user, you can make a GET request to the following endpoint:

```http
GET /brains/default/
```
