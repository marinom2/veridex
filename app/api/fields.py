# ✅ File: app/api/fields.py
from fastapi import APIRouter
from pydantic import BaseModel
import json
import os

router = APIRouter()

FIELDS_FILE = "fields.json"

class FieldDefinition(BaseModel):
    name: str
    label: str
    type: str  # e.g., "string", "date", "number"
    options: list[str] | None = None  # optional dropdown options

@router.get("/fields")
async def get_fields():
    if not os.path.exists(FIELDS_FILE):
        return {"fields": []}
    with open(FIELDS_FILE, "r") as f:
        return {"fields": json.load(f)}

@router.post("/fields")
async def add_field(field: FieldDefinition):
    fields = []
    if os.path.exists(FIELDS_FILE):
        with open(FIELDS_FILE, "r") as f:
            fields = json.load(f)
    fields.append(field.dict())
    with open(FIELDS_FILE, "w") as f:
        json.dump(fields, f, indent=2)
    return {"message": "Field added successfully"}