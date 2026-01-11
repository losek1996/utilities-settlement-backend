from datetime import date

import pandas as pd


def replace_nan_with_none(obj: dict) -> dict:
    return {k: None if pd.isna(v) else v for k, v in obj.items()}


def extract_date_str_from_filename(filename: str) -> str:
    """Returned format is YYYY-MM-DD."""
    date_parts = filename.split("_")[:-3]
    year = int(date_parts[0])
    month = int(date_parts[1])
    day = int(date_parts[2])
    return f"{year}-{month}-{day}"
