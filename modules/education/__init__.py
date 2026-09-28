"""
Education & Skills Module Package for Bharat360
Member 1 - Education & Skills
"""

from .education import render_education_module
from .data_loader import (
    load_all_education_data,
    load_institutions_data,
    load_scholarships_data,
    load_skills_data,
)
from .recommender import (
    get_personalized_recommendations,
    recommend_institutions,
    recommend_scholarships,
    recommend_skill_programs,
)

__all__ = [
    "render_education_module",
    "load_all_education_data",
    "load_institutions_data",
    "load_scholarships_data",
    "load_skills_data",
    "get_personalized_recommendations",
    "recommend_institutions",
    "recommend_scholarships",
    "recommend_skill_programs",
]
