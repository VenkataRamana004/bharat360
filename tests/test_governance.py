"""
test_governance.py
Automated tests for Bharat360 Governance, Finance & Mobility Module.
Tests:
- Dynamic data loading & error resiliency (missing files, empty files)
- Transparent rule-based recommender engine
- Explainable recommendation outputs
- Module export and integration readiness
"""

import unittest
import pandas as pd

from modules.governance.data_loader import (
    load_all_governance_data,
    load_government_schemes,
    load_financial_inclusion,
    load_transport,
    load_csv_safely,
    SCHEMES_COLUMNS,
    FINANCIAL_COLUMNS,
    TRANSPORT_COLUMNS,
)
from modules.governance.recommender import (
    recommend_schemes,
    recommend_financial_resources,
    recommend_transport,
    get_personalized_recommendations,
)
from modules.governance import render_governance_module


class TestDataLoader(unittest.TestCase):
    """Test data loading and graceful degradation."""

    def test_load_all_governance_data(self):
        data = load_all_governance_data()
        self.assertIn("schemes", data)
        self.assertIn("financial", data)
        self.assertIn("transport", data)
        self.assertIn("errors", data)
        self.assertIn("is_valid", data)

        # Datasets should have records
        self.assertFalse(data["schemes"].empty)
        self.assertFalse(data["financial"].empty)
        self.assertFalse(data["transport"].empty)
        self.assertEqual(len(data["errors"]), 0)
        self.assertTrue(data["is_valid"])

    def test_schema_columns(self):
        schemes, _ = load_government_schemes()
        for col in SCHEMES_COLUMNS:
            self.assertIn(col, schemes.columns)

        fin, _ = load_financial_inclusion()
        for col in FINANCIAL_COLUMNS:
            self.assertIn(col, fin.columns)

        trans, _ = load_transport()
        for col in TRANSPORT_COLUMNS:
            self.assertIn(col, trans.columns)

    def test_missing_file_graceful_handling(self):
        df, err = load_csv_safely("non_existent_file.csv", ["col1", "col2"])
        self.assertTrue(df.empty)
        self.assertListEqual(list(df.columns), ["col1", "col2"])
        self.assertIsNotNone(err)
        self.assertIn("could not be located", err)


class TestRecommenderEngine(unittest.TestCase):
    """Test explainable rule-based matching."""

    def setUp(self):
        self.data = load_all_governance_data()

    def test_farmer_profile_recommendations(self):
        profile = {
            "age": 42,
            "state": "Andhra Pradesh",
            "city": "Kakinada",
            "occupation": "Farmer / Agriculture",
            "interest": "Agriculture",
        }
        recs = get_personalized_recommendations(
            profile,
            self.data["schemes"],
            self.data["financial"],
            self.data["transport"],
        )

        top_scheme = recs["top_scheme"]
        self.assertIsNotNone(top_scheme)
        self.assertEqual(top_scheme["title"], "PM-KISAN")
        self.assertGreaterEqual(top_scheme["score"], 80)
        self.assertTrue(any("farmer" in r.lower() or "agriculture" in r.lower() for r in top_scheme["reasons"]))

        top_fin = recs["top_financial"]
        self.assertIsNotNone(top_fin)
        self.assertEqual(top_fin["title"], "Basic Bank Account")

        top_trans = recs["top_transport"]
        self.assertIsNotNone(top_trans)
        self.assertIn("Kakinada", top_trans["title"])

    def test_student_profile_recommendations(self):
        profile = {
            "age": 21,
            "state": "Andhra Pradesh",
            "city": "Vijayawada",
            "occupation": "Student / Youth",
            "interest": "Skills and employment",
        }
        recs = get_personalized_recommendations(
            profile,
            self.data["schemes"],
            self.data["financial"],
            self.data["transport"],
        )

        top_scheme = recs["top_scheme"]
        self.assertEqual(top_scheme["title"], "Skill India")
        self.assertTrue(any("youth" in r.lower() or "skill" in r.lower() for r in top_scheme["reasons"]))

        top_trans = recs["top_transport"]
        self.assertIn("Vijayawada", top_trans["title"])

    def test_entrepreneur_profile_recommendations(self):
        profile = {
            "age": 32,
            "state": "Andhra Pradesh",
            "city": "Visakhapatnam",
            "occupation": "Small Business Owner / Entrepreneur",
            "interest": "Financial inclusion",
        }
        recs = get_personalized_recommendations(
            profile,
            self.data["schemes"],
            self.data["financial"],
            self.data["transport"],
        )

        top_fin = recs["top_financial"]
        self.assertIn(top_fin["title"], ["Microcredit Awareness", "Digital Payments"])
        self.assertTrue(any("business" in r.lower() or "credit" in r.lower() or "upi" in r.lower() for r in top_fin["reasons"]))

    def test_empty_dataframe_resilience(self):
        empty_df = pd.DataFrame(columns=SCHEMES_COLUMNS)
        recs = recommend_schemes({"age": 30}, empty_df)
        self.assertEqual(recs, [])


class TestModuleExport(unittest.TestCase):
    """Test module public interface."""

    def test_render_function_exists(self):
        self.assertTrue(callable(render_governance_module))


if __name__ == "__main__":
    unittest.main()
