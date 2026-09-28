"""
data_loader.py
Dynamic and robust data loader for the Bharat360 Governance, Finance & Mobility Module.
Loads:
- government_schemes.csv
- financial_inclusion.csv
- transport.csv
Handles missing files, empty datasets, missing values, and column normalization.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import streamlit as st


# Expected column schemas for data integrity verification
SCHEMES_COLUMNS = ["id", "scheme", "category", "target_group", "benefit"]
FINANCIAL_COLUMNS = ["id", "service", "area", "target_group", "purpose"]
TRANSPORT_COLUMNS = ["id", "mode", "city", "state", "service_type", "purpose"]

SCHEMES_FILENAME = "government_schemes.csv"
FINANCIAL_FILENAME = "financial_inclusion.csv"
TRANSPORT_FILENAME = "transport.csv"
MEMBER4_DIRNAME = "member4_governance_finance_mobility"


def find_dataset_file(filename: str) -> Optional[Path]:
    """
    Dynamically locate a CSV dataset file across multiple search paths.
    Ensures portability whether running from repo root, parent directory, or nested module.
    """
    candidate_paths: List[Path] = []

    # 1. Search relative to this file's location
    current_file_dir = Path(__file__).resolve().parent
    for parent in [current_file_dir, current_file_dir.parent, current_file_dir.parent.parent, current_file_dir.parent.parent.parent]:
        candidate_paths.append(parent / "Bharat360_datasets" / MEMBER4_DIRNAME / filename)
        candidate_paths.append(parent / "bharat360" / "Bharat360_datasets" / MEMBER4_DIRNAME / filename)
        candidate_paths.append(parent / filename)

    # 2. Search relative to current working directory
    cwd = Path.cwd().resolve()
    for base in [cwd, cwd.parent, cwd / "bharat360"]:
        candidate_paths.append(base / "Bharat360_datasets" / MEMBER4_DIRNAME / filename)
        candidate_paths.append(base / "bharat360" / "Bharat360_datasets" / MEMBER4_DIRNAME / filename)
        candidate_paths.append(base / filename)

    for path in candidate_paths:
        try:
            if path.is_file() and path.stat().st_size > 0:
                return path
        except (PermissionError, OSError):
            continue

    # 3. Fallback: recursive glob search within 3 levels of cwd
    try:
        for found in cwd.glob(f"**/{filename}"):
            if found.is_file() and found.stat().st_size > 0:
                return found
    except Exception:
        pass

    return None


def _clean_dataframe(df: pd.DataFrame, expected_columns: List[str]) -> pd.DataFrame:
    """
    Clean, strip, and validate DataFrame columns and missing values.
    """
    if df.empty:
        return pd.DataFrame(columns=expected_columns)

    # Normalize column names: strip whitespace, lowercase
    df.columns = [str(col).strip().lower() for col in df.columns]

    # Ensure all expected columns exist
    for col in expected_columns:
        if col not in df.columns:
            df[col] = "Not Specified"

    # Fill NaN and strip whitespace on string columns
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].fillna("Not Specified").astype(str).str.strip()

    # Reorder to keep expected columns first
    ordered_cols = [c for c in expected_columns if c in df.columns] + [
        c for c in df.columns if c not in expected_columns
    ]
    return df[ordered_cols]


def load_csv_safely(filename: str, expected_columns: List[str]) -> Tuple[pd.DataFrame, Optional[str]]:
    """
    Load a CSV file with full error handling.
    Returns (DataFrame, error_message_or_None).
    """
    filepath = find_dataset_file(filename)
    if filepath is None:
        empty_df = pd.DataFrame(columns=expected_columns)
        err = f"Dataset file '{filename}' could not be located in standard search paths."
        return empty_df, err

    try:
        df = pd.read_csv(filepath)
        if df.empty or len(df.columns) == 0:
            return pd.DataFrame(columns=expected_columns), f"Dataset file '{filename}' was found at '{filepath}', but contains no records."

        cleaned_df = _clean_dataframe(df, expected_columns)
        return cleaned_df, None
    except Exception as exc:
        empty_df = pd.DataFrame(columns=expected_columns)
        return empty_df, f"Error reading '{filename}' from '{filepath}': {str(exc)}"


@st.cache_data(show_spinner=False)
def load_government_schemes() -> Tuple[pd.DataFrame, Optional[str]]:
    """Cached loader for government_schemes.csv."""
    return load_csv_safely(SCHEMES_FILENAME, SCHEMES_COLUMNS)


@st.cache_data(show_spinner=False)
def load_financial_inclusion() -> Tuple[pd.DataFrame, Optional[str]]:
    """Cached loader for financial_inclusion.csv."""
    return load_csv_safely(FINANCIAL_FILENAME, FINANCIAL_COLUMNS)


@st.cache_data(show_spinner=False)
def load_transport() -> Tuple[pd.DataFrame, Optional[str]]:
    """Cached loader for transport.csv."""
    return load_csv_safely(TRANSPORT_FILENAME, TRANSPORT_COLUMNS)


def load_all_governance_data() -> Dict[str, Any]:
    """
    Unified loader for all three datasets with aggregated health check status.
    Returns:
        dict: {
            "schemes": pd.DataFrame,
            "financial": pd.DataFrame,
            "transport": pd.DataFrame,
            "errors": List[str],
            "is_valid": bool
        }
    """
    schemes_df, schemes_err = load_government_schemes()
    fin_df, fin_err = load_financial_inclusion()
    trans_df, trans_err = load_transport()

    errors = [e for e in [schemes_err, fin_err, trans_err] if e]

    return {
        "schemes": schemes_df,
        "financial": fin_df,
        "transport": trans_df,
        "errors": errors,
        "is_valid": len(errors) == 0,
    }
