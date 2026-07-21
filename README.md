# Test-PR

A FastAPI-based user authentication service.

## Features

- **POST /register** — Register a new user (username, email, password). Returns 201 with user ID.
- **POST /login** — Authenticate with email and password. Returns user details on success.
- **GET /users** — List all registered users.
- **GET /users/{user_id}** — Retrieve a single user by ID.

Duplicate emails and usernames are rejected with a `400` error. Invalid login returns `401`.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

The API docs are available at `http://127.0.0.1:8000/docs`.

## Tech Stack

- Python
- FastAPI
- Pydantic (with email validation)
