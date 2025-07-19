from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os

router = APIRouter()

TEMPLATES_FILE = os.path.join(os.path.dirname(__file__), "../sql_templates.json")

class SQLTemplate(BaseModel):
    rule_id: str
    sql: str

@router.get("/sql_templates")
async def get_templates():
    if not os.path.exists(TEMPLATES_FILE):
        return {"templates": []}
    with open(TEMPLATES_FILE, "r") as f:
        return {"templates": json.load(f)}

@router.post("/sql_templates")
async def save_template(template: SQLTemplate):
    templates = []
    if os.path.exists(TEMPLATES_FILE):
        with open(TEMPLATES_FILE, "r") as f:
            templates = json.load(f)

    # Replace existing rule_id if exists
    templates = [t for t in templates if t["rule_id"] != template.rule_id]
    templates.append(template.dict())

    with open(TEMPLATES_FILE, "w") as f:
        json.dump(templates, f, indent=2)
    return {"message": "SQL template saved"}

@router.delete("/sql_templates/{rule_id}")
async def delete_template(rule_id: str):
    if not os.path.exists(TEMPLATES_FILE):
        raise HTTPException(status_code=404, detail="No templates found.")
    with open(TEMPLATES_FILE, "r") as f:
        templates = json.load(f)
    templates = [t for t in templates if t["rule_id"] != rule_id]
    with open(TEMPLATES_FILE, "w") as f:
        json.dump(templates, f, indent=2)
    return {"message": "SQL template deleted"}