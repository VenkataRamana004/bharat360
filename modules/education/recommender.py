"""
Rule-Based Recommender Engine for Education & Skills Module (Bharat360)
Member 1 - Education & Skills

Uses transparent, rule-based matching across:
- Student Profile (Education level, Area of Interest, Skill level, State, City, Age)
Against:
- Education Institutions (major_area, type, state, city)
- Scholarships (level, region, eligibility)
- Skill Programs (level, focus, cost, mode)
"""

from typing import Dict, Any, List
import pandas as pd


def _tokenize_and_match(text: str, keywords: List[str]) -> bool:
    """Helper to check if any keyword exists as a substring in text (case-insensitive)."""
    text_lower = str(text).lower()
    return any(kw.lower() in text_lower for kw in keywords if kw.strip())


def recommend_institutions(
    df_institutions: pd.DataFrame,
    profile: Dict[str, Any],
    top_n: int = 5
) -> pd.DataFrame:
    """
    Recommends educational institutions based on user's education level,
    interest, state, and city.
    """
    if df_institutions is None or df_institutions.empty:
        return pd.DataFrame()

    df = df_institutions.copy()
    user_state = profile.get("state", "").strip().lower()
    user_city = profile.get("city", "").strip().lower()
    user_interest = profile.get("interest", "").strip().lower()
    user_edu_level = profile.get("education_level", "").strip().lower()

    # Define interest keyword clusters
    interest_map = {
        "computer science": ["computer", "it", "software", "data", "analytics", "coding", "programming"],
        "programming": ["computer", "engineering", "polytechnic", "software", "data"],
        "data analytics": ["data", "analytics", "computer", "science"],
        "engineering": ["polytechnic", "engineering", "computer", "technical"],
        "commerce": ["commerce", "arts", "business", "finance", "accounting"],
        "science": ["mpc", "science", "polytechnic", "degree", "computer"]
    }

    # Educational level to institution type mapping
    level_type_map = {
        "school": ["junior college", "school"],
        "intermediate / 12th": ["junior college", "polytechnic"],
        "junior college": ["junior college", "polytechnic"],
        "diploma": ["polytechnic", "skill centre", "degree college"],
        "ug": ["degree college", "polytechnic", "skill centre"],
        "undergraduate": ["degree college", "polytechnic", "skill centre"],
        "pg": ["degree college", "skill centre"],
        "postgraduate": ["degree college", "skill centre"]
    }

    keywords_for_interest = [user_interest] if user_interest else []
    for key, cluster in interest_map.items():
        if key in user_interest or user_interest in key:
            keywords_for_interest.extend(cluster)
    keywords_for_interest = list(set([k for k in keywords_for_interest if k]))

    compatible_types = []
    for key, types in level_type_map.items():
        if key in user_edu_level or user_edu_level in key:
            compatible_types.extend(types)
    compatible_types = list(set(compatible_types))

    scores = []
    reasons_list = []

    for _, row in df.iterrows():
        score = 0
        reasons = []
        inst_name = str(row.get("name", "")).lower()
        inst_type = str(row.get("type", "")).lower()
        inst_area = str(row.get("major_area", "")).lower()
        inst_state = str(row.get("state", "")).lower()
        inst_city = str(row.get("city", "")).lower()

        # 1. Major area match with user interest
        if keywords_for_interest:
            if any(k in inst_area or k in inst_name for k in keywords_for_interest):
                score += 35
                reasons.append(f"Offers specialization in '{row.get('major_area', 'relevant field')}'")

        # 2. Institution type matches education level
        if compatible_types:
            if any(t in inst_type for t in compatible_types):
                score += 25
                reasons.append(f"Suitable for your stage ({row.get('type', 'Institution')})")
        else:
            score += 10

        # 3. Location match (State & City)
        if user_state and user_state != "all" and user_state in inst_state:
            score += 20
            reasons.append(f"Located in your state: {row.get('state', '')}")
            if user_city and user_city != "all" and user_city in inst_city:
                score += 15
                reasons.append(f"Close to your city: {row.get('city', '')}")

        # Baseline point if no specific matches so we don't return 0
        if score == 0:
            score = 10
            reasons.append("Recognized state institution")

        scores.append(score)
        reasons_list.append(" • ".join(reasons))

    df["match_score"] = scores
    df["match_reasons"] = reasons_list
    df = df.sort_values(by="match_score", ascending=False).reset_index(drop=True)
    return df.head(top_n)


