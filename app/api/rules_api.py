from fastapi import APIRouter, HTTPException
import json
from pathlib import Path

router = APIRouter()

RULES_FILE = Path("rules.json")
SQL_TEMPLATE_FILE = Path("sql_templates.json")

@router.post("/rules/save")
def save_rules(data: dict):
    try:
        rules = data.get("rules")
        sql = data.get("sql")
        with open(RULES_FILE, "w") as f:
            json.dump({"rules": rules}, f)
        if sql:
            with open(SQL_TEMPLATE_FILE, "w") as f:
                json.dump({"sql": sql}, f)
        return {"status": "saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/rules/load")
def load_rules():
    try:
        if RULES_FILE.exists():
            with open(RULES_FILE) as f:
                return json.load(f)
        return {"rules": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))