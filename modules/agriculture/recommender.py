"""
Rule-Based Recommendation Engine for Bharat360 Agriculture & Sustainability Module.
Grounds all irrigation, crop management, and sustainability recommendations
strictly in the provided dataset attributes without invented agricultural claims.
"""

from typing import Dict, Any, List, Optional
import pandas as pd


def get_crop_profile(crop_df: pd.DataFrame, crop_name: str) -> Optional[Dict[str, Any]]:
    """Retrieve the row data for a specific crop."""
    if crop_df.empty or "crop" not in crop_df.columns:
        return None
    match = crop_df[crop_df["crop"].astype(str).str.lower() == str(crop_name).lower()]
    if not match.empty:
        return match.iloc[0].to_dict()
    return None


def get_district_rainfall(rainfall_df: pd.DataFrame, district_name: str) -> Optional[Dict[str, Any]]:
    """Retrieve rainfall data and district context relative to the dataset."""
    if rainfall_df.empty or "district" not in rainfall_df.columns:
        return None
    match = rainfall_df[rainfall_df["district"].astype(str).str.lower() == str(district_name).lower()]
    if match.empty:
        return None

    row = match.iloc[0].to_dict()
    avg_rainfall = rainfall_df["annual_rainfall_mm"].mean() if "annual_rainfall_mm" in rainfall_df.columns else 1000
    rainfall_val = float(row.get("annual_rainfall_mm", 0))
    diff = rainfall_val - avg_rainfall
    diff_pct = (diff / avg_rainfall * 100) if avg_rainfall else 0

    return {
        **row,
        "state_avg_rainfall_mm": round(avg_rainfall, 1),
        "rainfall_diff_mm": round(diff, 1),
        "rainfall_diff_pct": round(diff_pct, 1),
        "rainfall_status": "Above Average" if diff >= 0 else "Below Average",
    }


