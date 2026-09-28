"""
Data Loader Module for Bharat360 Healthcare & Public Services.
Dynamically loads and cleans datasets:
- hospitals.csv
- health_services.csv
- health_awareness.csv

Handles missing files, empty data, corrupted rows, and missing values gracefully.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
import pandas as pd
import streamlit as st

logger = logging.getLogger(__name__)

# Expected column schemas
HOSPITAL_COLUMNS = [
    "id", "name", "city", "state", "management", "type", "latitude", "longitude"
]
SERVICE_COLUMNS = [
    "id", "service", "description", "available_at", "cost_category"
]
AWARENESS_COLUMNS = [
    "id", "topic", "guidance", "target_group"
]


def resolve_dataset_directory() -> Path:
    """
    Locates the dataset directory dynamically across different execution contexts:
    - Running from repository root
    - Running from modules directory
    - Running from parent workspace directory
    """
    candidate_paths = [
        # Relative to this file: modules/healthcare/ -> bharat360/Bharat360_datasets/member2_healthcare
        Path(__file__).resolve().parent.parent.parent / "Bharat360_datasets" / "member2_healthcare",
        # If modules is at root of workspace:
        Path(__file__).resolve().parent.parent / "Bharat360_datasets" / "member2_healthcare",
        # Current working directory paths
        Path.cwd() / "bharat360" / "Bharat360_datasets" / "member2_healthcare",
        Path.cwd() / "Bharat360_datasets" / "member2_healthcare",
        Path.cwd() / "member2_healthcare",
        # Hard fallback to known project path
        Path(r"C:\Users\Salad\OneDrive\Desktop\BHRATH 360\bharat360\Bharat360_datasets\member2_healthcare")
    ]

    for candidate in candidate_paths:
        if candidate.exists() and candidate.is_dir():
            return candidate

    # Return the first plausible path even if missing so error handling can report it cleanly
    return candidate_paths[0]


def get_dataset_file_path(filename: str) -> Optional[Path]:
    """Finds the absolute path to a specific dataset CSV file."""
    base_dir = resolve_dataset_directory()
    target = base_dir / filename
    if target.exists() and target.is_file():
        return target

    # Fallback search in parent tree if not found in base_dir
    search_roots = [Path.cwd(), Path(__file__).resolve().parent.parent.parent]
    for root in search_roots:
        matches = list(root.rglob(filename))
        if matches:
            return matches[0]

    return None


@st.cache_data(show_spinner=False)
def load_hospitals_data(csv_path: Optional[str] = None) -> Tuple[pd.DataFrame, Optional[str]]:
    """
    Loads and cleans hospitals.csv.
    Returns (cleaned_dataframe, error_message).
    """
    file_path = Path(csv_path) if csv_path else get_dataset_file_path("hospitals.csv")
    
    if not file_path or not file_path.exists():
        msg = f"hospitals.csv not found at expected location ({file_path or 'unknown'})."
        logger.warning(msg)
        return pd.DataFrame(columns=HOSPITAL_COLUMNS), msg

    try:
        df = pd.read_csv(file_path, encoding="utf-8-sig")
    except Exception as e:
        msg = f"Error reading hospitals.csv: {e}"
        logger.error(msg)
        return pd.DataFrame(columns=HOSPITAL_COLUMNS), msg

    if df.empty:
        return pd.DataFrame(columns=HOSPITAL_COLUMNS), "hospitals.csv is empty."

    # Normalize column names
    df.columns = [str(c).strip().lower() for c in df.columns]

    # Ensure all expected columns exist
    for col in HOSPITAL_COLUMNS:
        if col not in df.columns:
            df[col] = None

    # Clean string columns
    str_cols = ["name", "city", "state", "management", "type"]
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()
        df.loc[df[col].isin(["nan", "None", ""].copy()), col] = "Unknown"

    # Numeric coordinates handling
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    # Deduplicate
    df = df.drop_duplicates(subset=["name", "city", "state"]).reset_index(drop=True)

    return df, None


@st.cache_data(show_spinner=False)
def load_health_services_data(csv_path: Optional[str] = None) -> Tuple[pd.DataFrame, Optional[str]]:
    """
    Loads and cleans health_services.csv.
    Returns (cleaned_dataframe, error_message).
    """
    file_path = Path(csv_path) if csv_path else get_dataset_file_path("health_services.csv")

    if not file_path or not file_path.exists():
        msg = f"health_services.csv not found at expected location ({file_path or 'unknown'})."
        logger.warning(msg)
        return pd.DataFrame(columns=SERVICE_COLUMNS), msg

    try:
        df = pd.read_csv(file_path, encoding="utf-8-sig")
    except Exception as e:
        msg = f"Error reading health_services.csv: {e}"
        logger.error(msg)
        return pd.DataFrame(columns=SERVICE_COLUMNS), msg

    if df.empty:
        return pd.DataFrame(columns=SERVICE_COLUMNS), "health_services.csv is empty."

    df.columns = [str(c).strip().lower() for c in df.columns]

    for col in SERVICE_COLUMNS:
        if col not in df.columns:
            df[col] = "Not Specified"

    for col in ["service", "description", "available_at", "cost_category"]:
        df[col] = df[col].astype(str).str.strip()
        df.loc[df[col].isin(["nan", "None", ""]), col] = "Not Specified"

    df = df.drop_duplicates(subset=["service", "available_at"]).reset_index(drop=True)
    return df, None


@st.cache_data(show_spinner=False)
def load_health_awareness_data(csv_path: Optional[str] = None) -> Tuple[pd.DataFrame, Optional[str]]:
    """
    Loads and cleans health_awareness.csv.
    Returns (cleaned_dataframe, error_message).
    """
    file_path = Path(csv_path) if csv_path else get_dataset_file_path("health_awareness.csv")

    if not file_path or not file_path.exists():
        msg = f"health_awareness.csv not found at expected location ({file_path or 'unknown'})."
        logger.warning(msg)
        return pd.DataFrame(columns=AWARENESS_COLUMNS), msg

    try:
        df = pd.read_csv(file_path, encoding="utf-8-sig")
    except Exception as e:
        msg = f"Error reading health_awareness.csv: {e}"
        logger.error(msg)
        return pd.DataFrame(columns=AWARENESS_COLUMNS), msg

    if df.empty:
        return pd.DataFrame(columns=AWARENESS_COLUMNS), "health_awareness.csv is empty."

    df.columns = [str(c).strip().lower() for c in df.columns]

    for col in AWARENESS_COLUMNS:
        if col not in df.columns:
            df[col] = "General"

    for col in ["topic", "guidance", "target_group"]:
        df[col] = df[col].astype(str).str.strip()
        df.loc[df[col].isin(["nan", "None", ""]), col] = "General"

    df = df.drop_duplicates(subset=["topic", "target_group"]).reset_index(drop=True)
    return df, None


def load_all_healthcare_data() -> Dict[str, any]:
    """
    Loads all 3 healthcare datasets and aggregates any warnings or errors.
    """
    df_hospitals, err_hosp = load_hospitals_data()
    df_services, err_serv = load_health_services_data()
    df_awareness, err_aware = load_health_awareness_data()

    errors = [e for e in [err_hosp, err_serv, err_aware] if e is not None]

    return {
        "hospitals": df_hospitals,
        "services": df_services,
        "awareness": df_awareness,
        "errors": errors,
        "dataset_dir": str(resolve_dataset_directory())
    }


# Helper filtering extractors
def get_unique_states(df: pd.DataFrame) -> List[str]:
    """Returns sorted unique states from hospitals dataframe."""
    if df.empty or "state" not in df.columns:
        return []
    states = [s for s in df["state"].dropna().unique() if s and s != "Unknown"]
    return sorted(states)


def get_unique_cities(df: pd.DataFrame, state: Optional[str] = None) -> List[str]:
    """Returns sorted unique cities, optionally filtered by state."""
    if df.empty or "city" not in df.columns:
        return []
    filtered = df if not state or state == "All States" else df[df["state"].str.lower() == state.lower()]
    cities = [c for c in filtered["city"].dropna().unique() if c and c != "Unknown"]
    return sorted(cities)


def get_unique_managements(df: pd.DataFrame) -> List[str]:
    """Returns sorted unique hospital management categories."""
    if df.empty or "management" not in df.columns:
        return []
    mgmt = [m for m in df["management"].dropna().unique() if m and m != "Unknown"]
    return sorted(mgmt)


def get_unique_hospital_types(df: pd.DataFrame) -> List[str]:
    """Returns sorted unique hospital types."""
    if df.empty or "type" not in df.columns:
        return []
    types = [t for t in df["type"].dropna().unique() if t and t != "Unknown"]
    return sorted(types)


def get_unique_cost_categories(df: pd.DataFrame) -> List[str]:
    """Returns sorted unique cost categories from services dataframe."""
    if df.empty or "cost_category" not in df.columns:
        return []
    costs = [c for c in df["cost_category"].dropna().unique() if c and c != "Not Specified"]
    return sorted(costs)
