# app/rule_editor.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os

router = APIRouter()

RULES_FILE = os.path.join(os.path.dirname(__file__), "../rules.json")
SQL_TEMPLATES_FILE = os.path.join(os.path.dirname(__file__), "../sql_templates.json")

class RuleBlock(BaseModel):
    id: str
    field: str
    operator: str
    value: str

class RuleGroup(BaseModel):
    id: str
    logic: str  
    children: list 

class RulePayload(BaseModel):
    ruleGroup: RuleGroup
    sqlPreview: str

@router.post("/rules/save")
async def save_rule_group(payload: RulePayload):
    with open(RULES_FILE, "w") as f:
        json.dump(payload.ruleGroup.dict(), f, indent=2)

    with open(SQL_TEMPLATES_FILE, "w") as f:
        json.dump({"sql_preview": payload.sqlPreview}, f, indent=2)

    return {"message": "Saved successfully"}

@router.get("/rules/load")
async def load_rule_group():
    if not os.path.exists(RULES_FILE):
        return {"ruleGroup": None}
    with open(RULES_FILE, "r") as f:
        rule_group = json.load(f)
    return {"ruleGroup": rule_group}