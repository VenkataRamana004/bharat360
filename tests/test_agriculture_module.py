"""
Unit and Integration Tests for Bharat360 Agriculture & Sustainability Module (Member 3).
Tests:
- Dynamic data loading
- Resiliency against missing files, empty files, duplicates, NaNs
- Rule-based irrigation recommender accuracy and grounding
- Smart agriculture holistic recommendations
- Render entry point export
"""

import sys
import unittest
from pathlib import Path
import pandas as pd

# Add repo root to sys.path
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.agriculture.data_loader import (
    load_crop_data,
    load_rainfall_data,
    load_irrigation_data,
    load_sustainability_data,
    load_all_agriculture_data,
    clean_dataframe,
    find_dataset_path,
)
from modules.agriculture.recommender import (
    recommend_irrigation,
    compute_smart_agriculture_recommendations,
    get_crop_profile,
    get_district_rainfall,
)
from modules.agriculture import render_agriculture_module


class TestAgricultureDataLoader(unittest.TestCase):
    """Test data loader functionality and edge cases."""

    def test_load_all_datasets_success(self):
        """Verify all 4 datasets are discovered and loaded without errors."""
        data = load_all_agriculture_data()
        self.assertTrue(data["all_loaded"], f"Failed to load datasets: {data.get('errors')}")
        self.assertEqual(len(data["errors"]), 0)

        # Check expected minimum rows and columns
        crop_df = data["crop_data"]
        self.assertGreaterEqual(len(crop_df), 5)
        for col in ["id", "crop", "season", "water_requirement", "input_requirement", "category"]:
            self.assertIn(col, crop_df.columns)

        rain_df = data["rainfall"]
        self.assertGreaterEqual(len(rain_df), 5)
        for col in ["id", "district", "state", "year", "annual_rainfall_mm"]:
            self.assertIn(col, rain_df.columns)

        irrig_df = data["irrigation"]
        self.assertGreaterEqual(len(irrig_df), 5)
        for col in ["id", "method", "water_efficiency", "cost_level", "suitable_for"]:
            self.assertIn(col, irrig_df.columns)

        sust_df = data["sustainability"]
        self.assertGreaterEqual(len(sust_df), 5)
        for col in ["id", "initiative", "impact_area", "potential_impact", "target_users"]:
            self.assertIn(col, sust_df.columns)

    def test_missing_file_handling(self):
        """Verify data loader handles non-existent file path gracefully."""
        df, err = load_crop_data(custom_path="non_existent_folder/missing_crop_data.csv")
        self.assertIsNotNone(err)
        self.assertTrue(df.empty)
        self.assertIn("crop", df.columns)

    def test_clean_dataframe_edge_cases(self):
        """Verify dirty data with spaces, NaNs, and duplicates is cleaned properly."""
        raw_data = {
            "id": [1, 2, 3, 4],
            "crop": [" Rice ", "Maize", " Rice ", None],
            "season": ["Kharif ", "Kharif", "Kharif", "Rabi"],
            "water_requirement": [" High", "Medium", " High", "Low"],
            "input_requirement": ["Medium", "Medium", "Medium", "Low"],
            "category": ["Paddy", "Cereal", "Paddy", "Oilseed"],
        }
        df_raw = pd.DataFrame(raw_data)
        cleaned = clean_dataframe(df_raw, ["id", "crop", "season", "water_requirement", "input_requirement", "category"])
        
        # Leading/trailing whitespace should be trimmed
        rice_rows = cleaned[cleaned["crop"] == "Rice"]
        self.assertEqual(len(rice_rows), 1, "Duplicate Rice row should have been dropped")
        self.assertEqual(cleaned.loc[cleaned["crop"] == "Rice", "water_requirement"].iloc[0], "High")


class TestAgricultureRecommender(unittest.TestCase):
    """Test recommendation engine logic and grounding."""

    @classmethod
    def setUpClass(cls):
        data = load_all_agriculture_data()
        cls.crop_df = data["crop_data"]
        cls.rainfall_df = data["rainfall"]
        cls.irrigation_df = data["irrigation"]
        cls.sustainability_df = data["sustainability"]

    def test_irrigation_recommendation_rice(self):
        """Verify Canal Irrigation or high-capacity system is recommended for Rice."""
        rec = recommend_irrigation(
            crop_name="Rice",
            water_availability="High",
            preference="Balanced / Any",
            crop_df=self.crop_df,
            irrigation_df=self.irrigation_df,
        )
        top = rec["top_method"]
        self.assertIsNotNone(top)
        self.assertEqual(top["method"], "Canal Irrigation")
        self.assertIn("Rice", top["suitable_for"])
        self.assertIn("Canal Irrigation", rec["reason"])

    def test_irrigation_recommendation_chilli_efficiency(self):
        """Verify Drip Irrigation is recommended for Chilli with Efficiency-First."""
        rec = recommend_irrigation(
            crop_name="Chilli",
            water_availability="Low",
            preference="Efficiency-First",
            crop_df=self.crop_df,
            irrigation_df=self.irrigation_df,
        )
        top = rec["top_method"]
        self.assertIsNotNone(top)
        self.assertEqual(top["method"], "Drip Irrigation")
        self.assertEqual(top["water_efficiency"], "High")

    def test_smart_agriculture_high_stress(self):
        """Verify high water stress is detected for Sugarcane in low rainfall / low availability."""
        res = compute_smart_agriculture_recommendations(
            crop_name="Sugarcane",
            district_name="Guntur",  # Lowest rainfall (860 mm)
            water_availability="Low",
            irrigation_preference="Efficiency-First",
            crop_df=self.crop_df,
            rainfall_df=self.rainfall_df,
            irrigation_df=self.irrigation_df,
            sustainability_df=self.sustainability_df,
        )
        stress = res["water_stress"]
        self.assertEqual(stress["level"], "High Water Stress")
        self.assertIn("Sugarcane", stress["description"])

        # Check factors table
        factors = res["factors_table"]
        self.assertEqual(len(factors), 5)
        factor_names = [f["Factor"] for f in factors]
        self.assertIn("Selected Crop", factor_names)
        self.assertIn("District Rainfall", factor_names)
        self.assertIn("Water Availability", factor_names)
        self.assertIn("Irrigation Preference", factor_names)
        self.assertIn("Sustainability Options", factor_names)

    def test_district_rainfall_retrieval(self):
        """Verify district comparison calculations."""
        kakinada = get_district_rainfall(self.rainfall_df, "Kakinada")
        self.assertIsNotNone(kakinada)
        self.assertEqual(kakinada["annual_rainfall_mm"], 1180)
        self.assertEqual(kakinada["rainfall_status"], "Above Average")
        self.assertGreater(kakinada["rainfall_diff_pct"], 0)


class TestModuleExport(unittest.TestCase):
    """Test module exposure."""

    def test_render_function_exported(self):
        self.assertTrue(callable(render_agriculture_module))


if __name__ == "__main__":
    unittest.main()
