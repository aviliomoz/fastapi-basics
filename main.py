from typing import Optional
from enum import Enum

from pydantic import BaseModel
from pydantic import Field

from fastapi import FastAPI
from fastapi import Path, Query, Body

app = FastAPI()

# Types
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    red = "red"
    blonde = "blonde"

# Models
class Person(BaseModel):
    name: str = Field(..., min_length=1, max_length=10, example="Avilio")
    age: int = Field(..., ge=0, example=26)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

# Basic Path Operation
@app.get("/")
def home():
    return {
        "ok": True
    }

# Path Parameter Example
@app.get("/users/{user_id}")
def get_user_id(user_id: int = Path(..., title="User ID", description="User Identification Number", gt=1)):
    return {
        "user_id": user_id
    }

# Query Parameter Example
@app.get("/users")
def get_user_name(user_name: Optional[str] = Query(default=None, min_length=1, max_length=20)):
    return {
        "user_name": user_name
    }

# Request Body Example
@app.post("/users/new")
def create_user(new_user: Person = Body(...)):
    return {
        "msg": "New user created",
        "user": new_user
    }