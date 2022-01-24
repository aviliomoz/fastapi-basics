from typing import Optional
from enum import Enum

from pydantic import BaseModel
from pydantic import Field

from fastapi import FastAPI
from fastapi import Path, Query, Body, Form
from fastapi import status

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
    password: str = Field(..., min_length=5, example="123456")

class Login(BaseModel):
    username: str = Field(..., example="aviliomoz")
    password: str = Field(..., example="123456")

# Basic Path Operation
@app.get(path="/", status_code=status.HTTP_200_OK)
def home():
    return {
        "ok": True
    }

# Path Parameter Example
@app.get(path="/users/{user_id}", status_code=status.HTTP_200_OK)
def get_user_id(user_id: int = Path(..., title="User ID", description="User Identification Number", gt=1)):
    return {
        "user_id": user_id
    }

# Query Parameter Example
@app.get(path="/users", status_code=status.HTTP_200_OK)
def get_user_name(user_name: Optional[str] = Query(default=None, min_length=1, max_length=20)):
    return {
        "user_name": user_name
    }

# Request Body Example
# Nota: al uzar response_model_exclude la respuesta debe ser directamente el Response Body y no un JSON
@app.post(
        path="/users/new", 
        response_model=Person, 
        response_model_exclude={"password"}, 
        status_code=status.HTTP_201_CREATED
    )
def create_user(new_user: Person = Body(...)):
    return new_user

# Form Parameter Example
@app.post(
        path="/login", 
        response_model=Login, 
        response_model_exclude={"password"}, 
        status_code=status.HTTP_202_ACCEPTED
    )
def login(username = Form(...), password = Form(...)):
    return Login(username=username, password=password)