def recommend_irrigation(
    crop_name: str,
    water_availability: str,
    preference: str = "Balanced / Any",
    crop_df: Optional[pd.DataFrame] = None,
    irrigation_df: Optional[pd.DataFrame] = None,
) -> Dict[str, Any]:
    """
    Transparent, rule-based irrigation recommendation.
    Evaluates methods in irrigation.csv against:
    - Crop suitability (from 'suitable_for' column)
    - Local water availability ('Low', 'Medium', 'High')
    - Farmer preference ('Efficiency-First', 'Low Cost', 'Supplemental / Storage', 'Balanced / Any')
    """
    if irrigation_df is None or irrigation_df.empty:
        return {
            "top_method": None,
            "ranked_methods": [],
            "reason": "Irrigation dataset is unavailable.",
            "factors_used": {},
        }

    crop_info = get_crop_profile(crop_df, crop_name) if crop_df is not None else {}
    crop_clean = str(crop_name).strip().lower()
    crop_category = str(crop_info.get("category", "")).lower() if crop_info else ""
    water_req = str(crop_info.get("water_requirement", "Medium")).lower() if crop_info else "medium"
    water_avail = str(water_availability).strip().lower()
    pref = str(preference).strip().lower()

    scored_methods: List[Dict[str, Any]] = []

    for _, row in irrigation_df.iterrows():
        method_name = str(row.get("method", "")).strip()
        water_eff = str(row.get("water_efficiency", "")).strip().capitalize()
        cost_lvl = str(row.get("cost_level", "")).strip().capitalize()
        suitable_for = str(row.get("suitable_for", "")).strip()
        suit_lower = suitable_for.lower()

        score = 0
        explanations = []

        # 1. Crop Suitability Match (Max 45 pts)
        if crop_clean and crop_clean in suit_lower:
            score += 45
            explanations.append(f"Explicitly suitable for {crop_name.capitalize()} as documented in dataset ('{suitable_for}')")
        elif "vegetables" in suit_lower and "commercial" in crop_category:
            score += 25
            explanations.append(f"Broadly suitable for commercial/vegetable category ('{suitable_for}')")
        elif "rice" in suit_lower and "paddy" in crop_category:
            score += 45
            explanations.append(f"Directly suitable for paddy crop types ('{suitable_for}')")
        elif "rain-dependent" in suit_lower and ("low" in water_req or "rabi" in str(crop_info.get("season", "")).lower()):
            score += 20
            explanations.append(f"Aligned with low water demand crop profile ('{suitable_for}')")
        elif "supplemental" in suit_lower:
            score += 15
            explanations.append(f"Offers supplemental irrigation backup ('{suitable_for}')")
        else:
            score += 5
            explanations.append(f"General agro applicability ('{suitable_for}')")

        # 2. Water Availability Factor (Max 35 pts)
        if water_avail == "low":
            if water_eff == "High":
                score += 35
                explanations.append("High water efficiency preserves scarce local water availability")
            elif method_name.lower() == "farm pond":
                score += 25
                explanations.append("Farm pond captures and preserves critical buffer water under low availability")
            elif water_eff == "Medium":
                score += 15
            elif water_eff == "Low":
                score -= 10
                explanations.append("Low efficiency is risky when water availability is low")
        elif water_avail == "medium":
            if water_eff in ["High", "Medium"]:
                score += 25
                explanations.append(f"{water_eff} water efficiency provides sustainable resource usage")
            else:
                score += 10
        elif water_avail == "high":
            if method_name.lower() == "canal irrigation":
                score += 35
                explanations.append("Leverages high water availability with canal conveyance")
            elif water_eff in ["High", "Medium"]:
                score += 25
                explanations.append(f"Efficient application prevents waterlogging even with high supply")
            else:
                score += 15

        # 3. Preference Alignment (Max 20 pts)
        if "efficiency" in pref:
            if water_eff == "High":
                score += 20
                explanations.append("Matches your 'Efficiency-First' preference")
            elif water_eff == "Medium":
                score += 10
        elif "cost" in pref or "low" in pref:
            if "very low" in cost_lvl.lower():
                score += 20
                explanations.append("Matches your 'Low Cost' preference (Cost: Very Low)")
            elif "low" in cost_lvl.lower():
                score += 15
                explanations.append("Matches your 'Low Cost' preference (Cost: Low)")
            elif "high" in cost_lvl.lower():
                score -= 10
        elif "storage" in pref or "supplemental" in pref:
            if "pond" in method_name.lower() or "storage" in suit_lower:
                score += 25
                explanations.append("Matches your water storage preference")
        else:
            # Balanced / Any
            score += 10

        scored_methods.append({
            "method": method_name,
            "water_efficiency": water_eff,
            "cost_level": cost_lvl,
            "suitable_for": suitable_for,
            "score": score,
            "justification": " | ".join(explanations),
        })

    # Sort descending by score
    scored_methods.sort(key=lambda x: x["score"], reverse=True)
    top = scored_methods[0] if scored_methods else None

    # Construct the explainable reasoning strictly from dataset attributes
    if top:
        primary_reason = (
            f"The rule engine recommends **{top['method']}** based on dataset attributes: "
            f"it provides **{top['water_efficiency']} water efficiency** at a **{top['cost_level']} cost level**, "
            f"and is designated in the dataset for: *'{top['suitable_for']}'*. "
            f"This aligns with {crop_name}'s water requirements and local {water_availability.lower()} water availability."
        )
    else:
        primary_reason = "No matching irrigation method found."

    return {
        "top_method": top,
        "ranked_methods": scored_methods,
        "reason": primary_reason,
        "factors_used": {
            "crop": crop_name,
            "crop_water_requirement": crop_info.get("water_requirement", "N/A") if crop_info else "N/A",
            "water_availability": water_availability,
            "irrigation_preference": preference,
        },
    }


