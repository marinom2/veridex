from pydantic import BaseModel
from typing import List, Union


class RuleBlock(BaseModel):
    id: str
    field: str
    operator: str
    value: Union[str, int, float]


class RuleGroup(BaseModel):
    id: str
    logic: str  # "AND" / "OR"
    children: List[Union["RuleGroup", RuleBlock]]


# Needed for recursive models
RuleGroup.update_forward_refs()


class RuleSaveRequest(BaseModel):
    ruleGroup: RuleGroup
    sqlPreview: str


class SQLTemplateSaveRequest(BaseModel):
    rule_id: str
    sql: str