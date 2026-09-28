"""
Education & Skills Module for Bharat360
Member 1 - Education & Skills Module

Main entry point: render_education_module()
Integrates:
- Header & Civic-Tech Hero
- Key Metrics KPI row
- Student Profile Configuration
- Institutions Directory & Filters
- Scholarship Finder & Filters
- Skill Development Programs & Filters
- Rule-Based Recommendation Engine
- Visual Analytics (Plotly Charts)
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any

# Internal module imports (supports both relative package import and direct import)
try:
    from .data_loader import load_all_education_data
    from .recommender import get_personalized_recommendations
except ImportError:
    from modules.education.data_loader import load_all_education_data
    from modules.education.recommender import get_personalized_recommendations

# Safe Plotly import
try:
    import plotly.express as px
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

from modules.ui_theme import inject_master_styles, render_brand_bar


def _init_session_profile():
    """Ensure user profile is initialized in session state."""
    if "b360_student_profile" not in st.session_state:
        st.session_state["b360_student_profile"] = {
            "age": 20,
            "state": "Andhra Pradesh",
            "city": "Kakinada",
            "education_level": "Undergraduate (UG)",
            "interest": "Computer Science & IT",
            "skill_level": "Beginner"
        }


def render_hero_section():
    """Renders the top branding header for Education & Skills."""
    inject_master_styles()
    render_brand_bar()
    st.markdown(
        """
        <div class="b360-module-header" style="border-left: 4px solid #2563EB;">
            <div>
                <h1 class="b360-module-title">🎓 Education & Skills</h1>
                <p class="b360-module-sub">Discover scholarships, institutions and skill opportunities aligned with your academic path.</p>
            </div>
            <div>
                <span class="b360-tag-pill" style="background: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE;">
                    Viksit Bharat 2047 • Human Capital
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_overview_kpis(df_inst: pd.DataFrame, df_sch: pd.DataFrame, df_sk: pd.DataFrame):
    """Renders top key metrics summary cards in a clean 4-column layout."""
    col1, col2, col3, col4 = st.columns(4)

    total_inst = len(df_inst) if df_inst is not None else 0
    total_sch = len(df_sch) if df_sch is not None else 0
    total_sk = len(df_sk) if df_sk is not None else 0
    free_courses = len(df_sk[df_sk["cost"].str.lower().str.contains("free")]) if (df_sk is not None and "cost" in df_sk.columns) else 0

    with col1:
        st.markdown(
            f"""
            <div class="b360-metric-card" style="border-top: 3px solid #2563EB;">
                <div class="b360-metric-num" style="color: #2563EB;">{total_inst}</div>
                <div class="b360-metric-label">Institutions</div>
            </div>
            """, unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div class="b360-metric-card" style="border-top: 3px solid #16A34A;">
                <div class="b360-metric-num" style="color: #16A34A;">{total_sch}</div>
                <div class="b360-metric-label">Scholarships</div>
            </div>
            """, unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""
            <div class="b360-metric-card" style="border-top: 3px solid #7E22CE;">
                <div class="b360-metric-num" style="color: #7E22CE;">{total_sk}</div>
                <div class="b360-metric-label">Skill Programs</div>
            </div>
            """, unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            f"""
            <div class="b360-metric-card" style="border-top: 3px solid #38BDF8;">
                <div class="b360-metric-num" style="color: #38BDF8;">{free_courses}</div>
                <div class="b360-metric-label">100% Free Courses</div>
            </div>
            """, unsafe_allow_html=True
        )
    st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)


