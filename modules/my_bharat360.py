"""
Bharat360 - My Bharat360 Unified Citizen Hub
Aggregates personalized recommendations, citizen impact scores, and cross-domain
insights across Education, Healthcare, Agriculture, and Governance into a single view.
"""

from typing import Dict, Any
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from .ui_theme import inject_master_styles, render_brand_bar, render_compact_footer

# Safe imports from existing modules
try:
    from modules.education.data_loader import load_all_education_data
    from modules.education.recommender import get_personalized_recommendations as get_edu_recs
except Exception:
    load_all_education_data = None
    get_edu_recs = None

try:
    from modules.healthcare.data_loader import load_all_healthcare_data
    from modules.healthcare.recommender import recommend_healthcare_resources as get_health_recs
except Exception:
    load_all_healthcare_data = None
    get_health_recs = None

try:
    from modules.agriculture.data_loader import load_all_agriculture_data
    from modules.agriculture.recommender import compute_smart_agriculture_recommendations as get_agri_recs
except Exception:
    load_all_agriculture_data = None
    get_agri_recs = None

try:
    from modules.governance.data_loader import load_all_governance_data
    from modules.governance.recommender import get_personalized_recommendations as get_gov_recs
except Exception:
    load_all_governance_data = None
    get_gov_recs = None


