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


def render_landing_page():
    """Renders the executive, Indian civic-tech Landing Page for Bharat360."""
    inject_master_styles()
    render_brand_bar()

    # 1. Executive Hero Section
    st.markdown(
        """
        <div class="b360-landing-hero">
            <div style="font-size: 2.2rem; margin-bottom: 2px;">🇮🇳</div>
            <h1 class="b360-landing-title">BHARAT360</h1>
            <div class="b360-landing-subtitle">One Platform. Multiple Needs.</div>
            <p class="b360-landing-desc">
                Supporting the vision of <strong>Viksit Bharat 2047</strong>. A unified, AI-powered public intelligence
                dashboard empowering citizens, students, farmers, and administrators with localized, rule-based decision support.
            </p>
            <div>
                <span class="b360-tag-pill">🏛️ National Civic-Tech</span>
                <span class="b360-tag-pill">🤖 Explainable AI Engine</span>
                <span class="b360-tag-pill">🌱 Resource Efficiency</span>
                <span class="b360-tag-pill">🔒 100% Grounded in Verified Data</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Hero CTA Buttons
    cta_c1, cta_c2, cta_c3 = st.columns([1.6, 1.6, 3])
    with cta_c1:
        if st.button("🚀 Explore All Services", key="hero_btn_explore", use_container_width=True):
            navigate_to("🇮🇳 My Bharat360")
    with cta_c2:
        if st.button("🌾 Agriculture Module", key="hero_btn_agri", use_container_width=True):
            navigate_to("🌾 Agriculture & Sustainability")

    st.markdown("<div style='margin-bottom: 1.2rem;'></div>", unsafe_allow_html=True)

    # 2. National Impact Metrics Row (4-Column Layout)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            """
            <div class="b360-metric-card" style="border-top: 3px solid #0284C7;">
                <div class="b360-metric-num" style="color: #0284C7;">24+</div>
                <div class="b360-metric-label">Institutions & Colleges</div>
                <small style="color: #64748B;">Degree, Polytechnic & IT</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            """
            <div class="b360-metric-card" style="border-top: 3px solid #0E7490;">
                <div class="b360-metric-num" style="color: #0E7490;">15+</div>
                <div class="b360-metric-label">Hospitals & Centers</div>
                <small style="color: #64748B;">Public & Specialized Health</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            """
            <div class="b360-metric-card" style="border-top: 3px solid #16A34A;">
                <div class="b360-metric-num" style="color: #16A34A;">100%</div>
                <div class="b360-metric-label">Water Efficiency Rule Engine</div>
                <small style="color: #64748B;">Rainfall & Crop Precision</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            """
            <div class="b360-metric-card" style="border-top: 3px solid #D97706;">
                <div class="b360-metric-num" style="color: #D97706;">12+</div>
                <div class="b360-metric-label">Public Schemes & Transit</div>
                <small style="color: #64748B;">DBT, Credit & Urban Mobility</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

    # 3. Four Major Domain Dashboard Cards (2x2 Grid)
    st.markdown("### 🏛️ **Select a Bharat360 Public Domain**")
    st.caption("Access personalized resources, localized intelligence, and AI-powered recommendations across all four critical pillars.")

    d_col1, d_col2 = st.columns(2)

    # Card 1: Education & Skills
    with d_col1:
        st.markdown(
            """
            <div class="b360-domain-card" style="border-top: 4px solid #0284C7;">
                <div class="b360-domain-icon">🎓</div>
                <div class="b360-domain-title">Education & Skills</div>
                <div style="font-size: 0.85rem; color: #0284C7; font-weight: 600; margin-bottom: 6px;">
                    Scholarships, institutions and skill opportunities
                </div>
                <div class="b360-domain-desc">
                    Search certified universities, colleges, and polytechnics. Discover fee-free government scholarships
                    and skill-building bootcamps matched to your education level.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore Education & Skills →", key="card_btn_edu", use_container_width=True):
            navigate_to("🎓 Education & Skills")

    # Card 2: Healthcare & Public Services
    with d_col2:
        st.markdown(
            """
            <div class="b360-domain-card" style="border-top: 4px solid #0E7490;">
                <div class="b360-domain-icon">🏥</div>
                <div class="b360-domain-title">Healthcare & Public Services</div>
                <div style="font-size: 0.85rem; color: #0E7490; font-weight: 600; margin-bottom: 6px;">
                    Find healthcare resources and public services
                </div>
                <div class="b360-domain-desc">
                    Locate verified government hospitals and community health centers. Explore cashless Ayushman Bharat PM-JAY
                    services, emergency trauma care, and citizen wellness advisories.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore Healthcare & Services →", key="card_btn_health", use_container_width=True):
            navigate_to("🏥 Healthcare & Public Services")

    st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)
    d_col3, d_col4 = st.columns(2)

    # Card 3: Agriculture & Sustainability
    with d_col3:
        st.markdown(
            """
            <div class="b360-domain-card" style="border-top: 4px solid #16A34A;">
                <div class="b360-domain-icon">🌾</div>
                <div class="b360-domain-title">Agriculture & Sustainability</div>
                <div style="font-size: 0.85rem; color: #16A34A; font-weight: 600; margin-bottom: 6px;">
                    Explore farming and resource-efficiency solutions
                </div>
                <div class="b360-domain-desc">
                    Access district-level rainfall analytics, water-requirement crop profiles, rule-based irrigation
                    matching, and green farm sustainability initiatives for climate resilience.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore Agriculture & Sustainability →", key="card_btn_agri", use_container_width=True):
            navigate_to("🌾 Agriculture & Sustainability")

    # Card 4: Governance, Finance & Mobility
    with d_col4:
        st.markdown(
            """
            <div class="b360-domain-card" style="border-top: 4px solid #D97706;">
                <div class="b360-domain-icon">🏛️</div>
                <div class="b360-domain-title">Governance, Finance & Mobility</div>
                <div style="font-size: 0.85rem; color: #D97706; font-weight: 600; margin-bottom: 6px;">
                    Discover schemes, financial resources and mobility
                </div>
                <div class="b360-domain-desc">
                    Find central and state welfare schemes with verified eligibility checklists, micro-credit financial inclusion
                    models, and municipal transit routes for daily commuting.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore Governance & Mobility →", key="card_btn_gov", use_container_width=True):
            navigate_to("🏛️ Governance, Finance & Mobility")

    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

    # 4. How Bharat360 Works (Citizen Journey in 4 Steps)
    st.markdown("### 🌟 **The Bharat360 Citizen Journey**")
    st.caption("How Bharat360 synthesizes data to support informed civic decisions:")

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(
            """
            <div class="b360-card" style="text-align: center;">
                <div style="font-size: 1.6rem; color: #0284C7; font-weight: 800;">1️⃣</div>
                <h4 style="margin: 4px 0; font-size: 1rem;">Choose Domain</h4>
                <p style="font-size: 0.82rem; color: #64748B;">Select Education, Healthcare, Agriculture, or Governance.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with s2:
        st.markdown(
            """
            <div class="b360-card" style="text-align: center;">
                <div style="font-size: 1.6rem; color: #0E7490; font-weight: 800;">2️⃣</div>
                <h4 style="margin: 4px 0; font-size: 1rem;">Set Profile</h4>
                <p style="font-size: 0.82rem; color: #64748B;">Specify district, education level, crop demand, or income tier.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with s3:
        st.markdown(
            """
            <div class="b360-card" style="text-align: center;">
                <div style="font-size: 1.6rem; color: #16A34A; font-weight: 800;">3️⃣</div>
                <h4 style="margin: 4px 0; font-size: 1rem;">Smart Match</h4>
                <p style="font-size: 0.82rem; color: #64748B;">Transparent rule engines evaluate dataset attributes with zero hallucination.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with s4:
        st.markdown(
            """
            <div class="b360-card" style="text-align: center;">
                <div style="font-size: 1.6rem; color: #D97706; font-weight: 800;">4️⃣</div>
                <h4 style="margin: 4px 0; font-size: 1rem;">Track Impact</h4>
                <p style="font-size: 0.82rem; color: #64748B;">Inspect Plotly analytics and personalized Viksit Bharat readiness.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_compact_footer()


def main():
    """Main routing and sidebar execution controller."""
    _init_global_state()
    inject_master_styles()

    # Redesigned Professional Sidebar Navigation
    st.sidebar.markdown(
        """
        <div class="b360-sidebar-brand">
            <div style="font-size: 1.8rem; margin-bottom: 2px;">🇮🇳</div>
            <h3 style="margin: 0; color: #0B2545; font-weight: 800; letter-spacing: -0.5px;">BHARAT360</h3>
            <p style="margin: 2px 0 0 0; font-size: 0.75rem; color: #E65100; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">
                One Platform. Multiple Needs.
            </p>
            <span style="display: inline-block; background: #E0F2FE; color: #0369A1; font-size: 0.72rem; padding: 2px 8px; border-radius: 10px; font-weight: 600; margin-top: 6px;">
                🇮🇳 Viksit Bharat 2047
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Navigation Radio synced with current_page state (no widget key collision)
    current_page = st.session_state.get("current_page", "🏠 Home")
    nav_index = NAV_OPTIONS.index(current_page) if current_page in NAV_OPTIONS else 0

    selected_module = st.sidebar.radio(
        "Select Domain:",
        NAV_OPTIONS,
        index=nav_index,
    )

    # Sync state if changed via sidebar radio click
    if selected_module != current_page:
        navigate_to(selected_module)

    # Back to Home button in sidebar when on any domain dashboard
    if current_page != "🏠 Home":
        if st.sidebar.button("← Back to Bharat360 Home", key="sidebar_back_home", use_container_width=True):
            navigate_to("🏠 Home")

    st.sidebar.markdown("---")

    # Global Citizen Location Quick-Filter
    st.sidebar.markdown(
        """
        <div style="font-size: 0.85rem; font-weight: 700; color: #0B2545; margin-bottom: 4px;">
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
        <div style="font-size: 0.78rem; color: #64748B; line-height: 1.4;">
            <strong>System Status:</strong><br>
            🟢 4/4 Core Modules Active<br>
            📊 100% Dynamic CSV Datasets<br>
            🚀 Open Innovation Challenge
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Active Page Router
    active_nav = st.session_state.get("current_page", "🏠 Home")

    # Top Back Button Bar on all domain dashboards
    if active_nav != "🏠 Home":
        col_back, col_info = st.columns([3, 7])
        with col_back:
            if st.button("← Back to Bharat360 Home", key="top_back_home", use_container_width=True):
                navigate_to("🏠 Home")
        with col_info:
            st.markdown(
                f"<div style='text-align: right; padding-top: 6px; color: #64748B; font-size: 0.88rem;'>"
                f"Active Section: <strong>{active_nav}</strong></div>",
                unsafe_allow_html=True,
            )
        st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

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