def render_student_profile_form() -> Dict[str, Any]:
    """
    Renders an intuitive, streamlined Student Profile form.
    Stores and synchronizes profile in st.session_state.
    """
    _init_session_profile()
    curr = st.session_state["b360_student_profile"]

    with st.expander("👤 **Student Profile & Preferences** (Click to Customize Matches)", expanded=True):
        st.caption("Personalized recommendations across colleges, scholarships, and skill paths automatically adapt to these settings.")

        c1, c2, c3 = st.columns(3)
        with c1:
            age = st.number_input("Age", min_value=12, max_value=80, value=curr["age"], step=1, key="edu_profile_age")
            state_options = ["Andhra Pradesh", "Telangana", "Karnataka", "Tamil Nadu", "Maharashtra", "Pan-India"]
            state_idx = state_options.index(curr["state"]) if curr["state"] in state_options else 0
            state = st.selectbox("State / Union Territory", state_options, index=state_idx, key="edu_profile_state")

        with c2:
            city_options = ["Kakinada", "Visakhapatnam", "Vijayawada", "Rajahmundry", "Guntur", "Hyderabad", "Bengaluru", "Other"]
            city_idx = city_options.index(curr["city"]) if curr["city"] in city_options else 0
            city = st.selectbox("City / District", city_options, index=city_idx, key="edu_profile_city")

            edu_options = [
                "Undergraduate (UG)",
                "Postgraduate (PG)",
                "Diploma / Polytechnic",
                "Junior College / 12th",
                "School (10th)"
            ]
            edu_idx = edu_options.index(curr["education_level"]) if curr["education_level"] in edu_options else 0
            edu_level = st.selectbox("Education Level", edu_options, index=edu_idx, key="edu_profile_level")

        with c3:
            interest_options = [
                "Computer Science & IT",
                "Programming",
                "Data Analytics",
                "Engineering & Technology",
                "Commerce & Business",
                "Digital Literacy",
                "General Education"
            ]
            int_idx = interest_options.index(curr["interest"]) if curr["interest"] in interest_options else 0
            interest = st.selectbox("Area of Interest", interest_options, index=int_idx, key="edu_profile_interest")

            skill_levels = ["Beginner", "Intermediate", "Advanced"]
            sk_idx = skill_levels.index(curr["skill_level"]) if curr["skill_level"] in skill_levels else 0
            skill_lvl = st.selectbox("Skill Level", skill_levels, index=sk_idx, key="edu_profile_skill")

        updated_profile = {
            "age": age,
            "state": state,
            "city": city,
            "education_level": edu_level,
            "interest": interest,
            "skill_level": skill_lvl
        }
        st.session_state["b360_student_profile"] = updated_profile

    st.markdown(
        f"""
        <div style="font-size: 0.84rem; color: #94A3B8; margin-bottom: 0.6rem;">
            🎯 <strong>Active Student Profile:</strong> {edu_level} • {interest} ({skill_lvl}) • {city}, {state}
        </div>
        """,
        unsafe_allow_html=True,
    )

    return updated_profile


