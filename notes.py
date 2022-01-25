from typing import List, Dict

from pysondb import db

from pydantic import BaseModel
from pydantic import Field

from fastapi import FastAPI
from fastapi import Path, Body

app = FastAPI()
database = db.getDb("database.json")

# Models
class Note(BaseModel):
    text: str = Field(
        ..., 
        min_length=1, 
        max_length=100, 
        title="Nota", 
        description="Una nota de texto simple", 
        example="Nota de prueba"
    )

# CRUD
@app.get(path="/notes")
def get_notes():
    notes: List[Dict[str, str]] = database.getAll()
    return {
        "ok": True,
        "msg": "Todas las notas",
        "notes": notes
    }

@app.post(path="/notes")
def create_note(note: Note = Body(...)):
    database.add({"text": note.text})
    return {
        "ok": True,
        "msg": "Nota creada con éxito",
        "note": note
    }

@app.put(path="/notes/{note_id}")
def update_note(note_id: int = Path(...), note: Note = Body(...)):
    database.updateById(note_id, {"text": note.text})
    return {
        "ok": True,
        "msg": "Nota modificada con éxito",
        "note": note
    }

@app.delete(path="/notes/{note_id}")
def delete_note(note_id: int = Path(...)):
    database.deleteById(note_id)
    return {
        "ok": True,
        "msg": "Nota eliminada con éxito",
        "note": note_id
    }