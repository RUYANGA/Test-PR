# Test-PR

A FastAPI-based user registration service.

## Features

- **POST /register** — Register a new user (username, email, password). Returns 201 with user ID.
- **GET /users** — List all registered users.
- **GET /users/{user_id}** — Retrieve a single user by ID.

Duplicate emails and usernames are rejected with a `400` error.

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
