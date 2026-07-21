from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
import uuid

app = FastAPI(
    title="User Auth API",
    description="A simple authentication service for user registration and login.",
    version="1.0.0",
)

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=6, description="Password (min 6 characters)")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Registered email address")
    password: str = Field(..., description="Account password")

class UserResponse(BaseModel):
    id: str = Field(..., description="Unique user ID")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")

class LoginResponse(BaseModel):
    message: str = Field(..., description="Status message")
    user: UserResponse = Field(..., description="Authenticated user details")

users: list[dict] = []

@app.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
    tags=["Auth"],
    summary="Register a new user",
    description="Create a new user account. Returns 400 if email or username already exists.",
)
def register(user: UserRegister):
    for u in users:
        if u["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
        if u["username"] == user.username:
            raise HTTPException(status_code=400, detail="Username already taken")

    new_user = {
        "id": str(uuid.uuid4()),
        "username": user.username,
        "email": user.email,
        "password": user.password,
    }
    users.append(new_user)
    return new_user

@app.post(
    "/login",
    response_model=LoginResponse,
    tags=["Auth"],
    summary="Log in an existing user",
    description="Authenticate with email and password. Returns user details on success or 401 on failure.",
)
def login(credentials: UserLogin):
    for u in users:
        if u["email"] == credentials.email and u["password"] == credentials.password:
            return {"message": "Login successful", "user": u}
    raise HTTPException(status_code=401, detail="Invalid email or password")

@app.get(
    "/users",
    response_model=list[UserResponse],
    tags=["Users"],
    summary="List all users",
    description="Return a list of all registered users.",
)
def list_users():
    return users

@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    tags=["Users"],
    summary="Get a user by ID",
    description="Fetch a single user's details using their unique ID. Returns 404 if not found.",
)
def get_user(user_id: str):
    for u in users:
        if u["id"] == user_id:
            return u
    raise HTTPException(status_code=404, detail="User not found")
