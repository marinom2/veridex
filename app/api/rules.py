from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os
from datetime import datetime
from app.schemas.rule import RuleGroupWithSQL

router = APIRouter()

RULES_FILE = "rules.json"
VERSION_DIR = "rule_versions"

# --- Utility Functions ---

def load_rules_file():
    if os.path.exists(RULES_FILE):
        with open(RULES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_rules_file(data):
    with open(RULES_FILE, "w") as f:
        json.dump(data, f, indent=2)

def save_versioned_copy(data):
    os.makedirs(VERSION_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    version_path = os.path.join(VERSION_DIR, f"rules_{timestamp}.json")
    with open(version_path, "w") as f:
        json.dump(data, f, indent=2)
    return version_path

# --- Endpoints ---

@router.get("/rules/load")
async def load_rules():
    try:
        data = load_rules_file()
        return {"rules": data.get("rules", {})}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load rules: {e}")

@router.post("/rules/save")
async def save_rules(payload: RuleGroupWithSQL):
    try:
        data = {
            "rules": payload.rules,
            "sql": payload.sql
        }
        save_rules_file(data)
        version_path = save_versioned_copy(data)
        return {
            "message": "✅ Rules and SQL saved",
            "versioned_copy": version_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save rules: {e}")

@router.delete("/rules/reset")
async def delete_rules():
    try:
        if os.path.exists(RULES_FILE):
            os.remove(RULES_FILE)
            return {"message": "🗑️ Rules file deleted"}
        else:
            raise HTTPException(status_code=404, detail="Rules file not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete rules: {e}")