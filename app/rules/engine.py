import pandas as pd
import json
import os

RULES_PATH = os.path.join(os.path.dirname(__file__), "rules.json")

def load_rules():
    with open(RULES_PATH, "r") as f:
        return json.load(f)

def evaluate_condition(row, condition):
    field = condition["field"]
    value = row.get(field)
    op = condition["op"]

    if op == "NOT_NULL":
        return pd.notnull(value)
    elif op == "EQ":
        return value == condition.get("value")
    elif op == "NEQ":
        return value != condition.get("value")
    elif op == "IN":
        return value in condition.get("value", [])
    return False

def evaluate_rules_on_df(df: pd.DataFrame) -> pd.DataFrame:
    rules = load_rules()

    def eval_row(row):
        return all(evaluate_condition(row, cond) for cond in rules.get("and", []))

    df["passes_rule"] = df.apply(eval_row, axis=1)
    return df[["subject_id", "passes_rule"]]