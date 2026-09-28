"""
Data Loader for Education & Skills Module (Bharat360)
Member 1 - Education & Skills

Dynamically discovers, loads, and validates:
- education_institutions.csv
- scholarships.csv
- skill_programs.csv
"""

import os
from pathlib import Path
from typing import Dict, Optional, Tuple
import pandas as pd

# Safe streamlit import to allow caching when run inside Streamlit
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False


# Expected column schemas for resilient loading
EXPECTED_COLUMNS = {
    "education_institutions.csv": [
        "id", "name", "city", "state", "management", "type", "major_area"
    ],
    "scholarships.csv": [
        "id", "name", "eligibility", "level", "region", "benefit"
    ],
    "skill_programs.csv": [
        "id", "name", "level", "mode", "cost", "focus"
    ]
}


def get_candidate_data_dirs() -> list:
    """
    Returns candidate directories where the member1_education datasets might reside.
    Searches relative to the current working directory and relative to this file.
    """
    current_dir = Path(__file__).resolve().parent
    cwd = Path.cwd().resolve()

    candidates = [
        # Relative to project execution root
        cwd / "data" / "member1_education",
        cwd / "Bharat360_datasets" / "member1_education",
        cwd / "bharat360" / "data" / "member1_education",
        cwd / "bharat360" / "Bharat360_datasets" / "member1_education",
        
        # Relative to module location
        current_dir.parent.parent / "Bharat360_datasets" / "member1_education",
        current_dir.parent.parent / "data" / "member1_education",
        current_dir.parent.parent / "bharat360" / "Bharat360_datasets" / "member1_education",
        current_dir.parent / "data" / "member1_education",
    ]

    # Return unique paths maintaining order
    seen = set()
    unique_candidates = []
    for c in candidates:
        resolved = str(c.resolve())
        if resolved not in seen:
            seen.add(resolved)
            unique_candidates.append(c)
    return unique_candidates


def locate_file(filename: str) -> Optional[Path]:
    """
    Search for a specific dataset filename in known candidate locations.
    """
    for candidate_dir in get_candidate_data_dirs():
        target = candidate_dir / filename
        if target.exists() and target.is_file():
            return target
    return None


def _load_csv_safely(filename: str) -> pd.DataFrame:
    """
    Loads a single CSV file safely with schema validation, missing column filling,
    and graceful error handling.
    """
    expected_cols = EXPECTED_COLUMNS.get(filename, [])
    file_path = locate_file(filename)

    if file_path is None:
        if HAS_STREAMLIT:
            st.warning(f"⚠️ Dataset file '{filename}' was not found in standard directories. Using empty template.")
        return pd.DataFrame(columns=expected_cols)

    try:
        df = pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(file_path, encoding="latin1")
        except Exception as e:
            if HAS_STREAMLIT:
                st.error(f"❌ Error decoding '{filename}': {e}")
            return pd.DataFrame(columns=expected_cols)
    except Exception as e:
        if HAS_STREAMLIT:
            st.error(f"❌ Failed to load '{filename}': {e}")
        return pd.DataFrame(columns=expected_cols)

    # Validate and normalize columns (lowercase, strip whitespace)
    df.columns = [str(c).strip().lower() for c in df.columns]

    # Ensure all expected columns exist
    for col in expected_cols:
        if col not in df.columns:
            df[col] = ""

    # Clean string columns: fill NaN with empty strings and strip
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].fillna("").astype(str).str.strip()
        else:
            df[col] = df[col].fillna(0)

    return df


def load_institutions_data() -> pd.DataFrame:
    """Load and return the education institutions dataset."""
    return _load_csv_safely("education_institutions.csv")


def load_scholarships_data() -> pd.DataFrame:
    """Load and return the scholarships dataset."""
    return _load_csv_safely("scholarships.csv")


def load_skills_data() -> pd.DataFrame:
    """Load and return the skill programs dataset."""
    return _load_csv_safely("skill_programs.csv")


# Cache data in Streamlit if available for speed and smooth UX
if HAS_STREAMLIT:
    cached_institutions = st.cache_data(show_spinner=False)(load_institutions_data)
    cached_scholarships = st.cache_data(show_spinner=False)(load_scholarships_data)
    cached_skills = st.cache_data(show_spinner=False)(load_skills_data)
else:
    cached_institutions = load_institutions_data
    cached_scholarships = load_scholarships_data
    cached_skills = load_skills_data


def load_all_education_data() -> Dict[str, pd.DataFrame]:
    """
    Main helper to load all 3 education datasets dynamically.
    Returns:
        dict with keys: 'institutions', 'scholarships', 'skills'
    """
    return {
        "institutions": cached_institutions(),
        "scholarships": cached_scholarships(),
        "skills": cached_skills()
    }
