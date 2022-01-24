import json
import random
from typing import List, Dict

from pydantic import BaseModel
from pydantic import Field

from fastapi import FastAPI
from fastapi import Path, Body

app = FastAPI()

# Utils
def getNotes():
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        return data

def setNotes(data):
    with open("data.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data))

def getRandomID():
    id: str = str(random.randint(1,9)) + str(random.randint(1,9)) + str(random.randint(1,9))
    return id

# Models
class Note(BaseModel):
    id: str = Field(...)
    text: str = Field(
        ..., 
        min_length=1, 
        max_length=20, 
        title="text note", 
        description="a simple text note", 
        example="Nota de prueba"
    )

# CRUD
@app.get(path="/notes")
def get_notes():
    notes: List[Dict[str, str]] = getNotes()
    return notes

@app.post(path="/notes")
def create_note(note: Note = Body(...)):
    notes: List[Dict[str, str]] = getNotes()
    notes.append({"id": getRandomID(), "text": note.text})
    setNotes(notes)
    return notes

@app.put(path="/notes/{note_id}")
def update_note(note_id: str = Path(...), note: Note = Body(...)):
    notes: List[Dict[str, str]] = getNotes()
    notes = list(map(lambda n: {"id": n["id"], "text": note.text} if n["id"] == note_id else {"id": n["id"], "text": n["text"]}, notes))
    setNotes(notes)
    return notes

@app.delete(path="/notes/{note_id}")
def delete_note(note_id: str = Path(...)):
    notes: List[Dict[str, str]] = getNotes()
    notes = list(filter(lambda n: n["id"] != note_id, notes))
    setNotes(notes)
    return notes