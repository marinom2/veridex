from pydantic import BaseModel
from typing import List, Union, Literal, Optional

class RuleBlock(BaseModel):
    id: str
    field: str
    operator: str
    value: str

class RuleGroup(BaseModel):
    id: str
    logic: Literal["AND", "OR"]
    children: List[Union["RuleBlock", "RuleGroup"]]

RuleGroup.update_forward_refs()

class SQLTemplateSaveRequest(BaseModel):
    sql: str

class RuleSaveRequest(BaseModel):
    ruleGroup: RuleGroup
    sqlPreview: str