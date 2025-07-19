from pydantic import BaseModel
from typing import List, Union, Literal

class RuleBlock(BaseModel):
    id: str
    field: str
    operator: str
    value: str

class RuleGroup(BaseModel):
    id: str
    logic: Literal["AND", "OR"]
    children: List[Union["RuleBlock", "RuleGroup"]]

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "id": "group-1",
                "logic": "AND",
                "children": []
            }
        }

RuleGroup.update_forward_refs()

class RuleGroupWithSQL(BaseModel):
    rules: RuleGroup
    sql: str