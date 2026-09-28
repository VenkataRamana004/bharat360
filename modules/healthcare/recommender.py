"""
Rule-Based Healthcare Service Recommendation Engine for Bharat360.
Matches citizen age group, location, and service interests to available:
- Health Services (from health_services.csv)
- Nearby Healthcare Facilities (from hospitals.csv)
- Health Awareness Guidance (from health_awareness.csv)

Strictly informational:
No medical prescriptions, diagnosis, or personalized medical treatment.
"""

from typing import Dict, List, Optional
import pandas as pd


def recommend_healthcare_resources(
    age_group: str,
    selected_state: Optional[str],
    selected_city: Optional[str],
    service_interest: str,
    df_hospitals: pd.DataFrame,
    df_services: pd.DataFrame,
    df_awareness: pd.DataFrame,
) -> Dict[str, any]:
    """
    Executes rule-based matching based purely on dataset records.
    Returns:
        dict containing:
        - services: DataFrame of matched services
        - hospitals: DataFrame of matched hospitals in location
        - awareness: DataFrame of matched awareness topics
        - rationale: List of human-readable match explanations
        - disclaimer: Mandatory medical advisory notice
    """
    rationale = []

    # 1. Match Services based on interest and age group
    matched_services = df_services.copy() if not df_services.empty else pd.DataFrame()
    interest_lower = (service_interest or "").lower()
    age_lower = (age_group or "").lower()

    if not matched_services.empty:
        service_mask = pd.Series([False] * len(matched_services), index=matched_services.index)

        # Keyword mapping rules
        if any(w in interest_lower for w in ["all", "comprehensive", "any"]):
            service_mask[:] = True
            rationale.append("All available public health services selected.")
        else:
            if any(w in interest_lower for w in ["maternal", "pregnant", "mother"]) or "mother" in age_lower:
                m = matched_services["service"].str.lower().str.contains("maternal|pregnancy", regex=True) | \
                    matched_services["description"].str.lower().str.contains("maternal|pregnancy", regex=True)
                service_mask |= m
                rationale.append("Maternal and prenatal care services matched for maternal health needs.")

            if any(w in interest_lower for w in ["child", "immuniz", "vaccin"]) or any(w in age_lower for w in ["child", "infant"]):
                m = matched_services["service"].str.lower().str.contains("immuniz|vaccin|child", regex=True) | \
                    matched_services["description"].str.lower().str.contains("immuniz|vaccin|child", regex=True)
                service_mask |= m
                rationale.append("Immunization and vaccination programs prioritized for infants and children.")

            if any(w in interest_lower for w in ["emergency", "urgent", "critical", "trauma"]):
                m = matched_services["service"].str.lower().str.contains("emergency|urgent", regex=True) | \
                    matched_services["description"].str.lower().str.contains("emergency|urgent", regex=True)
                service_mask |= m
                rationale.append("Emergency and casualty services prioritized for urgent assistance.")

            if any(w in interest_lower for w in ["diagnostic", "lab", "test", "scan", "blood"]):
                m = matched_services["service"].str.lower().str.contains("diagnostic|lab|test", regex=True) | \
                    matched_services["description"].str.lower().str.contains("diagnostic|lab|test", regex=True)
                service_mask |= m
                rationale.append("Diagnostic laboratory and testing services prioritized.")

            if any(w in interest_lower for w in ["opd", "consultation", "general", "doctor", "physician"]):
                m = matched_services["service"].str.lower().str.contains("opd|general|consultation", regex=True) | \
                    matched_services["description"].str.lower().str.contains("opd|general|consultation", regex=True)
                service_mask |= m
                rationale.append("General OPD consultation matched for general healthcare evaluation.")

            if any(w in interest_lower for w in ["preventive", "wellness", "checkup"]):
                m = matched_services["service"].str.lower().str.contains("opd|diagnostic|general", regex=True)
                service_mask |= m
                rationale.append("Preventive and diagnostic checkup services matched.")

        # Fallback: if no keyword rule triggered, perform dynamic token match
        if not service_mask.any():
            tokens = [t for t in interest_lower.replace("/", " ").replace("-", " ").split() if len(t) > 2]
            for tok in tokens:
                service_mask |= matched_services["service"].str.lower().str.contains(tok, regex=False) | \
                                matched_services["description"].str.lower().str.contains(tok, regex=False)
            if service_mask.any():
                rationale.append(f"Services dynamically matched with query keywords: '{service_interest}'.")
            else:
                # Return all services if nothing specific matched
                service_mask[:] = True
                rationale.append("Showing all essential public health services.")

        matched_services = matched_services[service_mask].reset_index(drop=True)

    # 2. Match Hospitals based on Location & Facility Type
    matched_hospitals = df_hospitals.copy() if not df_hospitals.empty else pd.DataFrame()

    if not matched_hospitals.empty:
        # State filter
        if selected_state and selected_state not in ["All States", "All"]:
            state_match = matched_hospitals["state"].str.lower() == selected_state.lower()
            if state_match.any():
                matched_hospitals = matched_hospitals[state_match]

        # City filter
        if selected_city and selected_city not in ["All Cities", "All"]:
            city_match = matched_hospitals["city"].str.lower() == selected_city.lower()
            if city_match.any():
                matched_hospitals = matched_hospitals[city_match]
                rationale.append(f"Located {len(matched_hospitals)} healthcare facility(ies) within {selected_city}.")
            else:
                rationale.append(f"No direct hospital in {selected_city}; displaying regional facilities in {selected_state or 'the state'}.")

        # Prioritize facility type depending on service need
        if any(w in interest_lower for w in ["emergency", "diagnostic", "urgent"]):
            # Rank Multi-specialty & General hospitals higher
            type_order = {"multi-specialty": 0, "general": 1, "primary/community care": 2}
            matched_hospitals["_rank"] = matched_hospitals["type"].str.lower().map(lambda x: type_order.get(x, 3))
            matched_hospitals = matched_hospitals.sort_values(by="_rank").drop(columns=["_rank"]).reset_index(drop=True)
        elif any(w in interest_lower for w in ["immuniz", "vaccin", "child"]):
            # Community Health Centres and primary centres are great for immunization
            type_order = {"primary/community care": 0, "general": 1, "multi-specialty": 2}
            matched_hospitals["_rank"] = matched_hospitals["type"].str.lower().map(lambda x: type_order.get(x, 3))
            matched_hospitals = matched_hospitals.sort_values(by="_rank").drop(columns=["_rank"]).reset_index(drop=True)

    # 3. Match Health Awareness Guidance
    matched_awareness = df_awareness.copy() if not df_awareness.empty else pd.DataFrame()

    if not matched_awareness.empty:
        aware_mask = pd.Series([False] * len(matched_awareness), index=matched_awareness.index)

        # Target group & interest matching
        if "mother" in age_lower or "maternal" in interest_lower or "pregnan" in interest_lower:
            aware_mask |= matched_awareness["target_group"].str.lower().str.contains("pregnant|mother|women", regex=True) | \
                          matched_awareness["topic"].str.lower().str.contains("maternal", regex=True)
            rationale.append("Antenatal and maternal guidance included for maternal health.")

        if "child" in age_lower or "infant" in age_lower or "immuniz" in interest_lower or "vaccin" in interest_lower:
            aware_mask |= matched_awareness["target_group"].str.lower().str.contains("families|child", regex=True) | \
                          matched_awareness["topic"].str.lower().str.contains("vaccination", regex=True)
            rationale.append("Vaccination schedules guidance included for child care.")

        if "adult" in age_lower or "senior" in age_lower or "preventive" in interest_lower or "checkup" in interest_lower:
            aware_mask |= matched_awareness["target_group"].str.lower().str.contains("adult", regex=True) | \
                          matched_awareness["topic"].str.lower().str.contains("preventive", regex=True)

        # Always include baseline public hygiene / nutrition awareness if general or fallback
        if not aware_mask.any() or "all" in interest_lower or "general" in age_lower:
            aware_mask |= matched_awareness["target_group"].str.lower().str.contains("general public|all", regex=True)

        matched_awareness = matched_awareness[aware_mask].reset_index(drop=True)

    disclaimer = (
        "This recommendation is informational only and based purely on the available Bharat360 dataset. "
        "It does not provide diagnosis, medical prescription, or personalized medical treatment. "
        "In case of a medical emergency, immediately contact national emergency services at 108 / 102 "
        "or visit your nearest hospital."
    )

    return {
        "services": matched_services,
        "hospitals": matched_hospitals,
        "awareness": matched_awareness,
        "rationale": rationale,
        "disclaimer": disclaimer,
    }
