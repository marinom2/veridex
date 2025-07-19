from fastapi import APIRouter, HTTPException
from app.schemas.field import FieldDefinition
import json
import os
from pathlib import Path
from typing import List

router = APIRouter()
FIELDS_FILE = Path("fields.json")

@router.get("/fields", response_model=List[FieldDefinition])
async def get_fields():
    if not FIELDS_FILE.exists():
        return []
    with open(FIELDS_FILE, "r") as f:
        return json.load(f)

@router.post("/fields")
async def add_field(field: FieldDefinition):
    fields = []
    if FIELDS_FILE.exists():
        with open(FIELDS_FILE, "r") as f:
            fields = json.load(f)

    # Prevent duplicates by name
    if any(f["name"] == field.name for f in fields):
        raise HTTPException(status_code=400, detail="Field name already exists.")

    fields.append(field.dict())
    with open(FIELDS_FILE, "w") as f:
        json.dump(fields, f, indent=2)
    return {"message": "Field added successfully"}

@router.delete("/fields/{name}")
async def delete_field(name: str):
    if not FIELDS_FILE.exists():
        raise HTTPException(status_code=404, detail="No fields to delete from.")

    with open(FIELDS_FILE, "r") as f:
        fields = json.load(f)

    updated_fields = [f for f in fields if f["name"] != name]
    if len(fields) == len(updated_fields):
        raise HTTPException(status_code=404, detail="Field not found.")

    with open(FIELDS_FILE, "w") as f:
        json.dump(updated_fields, f, indent=2)
    return {"message": f"Field '{name}' deleted successfully"}