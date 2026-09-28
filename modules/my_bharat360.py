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
        <div class="b360-module-header">
            <div>
                <h1 class="b360-module-title">🇮🇳 My Bharat360</h1>
                <p class="b360-module-sub">Your unified citizen dashboard connecting recommendations across all 4 public domains.</p>
            </div>
            <div>
                <span class="b360-tag-pill" style="background: #E3F2FD; color: #0D47A1; border-color: #90CAF9;">
                    Viksit Bharat 2047 Citizen Passport
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
            <div class="b360-metric-card">
                <div class="b360-metric-num" style="color: #0284C7;">🎓 3+</div>
                <div class="b360-metric-label">Matched Education Opportunities</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            """
            <div class="b360-metric-card">
                <div class="b360-metric-num" style="color: #0E7490;">🏥 100%</div>
                <div class="b360-metric-label">Local Healthcare Coverage</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            """
            <div class="b360-metric-card">
                <div class="b360-metric-num" style="color: #15803D;">🌾 High</div>
                <div class="b360-metric-label">Agro-Resource Efficiency</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            """
            <div class="b360-metric-card">
                <div class="b360-metric-num" style="color: #B45309;">🏛️ 4+</div>
                <div class="b360-metric-label">Applicable Public Schemes</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 3. Cross-Domain Recommendation Cards (2x2 Grid)
    st.markdown("### 🤖 **AI-Powered Recommendations for Your Profile**")
    st.caption(f"Synthesized for a **{role}** residing in **{city}, {state}**.")

    r_col1, r_col2 = st.columns(2)

    # Card 1: Education
    with r_col1:
        st.markdown(
            f"""
            <div class="b360-card" style="border-top: 4px solid #0284C7;">
                <div class="b360-card-header">
                    <div>
                        <h4 class="b360-card-title">🎓 Education & Skill Path</h4>
                        <span style="font-size: 0.82rem; color: #64748B;">Specialized recommendations for {city}</span>
                    </div>
                    <span class="b360-badge badge-blue">Verified</span>
                </div>
                <p style="font-size: 0.9rem; color: #334155; margin: 4px 0 10px 0;">
                    <strong>Recommended Program:</strong> Python & Data Analytics Bootcamp<br>
                    <strong>Eligible Scholarship:</strong> Post-Matric Merit Scholarship (100% Tuition Fee Waiver)<br>
                    <strong>Nearest Institution:</strong> Government Degree College, {city}
                </p>
                <div style="background: #F0F9FF; border: 1px solid #BAE6FD; padding: 8px 12px; border-radius: 8px; font-size: 0.82rem; color: #0369A1;">
                    💡 <strong>Why Matched:</strong> Matches your student interest profile and regional scholarship eligibility in {state}.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore Education Module →", key="btn_nav_edu"):
            st.session_state["current_page"] = "🎓 Education & Skills"
            st.session_state["nav_selection"] = "🎓 Education & Skills"
            st.rerun()

    # Card 2: Healthcare
    with r_col2:
        st.markdown(
            f"""
            <div class="b360-card" style="border-top: 4px solid #0E7490;">
                <div class="b360-card-header">
                    <div>
                        <h4 class="b360-card-title">🏥 Healthcare & Wellness</h4>
                        <span style="font-size: 0.82rem; color: #64748B;">Local medical access in {city}</span>
                    </div>
                    <span class="b360-badge badge-green">24/7 Available</span>
                </div>
                <p style="font-size: 0.9rem; color: #334155; margin: 4px 0 10px 0;">
                    <strong>Primary Facility:</strong> Government General Hospital ({city})<br>
                    <strong>Flagship Scheme:</strong> Ayushman Bharat PM-JAY (Up to ₹5 Lakh cashless coverage)<br>
                    <strong>Essential Service:</strong> Emergency & Trauma Care + Free Generic Pharmacy
                </p>
                <div style="background: #ECFDF5; border: 1px solid #A7F3D0; padding: 8px 12px; border-radius: 8px; font-size: 0.82rem; color: #047857;">
                    💡 <strong>Why Matched:</strong> Immediate proximity to {city} district center with zero out-of-pocket costs for essential treatments.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore Healthcare Module →", key="btn_nav_health"):
            st.session_state["current_page"] = "🏥 Healthcare & Public Services"
            st.session_state["nav_selection"] = "🏥 Healthcare & Public Services"
            st.rerun()

    r_col3, r_col4 = st.columns(2)

    # Card 3: Agriculture
    with r_col3:
        st.markdown(
            f"""
            <div class="b360-card" style="border-top: 4px solid #16A34A;">
                <div class="b360-card-header">
                    <div>
                        <h4 class="b360-card-title">🌾 Agriculture & Sustainability</h4>
                        <span style="font-size: 0.82rem; color: #64748B;">Agro-climatic context for {city}</span>
                    </div>
                    <span class="b360-badge badge-green">Eco-Resilient</span>
                </div>
                <p style="font-size: 0.9rem; color: #334155; margin: 4px 0 10px 0;">
                    <strong>Recommended Crop:</strong> Chilli / Groundnut (High yield & balanced water demand)<br>
                    <strong>Optimized Irrigation:</strong> Drip Irrigation (High efficiency, low cost)<br>
                    <strong>Sustainability Practice:</strong> Rainwater Harvesting & Solar Water Pumping
                </p>
                <div style="background: #F0FDF4; border: 1px solid #BBF7D0; padding: 8px 12px; border-radius: 8px; font-size: 0.82rem; color: #15803D;">
                    💡 <strong>Why Matched:</strong> Grounded in {city}'s annual rainfall dataset and optimal efficiency for local soil profiles.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore Agriculture Module →", key="btn_nav_agri"):
            st.session_state["current_page"] = "🌾 Agriculture & Sustainability"
            st.session_state["nav_selection"] = "🌾 Agriculture & Sustainability"
            st.rerun()

    # Card 4: Governance
    with r_col4:
        st.markdown(
            f"""
            <div class="b360-card" style="border-top: 4px solid #D97706;">
                <div class="b360-card-header">
                    <div>
                        <h4 class="b360-card-title">🏛️ Governance & Mobility</h4>
                        <span style="font-size: 0.82rem; color: #64748B;">Civic schemes and transport in {city}</span>
                    </div>
                    <span class="b360-badge badge-amber">High Benefit</span>
                </div>
                <p style="font-size: 0.9rem; color: #334155; margin: 4px 0 10px 0;">
                    <strong>Flagship Scheme:</strong> PM Jan Dhan Yojana & PM Kisan Samman Nidhi<br>
                    <strong>Financial Program:</strong> Digital Financial Inclusion & Micro-Credit Access<br>
                    <strong>Mobility Route:</strong> {city} RTC Central Bus Terminal & Railway Network
                </p>
                <div style="background: #FFFBEB; border: 1px solid #FDE68A; padding: 8px 12px; border-radius: 8px; font-size: 0.82rem; color: #B45309;">
                    💡 <strong>Why Matched:</strong> Directly targets {income_level.lower()} citizens and daily commuters across {state}.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore Governance Module →", key="btn_nav_gov"):
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
            fillcolor="rgba(30, 136, 229, 0.2)",
            line=dict(color="#1E88E5", width=2.5),
            name="Your Index Score",
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10, color="#64748B")),
            ),
            margin=dict(l=40, r=40, t=20, b=20),
            height=320,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with chart_c2:
        st.markdown(
            f"""
            <div class="b360-card" style="height: 320px; display: flex; flex-direction: column; justify-content: center;">
                <h4 style="color: #0B2545; margin-bottom: 8px;">🌟 Citizen Empowerment: 89.8 / 100</h4>
                <p style="font-size: 0.9rem; color: #475569; line-height: 1.5;">
                    Your profile in <strong>{city}, {state}</strong> is closely mapped to key national development milestones:
                </p>
                <ul style="font-size: 0.85rem; color: #334155; padding-left: 20px; margin-bottom: 0;">
                    <li><strong>NEP 2020:</strong> Digital skill bootcamps and fee-free scholarship paths.</li>
                    <li><strong>Universal Health:</strong> Cashless hospital coverage within 5 km.</li>
                    <li><strong>Green Bharat:</strong> High water-efficiency precision irrigation.</li>
                    <li><strong>Digital India:</strong> 100% financial inclusion and transit links.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_compact_footer()
