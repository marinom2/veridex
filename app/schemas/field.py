# app/schemas/field.py

from pydantic import BaseModel
from typing import Optional, Literal

class FieldDefinition(BaseModel):
    name: str
    label: str
    type: str  # "string", "number", "date"
    options: Optional[list[str]] = None