def compute_smart_agriculture_recommendations(
    crop_name: str,
    district_name: str,
    water_availability: str,
    irrigation_preference: str,
    crop_df: pd.DataFrame,
    rainfall_df: pd.DataFrame,
    irrigation_df: pd.DataFrame,
    sustainability_df: pd.DataFrame,
) -> Dict[str, Any]:
    """
    Combined Smart Agriculture Recommendation Engine.
    Integrates:
    - Selected Crop Profile (crop_data.csv)
    - District Rainfall Context (rainfall.csv)
    - Water Availability Assessment
    - Irrigation Method Advice (irrigation.csv)
    - Sustainability Practice Match (sustainability.csv)
    """
    # 1. Crop Context
    crop_info = get_crop_profile(crop_df, crop_name)
    crop_water_req = str(crop_info.get("water_requirement", "Medium")).strip() if crop_info else "Medium"
    crop_input_req = str(crop_info.get("input_requirement", "Medium")).strip() if crop_info else "Medium"
    crop_season = str(crop_info.get("season", "Kharif")).strip() if crop_info else "Kharif"
    crop_cat = str(crop_info.get("category", "General")).strip() if crop_info else "General"

    # 2. Rainfall Context
    rain_info = get_district_rainfall(rainfall_df, district_name)
    district_rainfall_mm = rain_info.get("annual_rainfall_mm", 0) if rain_info else 0
    state_avg_rainfall = rain_info.get("state_avg_rainfall_mm", 0) if rain_info else 0
    rainfall_diff_pct = rain_info.get("rainfall_diff_pct", 0) if rain_info else 0

    # 3. Water Stress & Feasibility Assessment (Rule-based)
    req_weights = {"Very High": 4, "High": 3, "Medium": 2, "Low": 1}
    avail_weights = {"High": 3, "Medium": 2, "Low": 1}

    req_score = req_weights.get(crop_water_req, 2)
    avail_score = avail_weights.get(water_availability, 2)

    # Adjust for district rainfall
    if rain_info:
        if rainfall_diff_pct >= 10:
            avail_score += 0.5
        elif rainfall_diff_pct <= -10:
            avail_score -= 0.5

    stress_delta = req_score - avail_score

    if stress_delta >= 1.5:
        stress_level = "High Water Stress"
        stress_color = "red"
        stress_desc = (
            f"The selected crop ({crop_name}) has {crop_water_req} water demand, whereas local water availability is {water_availability} "
            f"and district rainfall is {district_rainfall_mm} mm ({rainfall_diff_pct:+.1f}% vs state average). "
            f"Conservation and high-efficiency water application are critical."
        )
    elif stress_delta > 0:
        stress_level = "Moderate Water Stress"
        stress_color = "orange"
        stress_desc = (
            f"The crop's water demand ({crop_water_req}) moderately exceeds local baseline availability ({water_availability}). "
            f"Adopting efficient scheduling and storage will ensure consistent yields."
        )
    else:
        stress_level = "Favorable Water Balance"
        stress_color = "green"
        stress_desc = (
            f"Water availability ({water_availability}) and annual rainfall ({district_rainfall_mm} mm) "
            f"adequately support the {crop_water_req} water requirement of {crop_name}."
        )

    # 4. Irrigation Advice
    irrig_result = recommend_irrigation(
        crop_name=crop_name,
        water_availability=water_availability,
        preference=irrigation_preference,
        crop_df=crop_df,
        irrigation_df=irrigation_df,
    )
    top_irrigation = irrig_result.get("top_method")

    # 5. Sustainability Matching (from sustainability.csv)
    matched_initiatives = []
    if sustainability_df is not None and not sustainability_df.empty:
        for _, row in sustainability_df.iterrows():
            init_name = str(row.get("initiative", "")).strip()
            area = str(row.get("impact_area", "")).strip()
            impact = str(row.get("potential_impact", "")).strip()
            users = str(row.get("target_users", "")).strip()

            relevance_reasons = []

            # Match criteria based on farmer profile
            if "water" in area.lower():
                if stress_level in ["High Water Stress", "Moderate Water Stress"]:
                    relevance_reasons.append("Directly mitigates crop water stress through documented water efficiency/conservation")
                else:
                    relevance_reasons.append("Maintains resource sustainability and protects ground water tables")

            if "renewable" in area.lower() or "solar" in init_name.lower():
                if "Farmer" in users or "Farm" in users:
                    relevance_reasons.append(f"Provides clean energy autonomy for irrigation pumping (Target: {users})")

            if "organic" in area.lower() or "compost" in init_name.lower():
                if crop_input_req in ["Medium", "High"]:
                    relevance_reasons.append(f"Builds soil organic matter and offsets {crop_input_req.lower()} input requirements")

            if relevance_reasons:
                matched_initiatives.append({
                    "initiative": init_name,
                    "impact_area": area,
                    "potential_impact": impact,
                    "target_users": users,
                    "relevance_reason": " & ".join(relevance_reasons),
                })

    # Transparent Factors Summary
    factors = [
        {"Factor": "Selected Crop", "Value": f"{crop_name} ({crop_cat})", "Attribute Impact": f"Water Req: {crop_water_req}, Input Req: {crop_input_req}, Season: {crop_season}"},
        {"Factor": "District Rainfall", "Value": f"{district_name} ({district_rainfall_mm} mm)", "Attribute Impact": f"{rainfall_diff_pct:+.1f}% vs State Average ({state_avg_rainfall} mm)"},
        {"Factor": "Water Availability", "Value": water_availability, "Attribute Impact": f"Computed Stress Level: {stress_level}"},
        {"Factor": "Irrigation Preference", "Value": irrigation_preference, "Attribute Impact": f"Recommended: {top_irrigation['method'] if top_irrigation else 'N/A'}"},
        {"Factor": "Sustainability Options", "Value": f"{len(matched_initiatives)} matching initiatives", "Attribute Impact": "Filtered by impact area and target farmer relevance"},
    ]

    return {
        "crop_profile": crop_info,
        "rainfall_profile": rain_info,
        "water_stress": {
            "level": stress_level,
            "color": stress_color,
            "description": stress_desc,
        },
        "irrigation_recommendation": irrig_result,
        "sustainability_recommendations": matched_initiatives,
        "factors_table": factors,
    }
