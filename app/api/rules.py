# ✅ 1. app/api/rules.py – updated rule handling (including load)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os

router = APIRouter()

RULES_FILE = "rules.json"
SQL_TEMPLATES_FILE = "sql_templates.json"

class Rule(BaseModel):
    field: str
    operator: str
    value: str

class SQLTemplate(BaseModel):
    rule_id: str
    sql: str

@router.get("/rules")
async def get_rules():
    if not os.path.exists(RULES_FILE):
        return {"rules": []}
    with open(RULES_FILE, "r") as f:
        return {"rules": json.load(f)}

@router.post("/rules")
async def add_rules(rules: list[Rule]):
    with open(RULES_FILE, "w") as f:
        json.dump([rule.dict() for rule in rules], f, indent=2)
    return {"message": "Rules saved."}

@router.get("/rules/load")
async def load_rules():
    rules = []
    sql_templates = {}
    if os.path.exists(RULES_FILE):
        with open(RULES_FILE, "r") as f:
            rules = json.load(f)
    if os.path.exists(SQL_TEMPLATES_FILE):
        with open(SQL_TEMPLATES_FILE, "r") as f:
            sql_templates = json.load(f)
    return {"rules": rules, "sql_templates": sql_templates}

@router.post("/sql_templates")
async def save_sql_templates(payload: dict):
    with open(SQL_TEMPLATES_FILE, "w") as f:
        json.dump(payload, f, indent=2)
    return {"message": "SQL templates saved."}