def recommend_scholarships(
    df_scholarships: pd.DataFrame,
    profile: Dict[str, Any],
    top_n: int = 5
) -> pd.DataFrame:
    """
    Recommends scholarships based on user's education level, state/region,
    and eligibility criteria.
    """
    if df_scholarships is None or df_scholarships.empty:
        return pd.DataFrame()

    df = df_scholarships.copy()
    user_state = profile.get("state", "").strip().lower()
    user_edu_level = profile.get("education_level", "").strip().lower()
    user_interest = profile.get("interest", "").strip().lower()

    scores = []
    reasons_list = []

    for _, row in df.iterrows():
        score = 0
        reasons = []
        sch_level = str(row.get("level", "")).lower()
        sch_region = str(row.get("region", "")).lower()
        sch_elig = str(row.get("eligibility", "")).lower()
        sch_name = str(row.get("name", "")).lower()

        # 1. Level matching
        # Normalized checks (e.g. UG matches UG, UG/PG, Diploma/Degree)
        if "ug" in user_edu_level or "undergraduate" in user_edu_level:
            if any(l in sch_level for l in ["ug", "degree", "diploma/degree", "ug/pg"]):
                score += 40
                reasons.append(f"Matches your target level ({row.get('level', 'Degree')})")
        elif "pg" in user_edu_level or "postgraduate" in user_edu_level:
            if any(l in sch_level for l in ["pg", "ug/pg", "degree"]):
                score += 40
                reasons.append(f"Supports postgraduate level ({row.get('level', '')})")
        elif "school" in user_edu_level or "10th" in user_edu_level or "12th" in user_edu_level:
            if "school" in sch_level:
                score += 40
                reasons.append("Designed for school/intermediate students")
        elif "diploma" in user_edu_level:
            if any(l in sch_level for l in ["diploma", "diploma/degree"]):
                score += 40
                reasons.append("Eligible for diploma students")
        else:
            # Generic match
            score += 15

        # 2. Region matching (Pan-India or State)
        if "india" in sch_region or "national" in sch_region or "all" in sch_region:
            score += 25
            reasons.append("Pan-India national scholarship")
        elif user_state and user_state in sch_region:
            score += 35
            reasons.append(f"Direct state-level scholarship for {row.get('region', '')}")

        # 3. Eligibility & Interest synergy
        if ("tech" in sch_elig or "technical" in sch_elig) and any(kw in user_interest for kw in ["computer", "engineering", "programming", "tech"]):
            score += 20
            reasons.append("Special technical education grant")

        if "merit" in sch_elig or "meritorious" in sch_elig:
            score += 10
            reasons.append("Merit-based financial award")

        if score == 0:
            score = 10
            reasons.append("Open opportunity")

        scores.append(score)
        reasons_list.append(" • ".join(reasons))

    df["match_score"] = scores
    df["match_reasons"] = reasons_list
    df = df.sort_values(by="match_score", ascending=False).reset_index(drop=True)
    return df.head(top_n)


def recommend_skill_programs(
    df_skills: pd.DataFrame,
    profile: Dict[str, Any],
    top_n: int = 5
) -> pd.DataFrame:
    """
    Recommends skill-development programs based on user's current skill level,
    interest, and preferences.
    """
    if df_skills is None or df_skills.empty:
        return pd.DataFrame()

    df = df_skills.copy()
    user_skill_level = profile.get("skill_level", "").strip().lower()
    user_interest = profile.get("interest", "").strip().lower()

    # Keywords mapping
    interest_keywords = {
        "programming": ["programming", "python", "html", "javascript", "css", "code"],
        "computer science": ["programming", "python", "digital", "data", "html"],
        "data analytics": ["data", "analytics", "analysis", "python"],
        "business": ["business", "entrepreneurship", "management"],
        "commerce": ["business", "entrepreneurship", "finance"],
        "general": ["digital", "literacy", "basics"]
    }

    matched_keywords = [user_interest] if user_interest else []
    for key, words in interest_keywords.items():
        if key in user_interest or user_interest in key:
            matched_keywords.extend(words)
    matched_keywords = list(set([w for w in matched_keywords if w]))

    scores = []
    reasons_list = []

    for _, row in df.iterrows():
        score = 0
        reasons = []
        prog_name = str(row.get("name", "")).lower()
        prog_level = str(row.get("level", "")).lower()
        prog_focus = str(row.get("focus", "")).lower()
        prog_cost = str(row.get("cost", "")).lower()
        prog_mode = str(row.get("mode", "")).lower()

        # 1. Interest match on focus & name
        if matched_keywords:
            if any(kw in prog_focus or kw in prog_name for kw in matched_keywords):
                score += 45
                reasons.append(f"Direct match for '{row.get('focus', 'interest area')}'")

        # 2. Skill level match
        if user_skill_level:
            if user_skill_level in prog_level:
                score += 25
                reasons.append(f"Tailored for {row.get('level', '')} learners")
            elif "beginner" in user_skill_level and "intermediate" in prog_level:
                score += 10
                reasons.append("Next-step learning pathway")
            elif "advanced" in user_skill_level:
                score += 15
                reasons.append("Good supplementary refresher")
        else:
            score += 10

        # 3. Cost benefit (Free is high priority for citizen welfare)
        if "free" in prog_cost:
            score += 15
            reasons.append("100% Free / Zero tuition")
        elif "low" in prog_cost:
            score += 10
            reasons.append("Low cost affordable")

        # 4. Mode preference
        if "online" in prog_mode:
            score += 5
            reasons.append("Flexible self-paced online access")

        if score == 0:
            score = 10
            reasons.append("Recommended foundational skill program")

        scores.append(score)
        reasons_list.append(" • ".join(reasons))

    df["match_score"] = scores
    df["match_reasons"] = reasons_list
    df = df.sort_values(by="match_score", ascending=False).reset_index(drop=True)
    return df.head(top_n)


def get_personalized_recommendations(
    profile: Dict[str, Any],
    datasets: Dict[str, pd.DataFrame]
) -> Dict[str, pd.DataFrame]:
    """
    Unified rule-based recommendation orchestrator for Education & Skills.
    Returns:
        dict with keys: 'institutions', 'scholarships', 'skills'
    """
    df_inst = datasets.get("institutions", pd.DataFrame())
    df_sch = datasets.get("scholarships", pd.DataFrame())
    df_sk = datasets.get("skills", pd.DataFrame())

    return {
        "institutions": recommend_institutions(df_inst, profile),
        "scholarships": recommend_scholarships(df_sch, profile),
        "skills": recommend_skill_programs(df_sk, profile)
    }
