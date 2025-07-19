import pandas as pd

def get_sample_data():
    return pd.DataFrame({
        "subject_id": ["SUBJ001", "SUBJ002", "SUBJ003"],
        "VISDAT": ["2025-01-10", "2025-01-12", None],
        "VISTYPE": ["On-Site", "Phone", "On-Site"],
        "DRUG": ["Mono", "Combo", "Mono"]
    })