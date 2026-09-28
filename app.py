"""
Bharat360 - One Platform. Multiple Needs.
Viksit Bharat 2047 Hackathon Project.
Unified Civic-Tech Application Entrypoint & Executive Landing Page.
"""

from pathlib import Path
import streamlit as st
import pandas as pd

from modules.ui_theme import (
    inject_master_styles,
    render_brand_bar,
    render_compact_footer,
)
from modules.education import render_education_module
from modules.healthcare import render_healthcare_module
from modules.agriculture import render_agriculture_module
from modules.governance import render_governance_module
from modules.my_bharat360 import render_my_bharat360_module

# Configure page settings once at application root
st.set_page_config(
    page_title="Bharat360 - One Platform. Multiple Needs.",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAV_OPTIONS = [
    "🏠 Home",
    "🎓 Education & Skills",
    "🏥 Healthcare & Public Services",
    "🌾 Agriculture & Sustainability",
    "🏛️ Governance, Finance & Mobility",
    "🇮🇳 My Bharat360",
]


def navigate_to(page_name: str):
    """
    Central navigation router.
    Synchronizes current_page state and triggers immediate Streamlit rerun.
    """
    st.session_state["current_page"] = page_name
    st.session_state["nav_selection"] = page_name
    st.rerun()


def _init_global_state():
    """Initializes global navigation and citizen location filters."""
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = st.session_state.get("nav_selection", "🏠 Home")
    st.session_state["nav_selection"] = st.session_state["current_page"]

    if "global_state" not in st.session_state:
        st.session_state["global_state"] = "Andhra Pradesh"
    if "global_city" not in st.session_state:
        st.session_state["global_city"] = "Kakinada"


@st.cache_data(show_spinner=False)
def _load_summary_metrics():
    """Dynamically aggregates key metrics from underlying datasets for landing page."""
    metrics = {
        "institutions": 24,
        "scholarships": 10,
        "hospitals": 15,
        "health_services": 12,
        "crops": 16,
        "districts": 8,
        "schemes": 14,
        "transit": 12,
    }
    try:
        from modules.education.data_loader import load_all_education_data
        edu_data = load_all_education_data()
        if "institutions" in edu_data and not edu_data["institutions"].empty:
            metrics["institutions"] = len(edu_data["institutions"])
        if "scholarships" in edu_data and not edu_data["scholarships"].empty:
            metrics["scholarships"] = len(edu_data["scholarships"])
    except Exception:
        pass

    try:
        from modules.healthcare.data_loader import load_all_healthcare_data
        health_data = load_all_healthcare_data()
        if "hospitals" in health_data and not health_data["hospitals"].empty:
            metrics["hospitals"] = len(health_data["hospitals"])
        if "services" in health_data and not health_data["services"].empty:
            metrics["health_services"] = len(health_data["services"])
    except Exception:
        pass

    try:
        from modules.agriculture.data_loader import load_all_agriculture_data
        agri_data = load_all_agriculture_data()
        if "crop_data" in agri_data and not agri_data["crop_data"].empty:
            metrics["crops"] = len(agri_data["crop_data"])
        if "rainfall" in agri_data and not agri_data["rainfall"].empty:
            metrics["districts"] = len(agri_data["rainfall"])
    except Exception:
        pass

    try:
        from modules.governance.data_loader import load_all_governance_data
        gov_data = load_all_governance_data()
        if "schemes" in gov_data and not gov_data["schemes"].empty:
            metrics["schemes"] = len(gov_data["schemes"])
        if "transport" in gov_data and not gov_data["transport"].empty:
            metrics["transit"] = len(gov_data["transport"])
    except Exception:
        pass

    return metrics


def render_landing_page():
    """
    Renders the executive, Indian civic-tech Landing Page for Bharat360
    closely matching the dark navy cinematic reference design.
    """
    inject_master_styles()
    render_brand_bar()

    summary_metrics = _load_summary_metrics()

    # 1. Top Right Viksit Bharat 2047 Pill
    st.markdown(
        """
        <div style="display: flex; justify-content: flex-end; margin-bottom: 0.1rem;">
            <div class="b360-top-viksit-pill">
                <span style="color: #10B981; font-weight: 800;">↗</span> Viksit Bharat 2047
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. Executive Hero Section (Full width, lets the background breathe)
    st.markdown(
        """
        <div class="b360-ref-hero">
            <div class="b360-ref-hero-title">
                BHARAT<span style="color: #F59E0B;">3</span><span style="color: #38BDF8;">6</span><span style="color: #10B981;">0</span>
            </div>
            <div class="b360-ref-hero-sub">One Platform. Multiple Needs.</div>
            <p class="b360-ref-hero-desc">
                Technology-driven insights for a developed Bharat.
            </p>
            <div class="b360-ref-hero-badges">
                <span class="b360-ref-badge badge-blue">⚙ Data Driven</span>
                <span class="b360-ref-badge badge-amber">💡 Explainable Rule Engine</span>
                <span class="b360-ref-badge badge-green">🌱 Resource Efficiency</span>
                <span class="b360-ref-badge badge-purple">👥 Verified Data</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 3. Four Major Domain Dashboard Cards (One row on desktop matching reference)
    d_col1, d_col2, d_col3, d_col4 = st.columns(4)

    # Card 1: Education & Skills
    with d_col1:
        st.markdown(
            f"""
            <div class="b360-ref-card b360-card-edu">
                <div class="b360-ref-icon-circle bg-blue">🎓</div>
                <div class="b360-ref-card-title">Education & Skills</div>
                <div class="b360-ref-card-quote">"Better learning. Brighter futures."</div>
                <div class="b360-ref-card-metric">
                    <div class="b360-ref-metric-val">👥 {summary_metrics['institutions']}+</div>
                    <div class="b360-ref-metric-sub">Institutions & Programs</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore →", key="card_btn_edu", use_container_width=True):
            navigate_to("🎓 Education & Skills")

    # Card 2: Healthcare & Public Services
    with d_col2:
        st.markdown(
            f"""
            <div class="b360-ref-card b360-card-health">
                <div class="b360-ref-icon-circle bg-coral">➕</div>
                <div class="b360-ref-card-title">Healthcare & Public Services</div>
                <div class="b360-ref-card-quote">"Accessible healthcare. Healthier lives."</div>
                <div class="b360-ref-card-metric">
                    <div class="b360-ref-metric-val">❤️ {summary_metrics['hospitals']}+</div>
                    <div class="b360-ref-metric-sub">Hospitals & Centers</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore →", key="card_btn_health", use_container_width=True):
            navigate_to("🏥 Healthcare & Public Services")

    # Card 3: Agriculture & Sustainability
    with d_col3:
        st.markdown(
            f"""
            <div class="b360-ref-card b360-card-agri">
                <div class="b360-ref-icon-circle bg-green">🌱</div>
                <div class="b360-ref-card-title">Agriculture & Sustainability</div>
                <div class="b360-ref-card-quote">"Smarter farming. Greener tomorrow."</div>
                <div class="b360-ref-card-metric">
                    <div class="b360-ref-metric-val">🌱 {summary_metrics['crops']}+</div>
                    <div class="b360-ref-metric-sub">Crops & Water Profiles</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore →", key="card_btn_agri", use_container_width=True):
            navigate_to("🌾 Agriculture & Sustainability")

    # Card 4: Governance, Finance & Mobility
    with d_col4:
        st.markdown(
            f"""
            <div class="b360-ref-card b360-card-gov">
                <div class="b360-ref-icon-circle bg-purple">🏛️</div>
                <div class="b360-ref-card-title">Governance, Finance & Mobility</div>
                <div class="b360-ref-card-quote">"Transparent systems. Stronger India."</div>
                <div class="b360-ref-card-metric">
                    <div class="b360-ref-metric-val">🛡️ {summary_metrics['schemes']}+</div>
                    <div class="b360-ref-metric-sub">Verified Public Schemes</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore →", key="card_btn_gov", use_container_width=True):
            navigate_to("🏛️ Governance, Finance & Mobility")

    # 4. Bharat360 at a Glance Metrics Section (Using Real Dynamic Data)
    st.markdown("<div style='margin-top: 1.6rem;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="font-size: 1.15rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.2rem;">
            📊 Bharat360 at a Glance
        </div>
        <div style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 0.85rem;">
            Live dynamic aggregations synthesized across all four connected public service datasets.
        </div>
        """,
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    with m1:
        st.markdown(
            f"""
            <div class="b360-ref-glance-card" style="border-top: 2.5px solid #2563EB;">
                <div class="b360-ref-glance-num" style="color: #60A5FA;">{summary_metrics['institutions']}</div>
                <div class="b360-ref-glance-label">Institutions</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f"""
            <div class="b360-ref-glance-card" style="border-top: 2.5px solid #EF4444;">
                <div class="b360-ref-glance-num" style="color: #F87171;">{summary_metrics['hospitals']}</div>
                <div class="b360-ref-glance-label">Hospitals</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f"""
            <div class="b360-ref-glance-card" style="border-top: 2.5px solid #10B981;">
                <div class="b360-ref-glance-num" style="color: #34D399;">{summary_metrics['crops']}</div>
                <div class="b360-ref-glance-label">Crops Mapped</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            f"""
            <div class="b360-ref-glance-card" style="border-top: 2.5px solid #F59E0B;">
                <div class="b360-ref-glance-num" style="color: #FBBF24;">{summary_metrics['schemes']}</div>
                <div class="b360-ref-glance-label">Public Schemes</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m5:
        st.markdown(
            f"""
            <div class="b360-ref-glance-card" style="border-top: 2.5px solid #8B5CF6;">
                <div class="b360-ref-glance-num" style="color: #A78BFA;">{summary_metrics['transit']}</div>
                <div class="b360-ref-glance-label">Transit Routes</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m6:
        st.markdown(
            """
            <div class="b360-ref-glance-card" style="border-top: 2.5px solid #38BDF8;">
                <div class="b360-ref-glance-num" style="color: #38BDF8;">100%</div>
                <div class="b360-ref-glance-label">Rule-Based AI</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 5. The Bharat360 Citizen Journey
    st.markdown("<div style='margin-top: 1.4rem;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="font-size: 1.15rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.2rem;">
            🌟 The Bharat360 Citizen Journey
        </div>
        <div style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 0.85rem;">
            How Bharat360 synthesizes data to support informed civic decisions:
        </div>
        """,
        unsafe_allow_html=True,
    )

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(
            """
            <div class="b360-ref-glance-card" style="text-align: left; padding: 18px 18px;">
                <div style="font-size: 1.5rem; margin-bottom: 6px;">1️⃣</div>
                <div style="font-weight: 700; color: #FFFFFF; font-size: 0.96rem; margin-bottom: 4px;">Choose Domain</div>
                <p style="font-size: 0.82rem; color: #94A3B8; margin: 0; line-height: 1.45;">Select Education, Healthcare, Agriculture, or Governance.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with s2:
        st.markdown(
            """
            <div class="b360-ref-glance-card" style="text-align: left; padding: 18px 18px;">
                <div style="font-size: 1.5rem; margin-bottom: 6px;">2️⃣</div>
                <div style="font-weight: 700; color: #FFFFFF; font-size: 0.96rem; margin-bottom: 4px;">Set Profile</div>
                <p style="font-size: 0.82rem; color: #94A3B8; margin: 0; line-height: 1.45;">Specify district, education level, crop demand, or income tier.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with s3:
        st.markdown(
            """
            <div class="b360-ref-glance-card" style="text-align: left; padding: 18px 18px;">
                <div style="font-size: 1.5rem; margin-bottom: 6px;">3️⃣</div>
                <div style="font-weight: 700; color: #FFFFFF; font-size: 0.96rem; margin-bottom: 4px;">Smart Match</div>
                <p style="font-size: 0.82rem; color: #94A3B8; margin: 0; line-height: 1.45;">Transparent rule engines evaluate dataset attributes with zero hallucination.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with s4:
        st.markdown(
            """
            <div class="b360-ref-glance-card" style="text-align: left; padding: 18px 18px;">
                <div style="font-size: 1.5rem; margin-bottom: 6px;">4️⃣</div>
                <div style="font-weight: 700; color: #FFFFFF; font-size: 0.96rem; margin-bottom: 4px;">Track Impact</div>
                <p style="font-size: 0.82rem; color: #94A3B8; margin: 0; line-height: 1.45;">Inspect verified analytics and personalized Viksit Bharat readiness.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_compact_footer()


def main():
    """Main routing and sidebar execution controller."""
    _init_global_state()
    inject_master_styles()

    # Dark Navy Civic-Tech Sidebar Brand Header
    st.sidebar.markdown(
        """
        <div class="b360-sidebar-brand-ref">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 2px;">
                <span style="font-size: 1.3rem;">🇮🇳</span>
                <span style="font-size: 1.22rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.5px;">
                    BHARAT<span style="color:#F59E0B">3</span><span style="color:#38BDF8">6</span><span style="color:#10B981">0</span>
                </span>
            </div>
            <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 500;">
                One Platform. Multiple Needs.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    current_page = st.session_state.get("current_page", "🏠 Home")
    nav_index = NAV_OPTIONS.index(current_page) if current_page in NAV_OPTIONS else 0

    selected_module = st.sidebar.radio(
        "Select Domain:",
        NAV_OPTIONS,
        index=nav_index,
    )

    if selected_module != current_page:
        navigate_to(selected_module)

    if current_page != "🏠 Home":
        if st.sidebar.button("← Back to Bharat360 Home", key="sidebar_back_home", use_container_width=True):
            navigate_to("🏠 Home")

    st.sidebar.markdown("---")

    st.sidebar.markdown(
        """
        <div style="font-size: 0.80rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">
            📍 Citizen Region Context
        </div>
        """,
        unsafe_allow_html=True,
    )
    selected_state = st.sidebar.selectbox(
        "State",
        ["Andhra Pradesh", "Telangana", "Karnataka", "Tamil Nadu", "Maharashtra"],
        index=0,
        key="sidebar_global_state",
    )
    st.session_state["global_state"] = selected_state

    selected_city = st.sidebar.selectbox(
        "District / City",
        ["Kakinada", "Visakhapatnam", "Vijayawada", "Rajahmundry", "Guntur"],
        index=0,
        key="sidebar_global_city",
    )
    st.session_state["global_city"] = selected_city

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style="padding-top: 4px; display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 1.05rem;">🇮🇳</span>
            <span style="font-size: 0.78rem; font-weight: 700; color: #CBD5E1; letter-spacing: 0.5px;">
                Viksit Bharat 2047
            </span>
        </div>
        <div style="font-size: 0.72rem; color: #64748B; margin-top: 4px; line-height: 1.4;">
            4 Connected Public Domains • Dynamic Data Grounding
        </div>
        """,
        unsafe_allow_html=True,
    )

    active_nav = st.session_state.get("current_page", "🏠 Home")

    if active_nav != "🏠 Home":
        col_back, col_info = st.columns([2.5, 7.5])
        with col_back:
            if st.button("← Back to Bharat360 Home", key="top_back_home", use_container_width=True):
                navigate_to("🏠 Home")
        with col_info:
            st.markdown(
                f"<div style='text-align: right; padding-top: 5px; color: #94A3B8; font-size: 0.85rem;'>"
                f"Active Section: <strong style='color: #FFFFFF;'>{active_nav}</strong></div>",
                unsafe_allow_html=True,
            )
        st.markdown("<div style='margin-bottom: 6px;'></div>", unsafe_allow_html=True)

    if active_nav == "🏠 Home":
        render_landing_page()
    elif active_nav == "🎓 Education & Skills":
        render_education_module()
        render_compact_footer()
    elif active_nav == "🏥 Healthcare & Public Services":
        render_healthcare_module()
        render_compact_footer()
    elif active_nav == "🌾 Agriculture & Sustainability":
        render_agriculture_module()
        render_compact_footer()
    elif active_nav == "🏛️ Governance, Finance & Mobility":
        render_governance_module()
        render_compact_footer()
    elif active_nav == "🇮🇳 My Bharat360":
        render_my_bharat360_module()


if __name__ == "__main__":
    main()
