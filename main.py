from typing import Optional
from enum import Enum

from pydantic import BaseModel
from pydantic import Field

from fastapi import FastAPI
from fastapi import Path, Query, Body, Form, Header, Cookie, File
from fastapi import UploadFile
from fastapi import HTTPException
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
@app.get(
    path="/", 
    status_code=status.HTTP_200_OK,
    tags=["Home"]
)
def home():
    return {
        "ok": True,
        "msg": "Home"
    }

# Path Parameter Example

users = [1, 2, 3, 4, 5]

@app.get(
    path="/users/{user_id}", 
    status_code=status.HTTP_200_OK,
    tags=["Users"]
)
def get_user_id(
    user_id: int = Path(
        ..., 
        title="User ID", 
        description="User Identification Number", 
        gt=1
    )
):
    if user_id not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return {
        "user_id": user_id
    }

# Query Parameter Example
@app.get(
    path="/users", 
    status_code=status.HTTP_200_OK,
    tags=["Users"]
)
def get_user_name(
    user_name: Optional[str] = Query(
        default=None, 
        min_length=1, 
        max_length=20
    )
):
    return {
        "user_name": user_name
    }

# Request Body Example
# Nota: al uzar response_model_exclude la respuesta debe ser directamente el Response Body y no un JSON
@app.post(
    path="/users/new", 
    response_model=Person, 
    response_model_exclude={"password"}, 
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
    summary="Create new user"
)
def create_user(
    new_user: Person = Body(...)
):
    """
    **Create Person**

    This path operation creates a person in the app and save the information in the database

    Parameters: 
    - Request body parameter: 
        - **person: Person** -> A person model with first name, last name, age, hair color and marital status

    Returns a person model with first name, last name, age, hair color and marital status
    """
    return new_user

# Form Parameter Example
@app.post(
    path="/login", 
    response_model=Login, 
    response_model_exclude={"password"}, 
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Users"]
)
def login(
    username = Form(...), 
    password = Form(...)
):
    return Login(username=username, password=password)

# Header and Cookie Parameters Example
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Contact"]
)
def contact(
    name: str = Form(...),
    last_name: str = Form(...),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

# File Parameters Example
@app.post(
    path="/images",
    status_code=status.HTTP_201_CREATED,
    tags=["Files"]
)
def upload_image(
    image: UploadFile = File(...) 
):
    return {
        "filename": image.filename,
        "format": image.content_type,
        "size(kb)": round(len(image.file.read()) / 1024, ndigits=2)
    }