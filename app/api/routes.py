from fastapi import APIRouter, UploadFile, File
import pandas as pd
from app.rules.engine import evaluate_rules_on_df

router = APIRouter()

@router.post("/run-rule/")
async def run_rule(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    result = evaluate_rules_on_df(df)
    return result.to_dict(orient="records")