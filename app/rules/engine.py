import pandas as pd
import json
import os

RULES_PATH = os.path.join(os.path.dirname(__file__), "rules.json")

def load_rules():
    with open(RULES_PATH, "r") as f:
        return json.load(f)

def evaluate_condition(row, rule):
    field = rule["field"]
    operator = rule["operator"]
    value = rule.get("value")
    cell = row.get(field)

    if operator == "NOT_NULL":
        return pd.notnull(cell)
    elif operator == "EQ":
        return cell == value
    elif operator == "NEQ":
        return cell != value
    elif operator == "GT":
        return cell > value
    elif operator == "LT":
        return cell < value
    elif operator == "IN":
        return cell in value if isinstance(value, list) else False
    elif operator == "BEFORE":
        return pd.to_datetime(cell) < pd.to_datetime(value)
    elif operator == "AFTER":
        return pd.to_datetime(cell) > pd.to_datetime(value)
    return False

def evaluate_group(row, group):
    logic = group["logic"]
    results = []

    for child in group["children"]:
        if "children" in child:
            result = evaluate_group(row, child)
        else:
            result = evaluate_condition(row, child)
        results.append(result)

    return all(results) if logic == "AND" else any(results)

def evaluate_rules_on_df(df: pd.DataFrame) -> pd.DataFrame:
    rules = load_rules()

    def eval_row(row):
        return evaluate_group(row, rules)

    df["passes_rule"] = df.apply(eval_row, axis=1)
    return df[["subject_id", "passes_rule"]]
