from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os

router = APIRouter()
FIELDS_FILE = "fields.json"

class FieldDefinition(BaseModel):
    name: str
    label: str
    type: str  # "string", "date", "number"
    options: list[str] | None = None  # optional dropdown

def load_fields():
    if os.path.exists(FIELDS_FILE):
        with open(FIELDS_FILE, "r") as f:
            return json.load(f)
    return []

def save_fields(fields):
    with open(FIELDS_FILE, "w") as f:
        json.dump(fields, f, indent=2)

@router.get("/fields")
async def get_fields():
    return {"fields": load_fields()}

@router.post("/fields")
async def add_field(field: FieldDefinition):
    fields = load_fields()
    if any(f["name"] == field.name for f in fields):
        raise HTTPException(status_code=400, detail=f"Field '{field.name}' already exists.")
    fields.append(field.dict())
    save_fields(fields)
    return {"message": f"✅ Field '{field.name}' added successfully"}

@router.delete("/fields/{name}")
async def delete_field(name: str):
    fields = load_fields()
    updated_fields = [f for f in fields if f["name"] != name]
    if len(fields) == len(updated_fields):
        raise HTTPException(status_code=404, detail=f"Field '{name}' not found.")
    save_fields(updated_fields)
    return {"message": f"🗑️ Field '{name}' deleted successfully"}