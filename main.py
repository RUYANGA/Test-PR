from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import uuid

app = FastAPI()

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str

users: list[dict] = []

@app.post("/register", response_model=UserResponse, status_code=201)
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

@app.get("/users", response_model=list[UserResponse])
def list_users():
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    for u in users:
        if u["id"] == user_id:
            return u
    raise HTTPException(status_code=404, detail="User not found")
