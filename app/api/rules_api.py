from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
import os

from app.schemas.rule import RuleSaveRequest, SQLTemplateSaveRequest

router = APIRouter()

RULES_FILE = Path("rules.json")
SQL_FILE = Path("sql_templates.json")

@router.post("/rules/save")
async def save_rules(payload: RuleSaveRequest):
    try:
        with open(RULES_FILE, "w") as f:
            json.dump(payload.ruleGroup.dict(), f, indent=2)

        with open(SQL_FILE, "w") as f:
            json.dump({"sql_preview": payload.sqlPreview}, f, indent=2)

        return {"message": "Saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rules/load")
async def load_rules():
    try:
        rules = {}
        sql = {}
        if RULES_FILE.exists():
            with open(RULES_FILE, "r") as f:
                rules = json.load(f)
        if SQL_FILE.exists():
            with open(SQL_FILE, "r") as f:
                sql = json.load(f)
        return {"ruleGroup": rules, "sqlPreview": sql.get("sql_preview", "")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))