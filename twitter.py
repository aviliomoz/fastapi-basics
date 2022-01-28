from typing import List, Dict

from pysondb import db

from pydantic import BaseModel
from pydantic import Field

from fastapi import FastAPI
from fastapi import Path, Body
from fastapi import status

app = FastAPI()
database = db.getDb("database.json")

# Models
class Twit(BaseModel):
    text: str = Field(
        ..., 
        min_length=1, 
        max_length=100, 
        title="Twit", 
        description="Un twit simple", 
        example="Twit de prueba"
    )

# CRUD
@app.get(
    path="/twits",
    status_code=status.HTTP_200_OK,
    tags=["Twits"]
)
def get_twits():
    twits: List[Dict[str, str]] = database.getAll()
    return {
        "ok": True,
        "msg": "Todos los twits",
        "twits": twits
    }

@app.post(
    path="/twits",
    status_code=status.HTTP_201_CREATED,
    tags=["Twits"]
)
def create_twit(twit: Twit = Body(...)):
    """
    **Create Twit**

    This path operation creates a twit in the app and save the information in the database

    Parameters: 
    - Request body parameter: 
        - **twit: Twit** -> A twit model with text

    Returns a JSON object with the twit
    """
    database.add({"text": twit.text})
    return {
        "ok": True,
        "msg": "Twit creado con éxito",
        "twit": twit
    }

@app.put(
    path="/twits/{twit_id}",
    status_code=status.HTTP_200_OK,
    tags=["Twits"]
)
def update_twit(twit_id: int = Path(...), twit: Twit = Body(...)):
    database.updateById(twit_id, {"text": twit.text})
    return {
        "ok": True,
        "msg": "Twit modificado con éxito",
        "twit": twit
    }

@app.delete(
    path="/twits/{twit_id}",
    status_code=status.HTTP_200_OK,
    tags=["Twits"]
)
def delete_twit(twit_id: int = Path(...)):
    database.deleteById(twit_id)
    return {
        "ok": True,
        "msg": "Twit eliminado con éxito",
        "twit": twit_id
    }