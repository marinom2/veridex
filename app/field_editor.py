# app/field_editor.py
from fastapi import APIRouter
from pydantic import BaseModel
import json
import os

router = APIRouter()

FIELD_DEF_FILE = "field_definitions.json"

class FieldDefinition(BaseModel):
    name: str
    type: str  # e.g., "string", "date", "number"
    description: str | None = None

@router.get("/fields")
async def get_fields():
    if not os.path.exists(FIELD_DEF_FILE):
        return {"fields": []}
    with open(FIELD_DEF_FILE, "r") as f:
        return {"fields": json.load(f)}

@router.post("/fields")
async def add_field(field: FieldDefinition):
    fields = []
    if os.path.exists(FIELD_DEF_FILE):
        with open(FIELD_DEF_FILE, "r") as f:
            fields = json.load(f)
    fields.append(field.dict())
    with open(FIELD_DEF_FILE, "w") as f:
        json.dump(fields, f, indent=2)
    return {"message": "Field added"}

@router.delete("/fields/{field_name}")
async def delete_field(field_name: str):
    if not os.path.exists(FIELD_DEF_FILE):
        return {"message": "No fields to delete"}
    with open(FIELD_DEF_FILE, "r") as f:
        fields = json.load(f)
    fields = [f for f in fields if f["name"] != field_name]
    with open(FIELD_DEF_FILE, "w") as f:
        json.dump(fields, f, indent=2)
    return {"message": f"Field '{field_name}' deleted"}