from fastapi import APIRouter
from pydantic import BaseModel
import json
import os

router = APIRouter()

RULES_FILE = "app/rules/rules.json"
SQL_FILE = "app/sql_templates.json"

class RuleBlock(BaseModel):
    id: str
    field: str
    operator: str
    value: str

class RuleGroup(BaseModel):
    id: str
    logic: str
    children: list  

class SaveRequest(BaseModel):
    rules: RuleGroup
    sql: str

@router.get("/rules/load")
def load_rules():
    if not os.path.exists(RULES_FILE):
        return {"rules": {"id": "root", "logic": "AND", "children": []}}
    with open(RULES_FILE, "r") as f:
        return {"rules": json.load(f)}

@router.post("/rules/save")
def save_rules(payload: SaveRequest):
    with open(RULES_FILE, "w") as f:
        json.dump(payload.rules.dict(), f, indent=2)

    if os.path.exists(SQL_FILE):
        with open(SQL_FILE, "r") as f:
            sql_map = json.load(f)
    else:
        sql_map = {}
    sql_map[payload.rules.id] = payload.sql
    with open(SQL_FILE, "w") as f:
        json.dump(sql_map, f, indent=2)

    return {"message": "Rules and SQL saved."}