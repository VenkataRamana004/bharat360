"""
Bharat360 Governance, Finance & Mobility Module.
Exposes render_governance_module() and supporting utilities.
"""

from .governance import render_governance_module
from .data_loader import (
    load_all_governance_data,
    load_government_schemes,
    load_financial_inclusion,
    load_transport,
)
from .recommender import (
    recommend_schemes,
    recommend_financial_resources,
    recommend_transport,
    get_personalized_recommendations,
)

__all__ = [
    "render_governance_module",
    "load_all_governance_data",
    "load_government_schemes",
    "load_financial_inclusion",
    "load_transport",
    "recommend_schemes",
    "recommend_financial_resources",
    "recommend_transport",
    "get_personalized_recommendations",
]