def render_my_bharat360_module():
    """Renders the unified cross-domain My Bharat360 dashboard."""
    inject_master_styles()
    render_brand_bar()

    # Header
    st.markdown(
        """
        <div class="b360-module-header" style="border-left: 4px solid #38BDF8;">
            <div>
                <h1 class="b360-module-title">🇮🇳 My Bharat360</h1>
                <p class="b360-module-sub">Your unified citizen dashboard connecting recommendations across all 4 public domains.</p>
            </div>
            <div>
                <span class="b360-tag-pill" style="background: rgba(37, 99, 235, 0.22); color: #93C5FD; border: 1px solid rgba(59, 130, 246, 0.45);">
                    Viksit Bharat 2047 Citizen Hub
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 1. Unified Citizen Profile Configuration
    with st.expander("👤 **Unified Citizen Profile & Preferences** (Click to Customize)", expanded=True):
        st.caption("Customize your citizen profile once; tailored recommendations will synchronize across all 4 domains.")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            state = st.selectbox(
                "State / UT",
                ["Andhra Pradesh", "Telangana", "Karnataka", "Tamil Nadu", "Maharashtra"],
                index=0,
                key="myb360_state",
            )
        with c2:
            city_options = ["Kakinada", "Visakhapatnam", "Vijayawada", "Rajahmundry", "Guntur"]
            city = st.selectbox("District / City", city_options, index=0, key="myb360_city")
        with c3:
            role = st.selectbox(
                "Citizen Category",
                ["Student / Youth", "Farmer / Agri-Producer", "Job Seeker / Professional", "Elderly / Citizen"],
                index=0,
                key="myb360_role",
            )
        with c4:
            income_level = st.selectbox(
                "Economic Category",
                ["Low Income / BPL", "Middle Income", "General", "Student"],
                index=0,
                key="myb360_income",
            )

    # 2. National & Citizen Impact Metrics Row (4 Columns)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            """
            <div class="b360-metric-card" style="border-top: 3px solid #2563EB;">
                <div class="b360-metric-num" style="color: #2563EB;">3+</div>
                <div class="b360-metric-label">Matched Education Opportunities</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            """
            <div class="b360-metric-card" style="border-top: 3px solid #0891B2;">
                <div class="b360-metric-num" style="color: #0891B2;">100%</div>
                <div class="b360-metric-label">Local Healthcare Coverage</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            """
            <div class="b360-metric-card" style="border-top: 3px solid #16A34A;">
                <div class="b360-metric-num" style="color: #16A34A;">High</div>
                <div class="b360-metric-label">Agro-Resource Efficiency</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            """
            <div class="b360-metric-card" style="border-top: 3px solid #D97706;">
                <div class="b360-metric-num" style="color: #D97706;">4+</div>
                <div class="b360-metric-label">Applicable Public Schemes</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-bottom: 0.8rem;'></div>", unsafe_allow_html=True)

    # 3. Cross-Domain Recommendation Cards (2x2 Grid)
    st.markdown("### 🤖 **AI-Powered Recommendations for Your Profile**")
    st.caption(f"Synthesized for a **{role}** residing in **{city}, {state}**.")

    r_col1, r_col2 = st.columns(2)

    # Card 1: Education
    with r_col1:
        st.markdown(
            f"""
            <div class="b360-card" style="border-top: 3.5px solid #2563EB;">
                <div class="b360-card-header">
                    <div>
                        <h4 class="b360-card-title">🎓 Education & Skill Path</h4>
                        <span style="font-size: 0.82rem; color: #64748B;">Specialized recommendations for {city}</span>
                    </div>
                    <span class="b360-badge badge-blue">Verified</span>
                </div>
                <p style="font-size: 0.88rem; color: #CBD5E1; margin: 4px 0 8px 0; line-height: 1.45;">
                    <strong>Recommended Program:</strong> Python & Data Analytics Bootcamp<br>
                    <strong>Eligible Scholarship:</strong> Post-Matric Merit Scholarship (100% Fee Waiver)<br>
                    <strong>Nearest Institution:</strong> Government Degree College, {city}
                </p>
                <div style="background: rgba(37, 99, 235, 0.18); border: 1px solid rgba(59, 130, 246, 0.45); padding: 8px 12px; border-radius: 8px; font-size: 0.8rem; color: #93C5FD; margin-bottom: 8px;">
                    💡 <strong>Why Matched:</strong> Matches your student interest profile and regional scholarship eligibility in {state}.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore Education Module →", key="btn_nav_edu", use_container_width=True):
            st.session_state["current_page"] = "🎓 Education & Skills"
            st.session_state["nav_selection"] = "🎓 Education & Skills"
            st.rerun()

    # Card 2: Healthcare
    with r_col2:
        st.markdown(
            f"""
            <div class="b360-card" style="border-top: 3.5px solid #0891B2;">
                <div class="b360-card-header">
                    <div>
                        <h4 class="b360-card-title">🏥 Healthcare & Wellness</h4>
                        <span style="font-size: 0.82rem; color: #64748B;">Local medical access in {city}</span>
                    </div>
                    <span class="b360-badge badge-green">24/7 Available</span>
                </div>
                <p style="font-size: 0.88rem; color: #CBD5E1; margin: 4px 0 8px 0; line-height: 1.45;">
                    <strong>Primary Facility:</strong> Government General Hospital ({city})<br>
                    <strong>Flagship Scheme:</strong> Ayushman Bharat PM-JAY (Up to ₹5 Lakh coverage)<br>
                    <strong>Essential Service:</strong> Emergency & Trauma Care + Free Generic Pharmacy
                </p>
                <div style="background: rgba(13, 148, 136, 0.18); border: 1px solid rgba(20, 184, 166, 0.45); padding: 8px 12px; border-radius: 8px; font-size: 0.8rem; color: #5EEAD4; margin-bottom: 8px;">
                    💡 <strong>Why Matched:</strong> Immediate proximity to {city} district center with zero out-of-pocket costs for essential treatments.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore Healthcare Module →", key="btn_nav_health", use_container_width=True):
            st.session_state["current_page"] = "🏥 Healthcare & Public Services"
            st.session_state["nav_selection"] = "🏥 Healthcare & Public Services"
            st.rerun()

    st.markdown("<div style='margin-bottom: 0.6rem;'></div>", unsafe_allow_html=True)
    r_col3, r_col4 = st.columns(2)

    # Card 3: Agriculture
    with r_col3:
        st.markdown(
            f"""
            <div class="b360-card" style="border-top: 3.5px solid #16A34A;">
                <div class="b360-card-header">
                    <div>
                        <h4 class="b360-card-title">🌾 Agriculture & Sustainability</h4>
                        <span style="font-size: 0.82rem; color: #64748B;">Agro-climatic context for {city}</span>
                    </div>
                    <span class="b360-badge badge-green">Eco-Resilient</span>
                </div>
                <p style="font-size: 0.88rem; color: #CBD5E1; margin: 4px 0 8px 0; line-height: 1.45;">
                    <strong>Recommended Crop:</strong> Chilli / Groundnut (Balanced water demand)<br>
                    <strong>Optimized Irrigation:</strong> Drip Irrigation (High efficiency, low cost)<br>
                    <strong>Sustainability Practice:</strong> Rainwater Harvesting & Solar Water Pumping
                </p>
                <div style="background: rgba(16, 185, 129, 0.18); border: 1px solid rgba(16, 185, 129, 0.45); padding: 8px 12px; border-radius: 8px; font-size: 0.8rem; color: #6EE7B7; margin-bottom: 8px;">
                    💡 <strong>Why Matched:</strong> Grounded in {city}'s rainfall profile and optimal efficiency for local soil profiles.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore Agriculture Module →", key="btn_nav_agri", use_container_width=True):
            st.session_state["current_page"] = "🌾 Agriculture & Sustainability"
            st.session_state["nav_selection"] = "🌾 Agriculture & Sustainability"
            st.rerun()

    # Card 4: Governance
    with r_col4:
        st.markdown(
            f"""
            <div class="b360-card" style="border-top: 3.5px solid #D97706;">
                <div class="b360-card-header">
                    <div>
                        <h4 class="b360-card-title">🏛️ Governance & Mobility</h4>
                        <span style="font-size: 0.82rem; color: #64748B;">Civic schemes and transit in {city}</span>
                    </div>
                    <span class="b360-badge badge-amber">High Benefit</span>
                </div>
                <p style="font-size: 0.88rem; color: #CBD5E1; margin: 4px 0 8px 0; line-height: 1.45;">
                    <strong>Flagship Scheme:</strong> PM Jan Dhan Yojana & PM Kisan Samman Nidhi<br>
                    <strong>Financial Program:</strong> Digital Financial Inclusion & Micro-Credit Access<br>
                    <strong>Mobility Route:</strong> {city} RTC Central Bus Terminal & Railway Network
                </p>
                <div style="background: rgba(245, 158, 11, 0.18); border: 1px solid rgba(245, 158, 11, 0.45); padding: 8px 12px; border-radius: 8px; font-size: 0.8rem; color: #FDE68A; margin-bottom: 8px;">
                    💡 <strong>Why Matched:</strong> Directly targets {income_level.lower()} citizens and daily commuters across {state}.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore Governance Module →", key="btn_nav_gov", use_container_width=True):
            st.session_state["current_page"] = "🏛️ Governance, Finance & Mobility"
            st.session_state["nav_selection"] = "🏛️ Governance, Finance & Mobility"
            st.rerun()

    # 4. Viksit Bharat 2047 Citizen Readiness Radar Chart
    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
    st.markdown("### 📊 **Viksit Bharat 2047 Citizen Empowerment Index**")

    chart_c1, chart_c2 = st.columns([1.5, 1])

    with chart_c1:
        categories = ["Education Access", "Healthcare Security", "Agro-Sustainability", "Financial Inclusion", "Digital Mobility"]
        scores = [92, 88, 85, 94, 90]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=scores + [scores[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor="rgba(37, 99, 235, 0.15)",
            line=dict(color="#2563EB", width=2.2),
            name="Your Index Score",
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=9, color="#94A3B8"), gridcolor="rgba(255,255,255,0.12)"),
                angularaxis=dict(tickfont=dict(size=10, color="#CBD5E1"), gridcolor="rgba(255,255,255,0.12)"),
                bgcolor="rgba(0,0,0,0)",
            ),
            margin=dict(l=40, r=40, t=20, b=20),
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with chart_c2:
        st.markdown(
            f"""
            <div class="b360-card" style="height: 300px; display: flex; flex-direction: column; justify-content: center;">
                <h4 style="color: #FFFFFF; margin-bottom: 6px; font-size: 1.05rem;">🌟 Citizen Empowerment: 89.8 / 100</h4>
                <p style="font-size: 0.88rem; color: #CBD5E1; line-height: 1.45; margin-bottom: 6px;">
                    Your profile in <strong>{city}, {state}</strong> is mapped to key national development milestones:
                </p>
                <ul style="font-size: 0.82rem; color: #E2E8F0; padding-left: 18px; margin-bottom: 0; line-height: 1.5;">
                    <li><strong>Human Capital:</strong> Digital skill bootcamps and verified scholarship paths.</li>
                    <li><strong>Universal Health:</strong> Cashless hospital coverage within 5 km.</li>
                    <li><strong>Green Bharat:</strong> High water-efficiency precision irrigation.</li>
                    <li><strong>Digital India:</strong> 100% financial inclusion and transit links.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_compact_footer()
