"""
recommender.py
Transparent, rule-based recommendation engine for Bharat360.
Matches citizen profile against:
- Government Schemes
- Financial Inclusion Resources
- Mobility & Transport Services
Provides clear, explainable reasons for every recommendation without making false guarantees.
"""

from typing import Dict, List, Any
import pandas as pd


def recommend_schemes(profile: Dict[str, Any], df_schemes: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Rule-based matching for Government Schemes.
    Returns ranked list of recommendations with explicit reasons.
    """
    if df_schemes.empty:
        return []

    results = []
    age = int(profile.get("age", 28))
    occupation = str(profile.get("occupation", "General Citizen")).lower()
    interest = str(profile.get("interest", "All Categories")).lower()

    for _, row in df_schemes.iterrows():
        score = 20  # Base eligibility baseline
        reasons: List[str] = []

        scheme_name = str(row.get("scheme", "")).strip()
        category = str(row.get("category", "")).strip()
        target_group = str(row.get("target_group", "")).strip()
        benefit = str(row.get("benefit", "")).strip()

        cat_lower = category.lower()
        target_lower = target_group.lower()
        benefit_lower = benefit.lower()
        name_lower = scheme_name.lower()

        # 1. Occupation-based alignment
        if "farmer" in occupation or "agriculture" in occupation:
            if "agriculture" in cat_lower or "farmer" in target_lower or "kisan" in name_lower:
                score += 45
                reasons.append("🌾 Matched your occupation: Specifically designed for farmers and agricultural producers.")
        elif "student" in occupation or "youth" in occupation:
            if "skill" in cat_lower or "youth" in target_lower or "employment" in cat_lower:
                score += 45
                reasons.append("🎓 Matched your demographic: Focuses on skill enhancement and youth employment.")
        elif "entrepreneur" in occupation or "business" in occupation:
            if "digital" in cat_lower or "financial" in cat_lower or "skill" in cat_lower:
                score += 35
                reasons.append("💼 Matched your profile: Provides digital access & financial foundations for small enterprises.")
        elif "wage" in occupation or "worker" in occupation:
            if "worker" in target_lower or "skill" in cat_lower or "financial" in cat_lower:
                score += 40
                reasons.append("🛠️ Matched your background: Offers vocational empowerment and basic welfare access.")
        elif "senior" in occupation or "retired" in occupation:
            if "health" in cat_lower or "families" in target_lower:
                score += 40
                reasons.append("👴 Matched senior profile: Essential healthcare protection and medical coverage.")
        elif "homemaker" in occupation:
            if "families" in target_lower or "health" in cat_lower or "financial" in cat_lower:
                score += 35
                reasons.append("🏡 Matched family needs: Delivers comprehensive household healthcare & inclusion.")
        elif "healthcare" in occupation:
            if "health" in cat_lower:
                score += 45
                reasons.append("🩺 Sector alignment: Directly relevant to national health mission and wellness coverage.")

        # 2. Age-specific triggers
        if age < 30 and ("youth" in target_lower or "skill" in cat_lower):
            score += 15
            reasons.append(f"⏱️ Age alignment ({age} yrs): High priority for young professionals and early career growth.")
        elif age >= 60 and ("health" in cat_lower or "families" in target_lower):
            score += 20
            reasons.append(f"🛡️ Age alignment ({age} yrs): Senior citizen healthcare safety net.")

        # 3. Interest selection alignment
        if interest != "all categories" and interest != "all":
            if interest in cat_lower or interest in benefit_lower or interest in name_lower:
                score += 35
                reasons.append(f"🎯 Direct preference match: You selected interest in '{category}'.")

        # 4. Universal citizen accessibility
        if "citizen" in target_lower or "eligible citizen" in target_lower:
            score += 15
            reasons.append("🇮🇳 Citizen-wide mandate: Open to eligible citizens nationwide.")

        if not reasons:
            reasons.append("📋 Broad relevance: General citizen empowerment program.")

        score = min(score, 99)

        results.append({
            "id": row.get("id", ""),
            "type": "Government Scheme",
            "title": scheme_name,
            "category": category,
            "target_group": target_group,
            "benefit": benefit,
            "score": score,
            "reasons": reasons,
            "raw_data": row.to_dict()
        })

    # Sort descending by match score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def recommend_financial_resources(profile: Dict[str, Any], df_financial: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Rule-based matching for Financial Inclusion resources.
    Returns ranked list of educational resources with transparent reasons.
    """
    if df_financial.empty:
        return []

    results = []
    occupation = str(profile.get("occupation", "General Citizen")).lower()
    interest = str(profile.get("interest", "All Categories")).lower()

    for _, row in df_financial.iterrows():
        score = 25  # Base financial literacy baseline
        reasons: List[str] = []

        service = str(row.get("service", "")).strip()
        area = str(row.get("area", "")).strip()
        target_group = str(row.get("target_group", "")).strip()
        purpose = str(row.get("purpose", "")).strip()

        svc_lower = service.lower()
        area_lower = area.lower()
        target_lower = target_group.lower()
        purpose_lower = purpose.lower()

        # 1. Occupation-driven need
        if "entrepreneur" in occupation or "business" in occupation:
            if "credit" in area_lower or "microcredit" in svc_lower:
                score += 45
                reasons.append("💼 Essential for Small Business: Awareness of Mudra and micro-credit financing facilities.")
            elif "payment" in area_lower or "digital" in svc_lower:
                score += 35
                reasons.append("📲 Merchant digitization: UPI and cashless digital payment acceptance.")
        elif "farmer" in occupation or "agriculture" in occupation:
            if "bank account" in svc_lower or "banking" in area_lower:
                score += 40
                reasons.append("🌾 Direct Benefit Transfer: Zero-balance bank account required for PM-KISAN and subsidies.")
            elif "credit" in area_lower:
                score += 35
                reasons.append("🌱 Agricultural credit awareness: Institutional loans vs informal lending risks.")
        elif "student" in occupation or "youth" in occupation:
            if "digital" in svc_lower or "payment" in area_lower:
                score += 40
                reasons.append("⚡ Digital native: Fast, secure UPI and mobile transaction awareness.")
            elif "literacy" in svc_lower or "budget" in purpose_lower:
                score += 35
                reasons.append("📚 Financial Literacy: Early habits in budgeting, saving, and avoiding fraud.")
        elif "wage" in occupation or "worker" in occupation:
            if "bank account" in svc_lower:
                score += 45
                reasons.append("💳 Foundation: Zero-balance PMJDY bank account with RuPay debit card.")
            elif "insurance" in svc_lower or "risk" in area_lower:
                score += 35
                reasons.append("🛡️ Low-cost micro-insurance: Awareness of PMJJBY and PMSBY safety nets.")
        elif "homemaker" in occupation or "senior" in occupation:
            if "insurance" in svc_lower or "risk" in area_lower:
                score += 40
                reasons.append("👨‍👩‍👧 Family safety net: Health and life risk protection awareness.")
            elif "literacy" in svc_lower:
                score += 30
                reasons.append("💡 Household budgeting: Smart savings habits and risk mitigation.")

        # 2. Target group compatibility
        if "citizen" in target_lower or "eligible" in target_lower or "families" in target_lower:
            score += 15
            reasons.append("👥 Universal citizen access: Open to all households.")

        # 3. Interest match
        if interest != "all categories" and interest != "all":
            if "financial" in interest or interest in area_lower or interest in purpose_lower:
                score += 25
                reasons.append(f"🔍 Aligned with your interest in {area}.")

        if not reasons:
            reasons.append("📖 General financial awareness: Essential knowledge for economic empowerment.")

        score = min(score, 99)

        results.append({
            "id": row.get("id", ""),
            "type": "Financial Inclusion",
            "title": service,
            "category": area,
            "target_group": target_group,
            "benefit": purpose,
            "score": score,
            "reasons": reasons,
            "raw_data": row.to_dict()
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def recommend_transport(profile: Dict[str, Any], df_transport: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Rule-based matching for Mobility / Transport services.
    Returns ranked list of mobility options based on citizen's state and city.
    """
    if df_transport.empty:
        return []

    results = []
    user_city = str(profile.get("city", "All Cities")).strip()
    user_state = str(profile.get("state", "All India")).strip()
    occupation = str(profile.get("occupation", "General Citizen")).lower()

    for _, row in df_transport.iterrows():
        score = 25  # Base transit utility
        reasons: List[str] = []

        mode = str(row.get("mode", "")).strip()
        city = str(row.get("city", "")).strip()
        state = str(row.get("state", "")).strip()
        service_type = str(row.get("service_type", "")).strip()
        purpose = str(row.get("purpose", "")).strip()

        # 1. City locality match
        if user_city.lower() != "all cities" and user_city.lower() != "all":
            if user_city.lower() == city.lower():
                score += 45
                reasons.append(f"📍 Local availability: Operates directly in your city ({city}).")
            else:
                score -= 10
        else:
            score += 15
            reasons.append("🏙️ Regional urban network: Key municipal transport hub.")

        # 2. State regional match
        if user_state.lower() != "all india" and user_state.lower() != "all":
            if user_state.lower() == state.lower():
                score += 25
                reasons.append(f"🗺️ State network: Active within {state}.")
            else:
                score -= 15
        else:
            score += 10

        # 3. Commute pattern alignment
        if "student" in occupation or "wage" in occupation or "professional" in occupation:
            if "urban" in purpose.lower() or "bus" in mode.lower():
                score += 20
                reasons.append("🚌 Daily commuter fit: Economical public bus transit for work or study.")
        if "rail" in mode.lower() or "intercity" in purpose.lower():
            score += 15
            reasons.append("🚆 Intercity transit: Connects your city with commercial and administrative centers.")

        if not reasons:
            reasons.append("🚦 Public transit connectivity: Reliable citizen mobility option.")

        score = max(min(score, 99), 10)

        results.append({
            "id": row.get("id", ""),
            "type": "Mobility",
            "title": f"{mode} - {city}",
            "category": f"{service_type} ({state})",
            "target_group": f"Commuters in {city}",
            "benefit": purpose,
            "score": score,
            "reasons": reasons,
            "raw_data": row.to_dict()
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def get_personalized_recommendations(
    profile: Dict[str, Any],
    df_schemes: pd.DataFrame,
    df_financial: pd.DataFrame,
    df_transport: pd.DataFrame,
) -> Dict[str, Any]:
    """
    Generate unified cross-domain personalized recommendations for citizen dashboard.
    """
    schemes_recs = recommend_schemes(profile, df_schemes)
    fin_recs = recommend_financial_resources(profile, df_financial)
    trans_recs = recommend_transport(profile, df_transport)

    # Top highlight from each domain
    top_scheme = schemes_recs[0] if schemes_recs else None
    top_fin = fin_recs[0] if fin_recs else None
    top_trans = trans_recs[0] if trans_recs else None

    # Combined top recommendations across all domains
    combined = schemes_recs + fin_recs + trans_recs
    combined.sort(key=lambda x: x["score"], reverse=True)

    return {
        "schemes": schemes_recs,
        "financial": fin_recs,
        "transport": trans_recs,
        "combined": combined,
        "top_scheme": top_scheme,
        "top_financial": top_fin,
        "top_transport": top_trans,
    }
