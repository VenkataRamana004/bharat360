"""
Data Loader for Bharat360 Agriculture & Sustainability Module.
Dynamically resolves dataset locations, handles missing files, empty datasets,
duplicates, and missing values gracefully with caching.
"""

from pathlib import Path
import logging
from typing import Dict, Optional, Tuple
import pandas as pd
import streamlit as st

logger = logging.getLogger(__name__)

# Primary expected file names
DATASET_FILES = {
    "crop_data": "crop_data.csv",
    "rainfall": "rainfall.csv",
    "irrigation": "irrigation.csv",
    "sustainability": "sustainability.csv",
}

# Expected schemas for validation and graceful empty fallbacks
SCHEMAS = {
    "crop_data": ["id", "crop", "season", "water_requirement", "input_requirement", "category"],
    "rainfall": ["id", "district", "state", "year", "annual_rainfall_mm"],
    "irrigation": ["id", "method", "water_efficiency", "cost_level", "suitable_for"],
    "sustainability": ["id", "initiative", "impact_area", "potential_impact", "target_users"],
}


def find_dataset_path(filename: str) -> Optional[Path]:
    """
    Search dynamically for the dataset file across potential repository directories.
    Avoids hardcoding fixed machine-specific paths.
    """
    candidate_roots = [
        Path.cwd(),
        Path(__file__).resolve().parent,
        Path(__file__).resolve().parents[1],
        Path(__file__).resolve().parents[2],
    ]

    relative_subdirs = [
        Path("Bharat360_datasets/member3_agriculture"),
        Path("Bharat360_datasets"),
        Path("datasets/member3_agriculture"),
        Path("datasets"),
        Path("data"),
        Path("modules/agriculture/data"),
        Path("."),
    ]

    for root in candidate_roots:
        for subdir in relative_subdirs:
            candidate = (root / subdir / filename).resolve()
            if candidate.exists() and candidate.is_file():
                return candidate

    return None


def clean_dataframe(df: pd.DataFrame, expected_columns: list) -> pd.DataFrame:
    """
    Cleans a loaded dataframe:
    - Strips whitespace from string columns and column names
    - Ensures expected columns exist
    - Removes duplicates
    - Drops completely empty rows
    """
    if df.empty:
        return pd.DataFrame(columns=expected_columns)

    # Clean column names
    df.columns = [str(col).strip() for col in df.columns]

    # Ensure missing expected columns are present with None
    for col in expected_columns:
        if col not in df.columns:
            df[col] = None

    # Drop entirely empty rows
    df = df.dropna(how="all")

    # Strip whitespaces from string cells
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()
            # Replace 'nan' string with empty or sensible placeholder
            df[col] = df[col].replace({"nan": None, "None": None, "": None})

    # Drop duplicate records based on all non-id columns if possible
    subset_cols = [c for c in expected_columns if c != "id" and c in df.columns]
    if subset_cols:
        df = df.drop_duplicates(subset=subset_cols, keep="first")
    else:
        df = df.drop_duplicates(keep="first")

    return df.reset_index(drop=True)


@st.cache_data(show_spinner=False)
def load_crop_data(custom_path: Optional[str] = None) -> Tuple[pd.DataFrame, Optional[str]]:
    """Load and clean crop_data.csv dynamically."""
    path = Path(custom_path) if custom_path else find_dataset_path(DATASET_FILES["crop_data"])
    if not path or not path.exists():
        err = f"crop_data.csv not found in candidate paths."
        return pd.DataFrame(columns=SCHEMAS["crop_data"]), err

    try:
        df = pd.read_csv(path)
        df = clean_dataframe(df, SCHEMAS["crop_data"])
        return df, None
    except Exception as e:
        logger.error(f"Error loading {path}: {e}")
        return pd.DataFrame(columns=SCHEMAS["crop_data"]), f"Error reading crop_data: {str(e)}"


@st.cache_data(show_spinner=False)
def load_rainfall_data(custom_path: Optional[str] = None) -> Tuple[pd.DataFrame, Optional[str]]:
    """Load and clean rainfall.csv dynamically."""
    path = Path(custom_path) if custom_path else find_dataset_path(DATASET_FILES["rainfall"])
    if not path or not path.exists():
        err = f"rainfall.csv not found in candidate paths."
        return pd.DataFrame(columns=SCHEMAS["rainfall"]), err

    try:
        df = pd.read_csv(path)
        df = clean_dataframe(df, SCHEMAS["rainfall"])
        if "annual_rainfall_mm" in df.columns:
            df["annual_rainfall_mm"] = pd.to_numeric(df["annual_rainfall_mm"], errors="coerce").fillna(0)
        return df, None
    except Exception as e:
        logger.error(f"Error loading {path}: {e}")
        return pd.DataFrame(columns=SCHEMAS["rainfall"]), f"Error reading rainfall: {str(e)}"


@st.cache_data(show_spinner=False)
def load_irrigation_data(custom_path: Optional[str] = None) -> Tuple[pd.DataFrame, Optional[str]]:
    """Load and clean irrigation.csv dynamically."""
    path = Path(custom_path) if custom_path else find_dataset_path(DATASET_FILES["irrigation"])
    if not path or not path.exists():
        err = f"irrigation.csv not found in candidate paths."
        return pd.DataFrame(columns=SCHEMAS["irrigation"]), err

    try:
        df = pd.read_csv(path)
        df = clean_dataframe(df, SCHEMAS["irrigation"])
        return df, None
    except Exception as e:
        logger.error(f"Error loading {path}: {e}")
        return pd.DataFrame(columns=SCHEMAS["irrigation"]), f"Error reading irrigation: {str(e)}"


@st.cache_data(show_spinner=False)
def load_sustainability_data(custom_path: Optional[str] = None) -> Tuple[pd.DataFrame, Optional[str]]:
    """Load and clean sustainability.csv dynamically."""
    path = Path(custom_path) if custom_path else find_dataset_path(DATASET_FILES["sustainability"])
    if not path or not path.exists():
        err = f"sustainability.csv not found in candidate paths."
        return pd.DataFrame(columns=SCHEMAS["sustainability"]), err

    try:
        df = pd.read_csv(path)
        df = clean_dataframe(df, SCHEMAS["sustainability"])
        return df, None
    except Exception as e:
        logger.error(f"Error loading {path}: {e}")
        return pd.DataFrame(columns=SCHEMAS["sustainability"]), f"Error reading sustainability: {str(e)}"


def load_all_agriculture_data() -> Dict[str, any]:
    """
    Convenience loader that loads all four agriculture datasets.
    Returns a unified dict containing DataFrames, file statuses, and diagnostic info.
    """
    crop_df, crop_err = load_crop_data()
    rain_df, rain_err = load_rainfall_data()
    irrig_df, irrig_err = load_irrigation_data()
    sust_df, sust_err = load_sustainability_data()

    errors = [e for e in [crop_err, rain_err, irrig_err, sust_err] if e]

    return {
        "crop_data": crop_df,
        "rainfall": rain_df,
        "irrigation": irrig_df,
        "sustainability": sust_df,
        "errors": errors,
        "all_loaded": len(errors) == 0,
        "diagnostics": {
            "crop_rows": len(crop_df),
            "rainfall_rows": len(rain_df),
            "irrigation_rows": len(irrig_df),
            "sustainability_rows": len(sust_df),
        }
    }