def render_institutions_tab(df_institutions: pd.DataFrame):
    """
    Renders Section: Education Opportunities Directory.
    Includes state, city, institution type, and major area filters with cards/table view.
    """
    st.markdown("### 🏛️ Education Institutions Directory")
    st.caption("Search and explore certified degree colleges, polytechnics, junior colleges, and skill centres.")

    if df_institutions is None or df_institutions.empty:
        st.warning("⚠️ No institution records found in the dataset.")
        return

    # Filter controls
    f1, f2, f3, f4 = st.columns(4)

    states = ["All"] + sorted([s for s in df_institutions["state"].dropna().unique() if s])
    types = ["All"] + sorted([t for t in df_institutions["type"].dropna().unique() if t])
    areas = ["All"] + sorted([a for a in df_institutions["major_area"].dropna().unique() if a])

    with f1:
        selected_state = st.selectbox("Filter by State", states, key="inst_filter_state")

    filtered_for_city = df_institutions if selected_state == "All" else df_institutions[df_institutions["state"] == selected_state]
    cities = ["All"] + sorted([c for c in filtered_for_city["city"].dropna().unique() if c])

    with f2:
        selected_city = st.selectbox("Filter by City", cities, key="inst_filter_city")
    with f3:
        selected_type = st.selectbox("Institution Type", types, key="inst_filter_type")
    with f4:
        selected_area = st.selectbox("Specialization Area", areas, key="inst_filter_area")

    # Search Bar
    search_q = st.text_input("🔍 Search institution by name, major area or keyword:", "", key="inst_search_box")

    # Apply filters
    filtered_df = df_institutions.copy()
    if selected_state != "All":
        filtered_df = filtered_df[filtered_df["state"] == selected_state]
    if selected_city != "All":
        filtered_df = filtered_df[filtered_df["city"] == selected_city]
    if selected_type != "All":
        filtered_df = filtered_df[filtered_df["type"] == selected_type]
    if selected_area != "All":
        filtered_df = filtered_df[filtered_df["major_area"] == selected_area]
    if search_q.strip():
        q = search_q.strip().lower()
        filtered_df = filtered_df[
            filtered_df["name"].str.lower().str.contains(q) |
            filtered_df["major_area"].str.lower().str.contains(q) |
            filtered_df["city"].str.lower().str.contains(q) |
            filtered_df["type"].str.lower().str.contains(q)
        ]

    st.write(f"Showing **{len(filtered_df)}** of **{len(df_institutions)}** institutions")

    view_mode = st.radio("Display Mode:", ["Card View", "Table View"], horizontal=True, label_visibility="collapsed", key="inst_view_mode")

    if filtered_df.empty:
        st.info("No institutions match the chosen filter criteria. Try resetting filters.")
        return

    if view_mode == "Table View":
        display_cols = [c for c in ["name", "type", "major_area", "city", "state", "management"] if c in filtered_df.columns]
        st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)
    else:
        grid_cols = st.columns(2)
        for idx, (_, row) in enumerate(filtered_df.iterrows()):
            col = grid_cols[idx % 2]
            with col:
                st.markdown(
                    f"""
                    <div class="b360-card" style="border-top: 3px solid #2563EB;">
                        <div class="b360-card-header">
                            <div>
                                <h4 class="b360-card-title">{row.get('name', 'Institution')}</h4>
                                <span style="font-size: 0.82rem; color: #64748B;">📍 {row.get('city', '')}, {row.get('state', '')}</span>
                            </div>
                            <span class="b360-badge badge-blue">{row.get('type', '')}</span>
                        </div>
                        <div style="margin-top: 6px;">
                            <span class="b360-badge badge-purple">Specialization: {row.get('major_area', 'General')}</span>
                            <span class="b360-badge badge-green">Management: {row.get('management', 'Government')}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


def render_scholarships_tab(df_scholarships: pd.DataFrame):
    """
    Renders Section: Scholarship Finder.
    Filters by Education level, State/Region, and Eligibility category.
    """
    st.markdown("### 💰 Scholarship Finder")
    st.caption("Explore verified Central and State government scholarships, merit grants, and financial assistance schemes.")

    if df_scholarships is None or df_scholarships.empty:
        st.warning("⚠️ No scholarship records found in the dataset.")
        return

    # Filters
    s1, s2, s3 = st.columns(3)
    levels = ["All"] + sorted([lvl for lvl in df_scholarships["level"].dropna().unique() if lvl])
    regions = ["All"] + sorted([r for r in df_scholarships["region"].dropna().unique() if r])

    with s1:
        sel_level = st.selectbox("Education Level", levels, key="sch_filter_level")
    with s2:
        sel_region = st.selectbox("Region / State Scope", regions, key="sch_filter_region")
    with s3:
        search_elig = st.text_input("Filter by Eligibility / Keyword:", "", key="sch_filter_elig")

    # Apply filters
    filtered_sch = df_scholarships.copy()
    if sel_level != "All":
        filtered_sch = filtered_sch[filtered_sch["level"] == sel_level]
    if sel_region != "All":
        filtered_sch = filtered_sch[filtered_sch["region"] == sel_region]
    if search_elig.strip():
        q = search_elig.strip().lower()
        filtered_sch = filtered_sch[
            filtered_sch["name"].str.lower().str.contains(q) |
            filtered_sch["eligibility"].str.lower().str.contains(q) |
            filtered_sch["benefit"].str.lower().str.contains(q)
        ]

    st.write(f"Showing **{len(filtered_sch)}** of **{len(df_scholarships)}** scholarships")

    if filtered_sch.empty:
        st.info("No scholarships match the selected criteria. Try selecting 'All' for broader coverage.")
        return

    sch_cols = st.columns(2)
    for idx, (_, row) in enumerate(filtered_sch.iterrows()):
        with sch_cols[idx % 2]:
            st.markdown(
                f"""
                <div class="b360-card" style="border-top: 3px solid #16A34A;">
                    <div class="b360-card-header">
                        <div>
                            <h4 class="b360-card-title">📜 {row.get('name', 'Scholarship Scheme')}</h4>
                            <span style="font-size: 0.82rem; color: #64748B;">📍 Region: {row.get('region', 'India')}</span>
                        </div>
                        <span class="b360-badge badge-green">{row.get('level', 'UG/PG')}</span>
                    </div>
                    <div style="margin: 6px 0;">
                        <p style="margin: 3px 0; font-size: 0.88rem; color: #CBD5E1;">
                            <strong>Eligibility:</strong> {row.get('eligibility', 'Open to eligible students')}
                        </p>
                        <p style="margin: 3px 0; font-size: 0.88rem; color: #34D399;">
                            <strong>Benefit:</strong> {row.get('benefit', 'Financial assistance')}
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


def render_skills_tab(df_skills: pd.DataFrame):
    """
    Renders Section: Skill Programs.
    Filters: Skill level, Mode, Cost, Focus area.
    """
    st.markdown("### 🚀 Skill-Development Programs")
    st.caption("Equip yourself with industry-relevant skills supported by state and national skill missions.")

    if df_skills is None or df_skills.empty:
        st.warning("⚠️ No skill program records found in the dataset.")
        return

    # Filters
    k1, k2, k3, k4 = st.columns(4)

    levels = ["All"] + sorted([l for l in df_skills["level"].dropna().unique() if l])
    modes = ["All"] + sorted([m for m in df_skills["mode"].dropna().unique() if m])
    costs = ["All"] + sorted([c for c in df_skills["cost"].dropna().unique() if c])
    focuses = ["All"] + sorted([f for f in df_skills["focus"].dropna().unique() if f])

    with k1:
        sel_level = st.selectbox("Skill Level", levels, key="sk_filter_level")
    with k2:
        sel_mode = st.selectbox("Learning Mode", modes, key="sk_filter_mode")
    with k3:
        sel_cost = st.selectbox("Cost Type", costs, key="sk_filter_cost")
    with k4:
        sel_focus = st.selectbox("Focus Area", focuses, key="sk_filter_focus")

    filtered_sk = df_skills.copy()
    if sel_level != "All":
        filtered_sk = filtered_sk[filtered_sk["level"] == sel_level]
    if sel_mode != "All":
        filtered_sk = filtered_sk[filtered_sk["mode"] == sel_mode]
    if sel_cost != "All":
        filtered_sk = filtered_sk[filtered_sk["cost"] == sel_cost]
    if sel_focus != "All":
        filtered_sk = filtered_sk[filtered_sk["focus"] == sel_focus]

    st.write(f"Showing **{len(filtered_sk)}** of **{len(df_skills)}** skill programs")

    if filtered_sk.empty:
        st.info("No skill programs found matching these filters. Try broadening the selection.")
        return

    cols = st.columns(3)
    for idx, (_, row) in enumerate(filtered_sk.iterrows()):
        col = cols[idx % 3]
        cost_str = str(row.get('cost', '')).lower()
        cost_badge = "badge-green" if "free" in cost_str else "badge-amber"
        with col:
            st.markdown(
                f"""
                <div class="b360-card" style="border-top: 3px solid #7E22CE; min-height: 200px;">
                    <div class="b360-card-header">
                        <h4 class="b360-card-title">{row.get('name', 'Course')}</h4>
                        <span class="b360-badge {cost_badge}">{row.get('cost', 'Free')}</span>
                    </div>
                    <div style="margin: 4px 0;">
                        <span class="b360-badge badge-blue">{row.get('level', '')}</span>
                        <span class="b360-badge badge-purple">{row.get('mode', '')}</span>
                    </div>
                    <p style="margin-top: 8px; font-size: 0.85rem; color: #CBD5E1;">
                        <strong>Key Focus:</strong> {row.get('focus', '')}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )


def render_recommendations_tab(datasets: Dict[str, pd.DataFrame], profile: Dict[str, Any]):
    """
    Renders Section: AI-Powered Recommendations.
    Driven by transparent rule-based scoring matching user profile attributes.
    """
    st.markdown("### 🤖 **AI-Powered Recommendations**")
    st.info(f"Showing targeted opportunities for **{profile['education_level']}** student interested in **{profile['interest']}** ({profile['skill_level']} Level) in **{profile['state']}**.")

    recs = get_personalized_recommendations(profile, datasets)

    col1, col2 = st.columns(2)

    # 1. Recommended Institutions
    with col1:
        st.markdown("#### 🏛️ Top Matching Institutions")
        df_recs_inst = recs.get("institutions", pd.DataFrame())
        if df_recs_inst.empty:
            st.warning("No institution matching your exact profile right now.")
        else:
            for _, row in df_recs_inst.head(3).iterrows():
                st.markdown(
                    f"""
                    <div class="b360-card" style="border-top: 3px solid #2563EB;">
                        <div class="b360-card-header">
                            <div>
                                <h4 class="b360-card-title">{row.get('name', '')}</h4>
                                <span style="font-size: 0.82rem; color: #64748B;">📍 {row.get('city', '')}, {row.get('state', '')}</span>
                            </div>
                            <span class="b360-badge badge-blue">{row.get('type', '')}</span>
                        </div>
                        <div style="margin: 4px 0;">
                            <span class="b360-badge badge-purple">Area: {row.get('major_area', '')}</span>
                            <span class="b360-badge badge-amber">{row.get('management', 'Government')}</span>
                        </div>
                        <div style="background: rgba(37, 99, 235, 0.18); border: 1px solid rgba(59, 130, 246, 0.45); border-radius: 8px; padding: 6px 12px; font-size: 0.82rem; color: #93C5FD; margin-top: 6px;">
                            🎯 <strong>Why Matched:</strong> {row.get('match_reasons', 'Recommended for your profile')}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # 2. Recommended Scholarships
    with col2:
        st.markdown("#### 💰 Top Matching Scholarships")
        df_recs_sch = recs.get("scholarships", pd.DataFrame())
        if df_recs_sch.empty:
            st.warning("No specific scholarships found for current criteria.")
        else:
            for _, row in df_recs_sch.head(3).iterrows():
                st.markdown(
                    f"""
                    <div class="b360-card" style="border-top: 3px solid #16A34A;">
                        <div class="b360-card-header">
                            <div>
                                <h4 class="b360-card-title">{row.get('name', '')}</h4>
                                <span style="font-size: 0.82rem; color: #64748B;">🌍 Scope: {row.get('region', '')}</span>
                            </div>
                            <span class="b360-badge badge-green">{row.get('level', '')}</span>
                        </div>
                        <p style="margin: 4px 0; font-size: 0.85rem; color: #CBD5E1;"><strong>Eligibility:</strong> {row.get('eligibility', '')}</p>
                        <p style="margin: 4px 0; font-size: 0.85rem; color: #34D399;"><strong>Benefit:</strong> {row.get('benefit', '')}</p>
                        <div style="background: rgba(16, 185, 129, 0.18); border: 1px solid rgba(16, 185, 129, 0.45); border-radius: 8px; padding: 6px 12px; font-size: 0.82rem; color: #6EE7B7; margin-top: 6px;">
                            🎯 <strong>Why Matched:</strong> {row.get('match_reasons', 'Eligible based on profile')}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # 3. Recommended Skill Programs
    st.markdown("#### 🚀 Recommended Skill Development Programs")
    df_recs_sk = recs.get("skills", pd.DataFrame())
    if df_recs_sk.empty:
        st.warning("No skill programs found.")
    else:
        sk_cols = st.columns(min(3, len(df_recs_sk)))
        for i, (_, row) in enumerate(df_recs_sk.head(3).iterrows()):
            target_col = sk_cols[i % len(sk_cols)]
            with target_col:
                cost_tag = "badge-green" if "free" in str(row.get('cost', '')).lower() else "badge-amber"
                target_col.markdown(
                    f"""
                    <div class="b360-card" style="border-top: 3px solid #7E22CE; min-height: 190px;">
                        <div class="b360-card-header">
                            <h4 class="b360-card-title">{row.get('name', '')}</h4>
                            <span class="b360-badge {cost_tag}">{row.get('cost', '')}</span>
                        </div>
                        <div>
                            <span class="b360-badge badge-blue">{row.get('level', '')}</span>
                            <span class="b360-badge badge-purple">{row.get('mode', '')}</span>
                        </div>
                        <p style="margin: 6px 0; font-size: 0.84rem; color: #CBD5E1;">
                            <strong>Focus:</strong> {row.get('focus', '')}
                        </p>
                        <div style="background: rgba(139, 92, 246, 0.18); border: 1px solid rgba(139, 92, 246, 0.45); border-radius: 8px; padding: 6px 12px; font-size: 0.82rem; color: #DDD6FE; margin-top: 6px;">
                            🎯 <strong>Why Matched:</strong> {row.get('match_reasons', 'Matches your interest')}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


def render_analytics_tab(df_inst: pd.DataFrame, df_sch: pd.DataFrame, df_sk: pd.DataFrame):
    """
    Renders Visual Analytics using Plotly.
    Charts are dynamically generated from real CSV datasets.
    """
    st.markdown("### 📊 Education & Skills Visual Analytics")
    st.caption("Real-time data visualization based on certified educational opportunities across India.")

    if not HAS_PLOTLY:
        st.warning("Plotly is required for interactive charts. Please ensure plotly is installed.")
        return

    row1_c1, row1_c2 = st.columns(2)

    # 1. Institutions by Type
    with row1_c1:
        st.markdown("##### 🏛️ Institutions by Type")
        if df_inst is not None and not df_inst.empty and "type" in df_inst.columns:
            type_counts = df_inst["type"].value_counts().reset_index()
            type_counts.columns = ["Institution Type", "Count"]

            fig_type = px.pie(
                type_counts,
                names="Institution Type",
                values="Count",
                color_discrete_sequence=["#1D4ED8", "#0284C7", "#0D9488", "#D97706", "#7E22CE"],
                hole=0.45
            )
            fig_type.update_layout(
                margin=dict(l=10, r=10, t=20, b=10),
                height=280,
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_type, use_container_width=True)
        else:
            st.info("Insufficient data for institutions breakdown.")

    # 2. Skill Programs by Focus & Level
    with row1_c2:
        st.markdown("##### 🚀 Skill Programs by Category & Level")
        if df_sk is not None and not df_sk.empty and "focus" in df_sk.columns:
            sk_counts = df_sk.groupby(["focus", "level"]).size().reset_index(name="Count")
            fig_skills = px.bar(
                sk_counts,
                x="focus",
                y="Count",
                color="level",
                barmode="group",
                color_discrete_map={"Beginner": "#0D9488", "Intermediate": "#D97706", "Advanced": "#1D4ED8"},
                labels={"focus": "Program Focus", "Count": "Number of Programs", "level": "Level"}
            )
            fig_skills.update_layout(
                margin=dict(l=10, r=10, t=20, b=10),
                height=280,
                xaxis_tickangle=-25
            )
            st.plotly_chart(fig_skills, use_container_width=True)
        else:
            st.info("Insufficient data for skill programs chart.")

    row2_c1, row2_c2 = st.columns(2)

    # 3. Scholarship Scope & Level Distribution
    with row2_c1:
        st.markdown("##### 💰 Scholarships Distribution by Target Level")
        if df_sch is not None and not df_sch.empty and "level" in df_sch.columns:
            sch_counts = df_sch["level"].value_counts().reset_index()
            sch_counts.columns = ["Education Level", "Scholarships"]

            fig_sch = px.bar(
                sch_counts,
                x="Scholarships",
                y="Education Level",
                orientation="h",
                color="Education Level",
                color_discrete_sequence=px.colors.qualitative.Prism
            )
            fig_sch.update_layout(
                margin=dict(l=10, r=10, t=20, b=10),
                height=280,
                showlegend=False
            )
            st.plotly_chart(fig_sch, use_container_width=True)
        else:
            st.info("Insufficient data for scholarship chart.")

    # 4. Institutions by Major Area
    with row2_c2:
        st.markdown("##### 🎓 Institutions by Major Academic Specialization")
        if df_inst is not None and not df_inst.empty and "major_area" in df_inst.columns:
            area_counts = df_inst["major_area"].value_counts().reset_index()
            area_counts.columns = ["Major Area", "Count"]

            fig_area = px.bar(
                area_counts,
                x="Major Area",
                y="Count",
                color="Count",
                color_continuous_scale="Blues"
            )
            fig_area.update_layout(
                margin=dict(l=10, r=10, t=20, b=10),
                height=280,
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_area, use_container_width=True)
        else:
            st.info("Insufficient data for major area chart.")


def render_education_module():
    """
    Main entry point for Bharat360 Education & Skills Module.
    Visual Hierarchy:
    Header -> Key metrics -> Student profile -> Institutions / scholarships / skill programs -> Recommendations
    """
    # 1. Render Header
    render_hero_section()

    # 2. Dynamic Data Loading
    datasets = load_all_education_data()
    df_inst = datasets.get("institutions", pd.DataFrame())
    df_sch = datasets.get("scholarships", pd.DataFrame())
    df_sk = datasets.get("skills", pd.DataFrame())

    # 3. Key Metrics
    render_overview_kpis(df_inst, df_sch, df_sk)

    # 4. Student Profile
    profile = render_student_profile_form()

    # 5. Core Navigation Tabs: Structured per user requirement:
    # Institutions / scholarships / skill programs -> Existing recommendations
    tab_inst, tab_sch, tab_sk, tab_recs, tab_viz = st.tabs([
        "🏛️ Institutions",
        "💰 Scholarships",
        "🚀 Skill Programs",
        "🤖 Recommendations",
        "📊 Visual Analytics"
    ])

    with tab_inst:
        render_institutions_tab(df_inst)

    with tab_sch:
        render_scholarships_tab(df_sch)

    with tab_sk:
        render_skills_tab(df_sk)

    with tab_recs:
        render_recommendations_tab(datasets, profile)

    with tab_viz:
        render_analytics_tab(df_inst, df_sch, df_sk)


if __name__ == "__main__":
    st.set_page_config(page_title="Bharat360 - Education & Skills", page_icon="🎓", layout="wide")
    render_education_module()
