"""
governance.py
Main module for Bharat360: Governance, Finance & Mobility.
Exposes render_governance_module() for seamless integration into the unified Bharat360 app.
Follows the modern Indian civic-tech identity, incorporates responsive UI,
explainable rule-based recommendations, and official verification disclaimers.

Visual Hierarchy:
1. Header
2. Key Metrics: Verified Schemes | Financial Programs | Mobility Services | Connected Cities
3. Citizen Profile
4. Existing Recommendations (Tab 1)
5. Existing Scheme / Finance / Mobility Information (Tabs 2-4)
6. Analytics (Tab 5)
"""

from typing import Dict, Any, List, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from .data_loader import load_all_governance_data
from .recommender import (
    recommend_schemes,
    recommend_financial_resources,
    recommend_transport,
    get_personalized_recommendations,
)
from modules.ui_theme import inject_master_styles, render_brand_bar

KNOWN_CITY_COORDINATES = {
    "kakinada": {"lat": 16.9891, "lon": 82.2475},
    "vijayawada": {"lat": 16.5062, "lon": 80.6480},
    "visakhapatnam": {"lat": 17.6868, "lon": 83.2185},
    "rajahmundry": {"lat": 17.0005, "lon": 81.8040},
    "hyderabad": {"lat": 17.3850, "lon": 78.4867},
    "amaravati": {"lat": 16.5417, "lon": 80.5158},
    "tirupati": {"lat": 13.6288, "lon": 79.4192},
}


def _render_hero_section(schemes_count: int, financial_count: int, transport_count: int, cities_count: int):
    """Render the standard Hero Header with metrics and prototype notice."""
    inject_master_styles()
    render_brand_bar()
    st.markdown(
        """
        <div class="b360-module-header" style="border-left: 4px solid #D97706;">
            <div>
                <h1 class="b360-module-title">🏛️ Governance, Finance & Mobility</h1>
                <p class="b360-module-sub">Discover government welfare schemes, financial inclusion awareness, and municipal transit routes.</p>
            </div>
            <div>
                <span class="b360-tag-pill" style="background: #FFFBEB; color: #B45309; border: 1px solid #FDE68A;">
                    Viksit Bharat 2047 • Citizen Services
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Key metrics row: Verified Schemes | Financial Programs | Mobility Services | Connected Cities
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            f"""
            <div class="b360-metric-card" style="border-top: 3px solid #D97706;">
                <div class="b360-metric-num" style="color: #D97706;">{schemes_count}</div>
                <div class="b360-metric-label">Verified Schemes</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f"""
            <div class="b360-metric-card" style="border-top: 3px solid #16A34A;">
                <div class="b360-metric-num" style="color: #16A34A;">{financial_count}</div>
                <div class="b360-metric-label">Financial Programs</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f"""
            <div class="b360-metric-card" style="border-top: 3px solid #0284C7;">
                <div class="b360-metric-num" style="color: #0284C7;">{transport_count}</div>
                <div class="b360-metric-label">Mobility Services</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            f"""
            <div class="b360-metric-card" style="border-top: 3px solid #38BDF8;">
                <div class="b360-metric-num" style="color: #38BDF8;">{cities_count}</div>
                <div class="b360-metric-label">Connected Cities</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # High-level Prototype Notice
    st.markdown(
        """
        <div class="b360-disclaimer-info">
            <strong>🇮🇳 Bharat360 Prototype Notice:</strong>
            This module provides dynamic discovery of public governance schemes, financial inclusion awareness,
            and municipal mobility options. All data is dynamically loaded from verified datasets.
            Always confirm official requirements via scheme nodal portals.
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_citizen_profile(df_transport: pd.DataFrame) -> Dict[str, Any]:
    """
    Render citizen profile controller.
    Allows Age, State, City, Occupation, and Interest/Category.
    Persists profile in st.session_state for seamless multi-tab interaction.
    """
    if "b360_citizen_profile" not in st.session_state:
        st.session_state.b360_citizen_profile = {
            "age": 28,
            "state": "Andhra Pradesh",
            "city": "All Cities",
            "occupation": "General Citizen",
            "interest": "All Categories",
        }

    curr = st.session_state.b360_citizen_profile

    state_options = ["All India"]
    if not df_transport.empty and "state" in df_transport.columns:
        unique_states = sorted([s for s in df_transport["state"].dropna().unique() if s])
        state_options.extend(unique_states)

    occupations = [
        "General Citizen",
        "Farmer / Agriculture",
        "Student / Youth",
        "Small Business Owner / Entrepreneur",
        "Daily Wage / Worker",
        "Salaried / Professional",
        "Healthcare / Essential Worker",
        "Senior Citizen / Retired",
        "Homemaker",
    ]

    interests = [
        "All Categories",
        "Financial inclusion",
        "Healthcare",
        "Agriculture",
        "Digital public services",
        "Skills and employment",
        "Mobility & Transport",
    ]

    with st.expander("👤 **Citizen Profile & Preferences** (Click to customize recommendations)", expanded=True):
        st.caption("Customize your demographic details to receive personalized scheme, finance, and mobility recommendations.")
        p_col1, p_col2, p_col3, p_col4, p_col5 = st.columns([1, 1.2, 1.2, 1.5, 1.5])

        with p_col1:
            age = st.number_input("Age", min_value=18, max_value=99, value=int(curr.get("age", 28)), step=1, key="gov_profile_age")

        with p_col2:
            default_state_idx = state_options.index(curr.get("state", "Andhra Pradesh")) if curr.get("state") in state_options else 0
            state = st.selectbox("State", options=state_options, index=default_state_idx, key="gov_profile_state")

        city_options = ["All Cities"]
        if not df_transport.empty and "city" in df_transport.columns:
            if state != "All India" and "state" in df_transport.columns:
                filtered_cities = df_transport[df_transport["state"] == state]["city"].dropna().unique()
            else:
                filtered_cities = df_transport["city"].dropna().unique()
            city_options.extend(sorted(filtered_cities))

        with p_col3:
            default_city_idx = city_options.index(curr.get("city", "All Cities")) if curr.get("city") in city_options else 0
            city = st.selectbox("City", options=city_options, index=default_city_idx, key="gov_profile_city")

        with p_col4:
            default_occ_idx = occupations.index(curr.get("occupation", "General Citizen")) if curr.get("occupation") in occupations else 0
            occupation = st.selectbox("Occupation", options=occupations, index=default_occ_idx, key="gov_profile_occ")

        with p_col5:
            default_int_idx = interests.index(curr.get("interest", "All Categories")) if curr.get("interest") in interests else 0
            interest = st.selectbox("Primary Interest", options=interests, index=default_int_idx, key="gov_profile_int")

    updated_profile = {
        "age": age,
        "state": state,
        "city": city,
        "occupation": occupation,
        "interest": interest,
    }
    st.session_state.b360_citizen_profile = updated_profile

    st.markdown(
        f"""
        <div style="font-size: 0.84rem; color: #94A3B8; margin-bottom: 0.6rem;">
            🎯 <strong>Active Profile:</strong> {occupation} • Age {age} • {city}, {state} • Interest: <em>{interest}</em>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return updated_profile


def _render_recommendations_tab(
    profile: Dict[str, Any],
    df_schemes: pd.DataFrame,
    df_financial: pd.DataFrame,
    df_transport: pd.DataFrame,
):
    """
    Render Tab 1: Personalized Citizen Dashboard (🤖 My Recommendations).
    Shows explainable rule-based recommendations across schemes, finance, and transport.
    """
    st.markdown("### 🤖 **AI-Powered Recommendations**")
    st.caption("Personalized discovery tailored to your profile using transparent, rule-based matching.")

    recs = get_personalized_recommendations(profile, df_schemes, df_financial, df_transport)

    st.markdown("#### 🌟 Top Matched Highlights")
    h1, h2, h3 = st.columns(3)

    with h1:
        st.markdown("**🏛️ Recommended Scheme**")
        top_s = recs["top_scheme"]
        if top_s:
            st.markdown(
                f"""
                <div class="b360-card" style="border-top: 3px solid #D97706;">
                    <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF;">{top_s['title']}</div>
                    <div style="margin: 4px 0;">
                        <span class="b360-badge badge-amber">{top_s['category']}</span>
                        <span class="b360-badge badge-green">{top_s['score']}% Match</span>
                    </div>
                    <p style="margin: 4px 0 8px 0; font-size: 0.88rem; color: #CBD5E1;"><strong>Benefit:</strong> {top_s['benefit']}</p>
                    <div style="font-size: 0.8rem; color: #6EE7B7; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); padding: 6px 10px; border-radius: 8px;">
                        🎯 {top_s['reasons'][0] if top_s['reasons'] else 'General citizen match'}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info("No schemes available.")

    with h2:
        st.markdown("**💳 Priority Financial Resource**")
        top_f = recs["top_financial"]
        if top_f:
            st.markdown(
                f"""
                <div class="b360-card" style="border-top: 3px solid #16A34A;">
                    <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF;">{top_f['title']}</div>
                    <div style="margin: 4px 0;">
                        <span class="b360-badge badge-green">{top_f['category']}</span>
                        <span class="b360-badge badge-green">{top_f['score']}% Match</span>
                    </div>
                    <p style="margin: 4px 0 8px 0; font-size: 0.88rem; color: #CBD5E1;"><strong>Purpose:</strong> {top_f['benefit']}</p>
                    <div style="font-size: 0.8rem; color: #6EE7B7; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); padding: 6px 10px; border-radius: 8px;">
                        🎯 {top_f['reasons'][0] if top_f['reasons'] else 'Universal financial literacy'}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info("No financial resources available.")

    with h3:
        st.markdown("**🚆 Recommended Transit**")
        top_t = recs["top_transport"]
        if top_t:
            st.markdown(
                f"""
                <div class="b360-card" style="border-top: 3px solid #0284C7;">
                    <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF;">{top_t['title']}</div>
                    <div style="margin: 4px 0;">
                        <span class="b360-badge badge-blue">{top_t['category']}</span>
                        <span class="b360-badge badge-green">{top_t['score']}% Match</span>
                    </div>
                    <p style="margin: 4px 0 8px 0; font-size: 0.88rem; color: #CBD5E1;"><strong>Focus:</strong> {top_t['benefit']}</p>
                    <div style="font-size: 0.8rem; color: #6EE7B7; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); padding: 6px 10px; border-radius: 8px;">
                        🎯 {top_t['reasons'][0] if top_t['reasons'] else 'Regional public transport'}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info("No transport routes available.")

    st.markdown("---")
    st.markdown("#### 📋 Detailed Recommendations with Transparent Rationale")

    domain_filter = st.radio(
        "Filter recommendation view:",
        options=["All Services", "Government Schemes", "Financial Inclusion", "Mobility"],
        horizontal=True,
        key="gov_rec_domain_filter",
    )

    filtered_list = recs["combined"]
    if domain_filter == "Government Schemes":
        filtered_list = recs["schemes"]
    elif domain_filter == "Financial Inclusion":
        filtered_list = recs["financial"]
    elif domain_filter == "Mobility":
        filtered_list = recs["transport"]

    if not filtered_list:
        st.warning("No items match the current filter selection.")
        return

    for item in filtered_list:
        with st.container():
            col_main, col_score = st.columns([4, 1.2])
            with col_main:
                st.markdown(f"##### {item['title']}")
                st.markdown(
                    f"<span class='b360-badge badge-blue'>{item['type']}</span>"
                    f"<span class='b360-badge badge-amber'>{item['category']}</span>"
                    f"<span style='font-size:0.82rem; color:#64748B;'>Target Group: <strong>{item['target_group']}</strong></span>",
                    unsafe_allow_html=True,
                )
                st.write(f"**Value / Benefit:** {item['benefit']}")

                st.markdown("**Why this was recommended for your profile:**")
                for reason in item["reasons"]:
                    st.markdown(f"- {reason}")

            with col_score:
                st.metric("Profile Match", f"{item['score']}%")

            st.markdown("<hr style='margin:0.6rem 0; opacity:0.15;'>", unsafe_allow_html=True)


def _render_schemes_tab(profile: Dict[str, Any], df_schemes: pd.DataFrame):
    """
    Render Tab 2: Government Scheme Finder.
    Includes search, category/target group filters, profile matching badges,
    and mandatory eligibility disclaimer.
    """
    st.markdown("### 🏛️ Government Scheme Finder")
    st.caption("Discover central and state public welfare programs, subsidies, and income support initiatives.")

    # Mandatory Disclaimer Banner
    st.markdown(
        """
        <div class="b360-disclaimer">
            <strong>⚠️ Eligibility Disclaimer:</strong><br>
            Eligibility should always be verified through the official scheme source.
            Do not claim eligibility solely from this prototype. Formal approvals require verification
            against official guidelines and verified identity documentation.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df_schemes.empty:
        st.warning("No government scheme records found in dataset.")
        return

    f_col1, f_col2, f_col3, f_col4 = st.columns([2, 1.5, 1.5, 1.2])

    with f_col1:
        search_query = st.text_input("🔍 Search schemes, benefits, or keywords", placeholder="e.g. Kisan, Health, Digital, Skill...", key="gov_scheme_search")

    categories = sorted(df_schemes["category"].dropna().unique().tolist())
    with f_col2:
        selected_categories = st.multiselect("Category", options=categories, default=[], key="gov_scheme_cat")

    target_groups = sorted(df_schemes["target_group"].dropna().unique().tolist())
    with f_col3:
        selected_targets = st.multiselect("Target Group", options=target_groups, default=[], key="gov_scheme_target")

    with f_col4:
        match_only = st.checkbox("Profile Fit Only", value=False, help="Filter to schemes with high profile alignment", key="gov_scheme_fit_only")

    filtered_df = df_schemes.copy()

    if search_query.strip():
        q = search_query.strip().lower()
        filtered_df = filtered_df[
            filtered_df["scheme"].str.lower().str.contains(q)
            | filtered_df["category"].str.lower().str.contains(q)
            | filtered_df["benefit"].str.lower().str.contains(q)
            | filtered_df["target_group"].str.lower().str.contains(q)
        ]

    if selected_categories:
        filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]

    if selected_targets:
        filtered_df = filtered_df[filtered_df["target_group"].isin(selected_targets)]

    recs = recommend_schemes(profile, filtered_df)
    rec_score_map = {r["title"]: r["score"] for r in recs}
    rec_reason_map = {r["title"]: r["reasons"] for r in recs}

    if match_only:
        filtered_df = filtered_df[filtered_df["scheme"].apply(lambda s: rec_score_map.get(s, 0) >= 50)]

    st.markdown(f"**Showing {len(filtered_df)} of {len(df_schemes)} schemes**")

    if filtered_df.empty:
        st.info("No schemes match your filter criteria. Try clearing some filters or searching with different terms.")
        return

    card_cols = st.columns(2)
    for idx, (_, row) in enumerate(filtered_df.iterrows()):
        scheme_name = row.get("scheme", "N/A")
        category = row.get("category", "N/A")
        target = row.get("target_group", "N/A")
        benefit = row.get("benefit", "N/A")

        score = rec_score_map.get(scheme_name, 30)
        reasons = rec_reason_map.get(scheme_name, [])

        with card_cols[idx % 2]:
            st.markdown(
                f"""
                <div class="b360-card" style="border-top: 3px solid #D97706;">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <h4 style="margin:0; font-size:1.05rem; color:#FFFFFF;">{scheme_name}</h4>
                        <span class="b360-badge badge-green">{score}% Fit</span>
                    </div>
                    <div style="margin-top:0.3rem;">
                        <span class="b360-badge badge-blue">{category}</span>
                        <span class="b360-badge badge-amber">{target}</span>
                    </div>
                    <p style="margin:0.5rem 0 0.3rem 0; font-size:0.88rem; color:#CBD5E1;">
                        <strong>Key Benefit:</strong> {benefit}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander(f"📋 Official Verification Guidance for {scheme_name}"):
                st.markdown(
                    f"""
                    - **Required Documents:** Aadhaar Card, Active Bank Account with DBT enabled, Category/Income certificate if applicable.
                    - **Profile Rationale:** {reasons[0] if reasons else 'General public eligibility.'}
                    - **Official Verification:** Please visit the official central/state portal (e.g. `india.gov.in`, `pmkisan.gov.in`, or `pmjay.gov.in`) to submit official applications.
                    """
                )


def _render_financial_tab(profile: Dict[str, Any], df_financial: pd.DataFrame):
    """
    Render Tab 3: Financial Inclusion.
    Covers Banking access, Financial literacy, Digital payments, Microcredit awareness,
    and Insurance awareness. Includes strict disclaimer against personal investment advice.
    """
    st.markdown("### 💳 Financial Inclusion & Literacy Resources")
    st.caption("Empowering citizens and micro-entrepreneurs with essential financial awareness, banking accessibility, and risk protection knowledge.")

    st.markdown(
        """
        <div class="b360-disclaimer">
            <strong>🛡️ Financial Awareness Notice:</strong><br>
            Bharat360 provides educational awareness regarding public banking facilities,
            digital payment safety, microcredit awareness, and social security insurance.
            <strong>Bharat360 does not provide personalized financial, legal, or investment advice.</strong>
            Please consult licensed banking correspondents or certified financial institutions for transactions.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df_financial.empty:
        st.warning("No financial inclusion records found in dataset.")
        return

    fin_tabs = st.tabs([
        "🏦 Banking Access",
        "📚 Financial Literacy",
        "📱 Digital Payments",
        "🤝 Microcredit Awareness",
        "🛡️ Insurance Awareness"
    ])

    area_mapping = {
        0: ("Banking access", "Basic Bank Account"),
        1: ("Financial awareness", "Financial Literacy"),
        2: ("Payment access", "Digital Payments"),
        3: ("Credit access", "Microcredit Awareness"),
        4: ("Risk protection", "Insurance Awareness"),
    }

    educational_guides = {
        "Banking access": {
            "icon": "🏦",
            "guide": "Basic Savings Bank Deposit Account (BSBDA) offers zero minimum balance, free RuPay debit card, and seamless Direct Benefit Transfer (DBT) credit.",
            "tips": ["No minimum initial deposit required", "Free ATM withdrawals per month", "Eligible for government welfare transfers"],
        },
        "Financial awareness": {
            "icon": "📚",
            "guide": "Essential budgeting principles, understanding savings vs debt, building emergency savings, and identifying fraudulent get-rich-quick schemes.",
            "tips": ["Rule of 50-30-20 for household budgeting", "Always verify RBI registered NBFCs before taking loans", "Maintain an emergency fund for 3-6 months"],
        },
        "Payment access": {
            "icon": "📱",
            "guide": "Unified Payments Interface (UPI) and BHIM enable instant cashless transactions for consumers and local merchants via QR codes.",
            "tips": ["UPI PIN is only needed to SEND money, never to receive money", "Never share OTP or banking passwords", "Verify recipient name on QR scan before paying"],
        },
        "Credit access": {
            "icon": "🤝",
            "guide": "Institutional credit awareness for small vendors, artisans, and micro-enterprises under Pradhan Mantri Mudra Yojana without collateral.",
            "tips": ["Shishu Category: Loans up to ₹50,000", "Kishore Category: Loans from ₹50,000 to ₹5,00,000", "Tarun Category: Loans up to ₹10,00,000"],
        },
        "Risk protection": {
            "icon": "🛡️",
            "guide": "Affordable micro-insurance awareness covering accidental disability (PMSBY) and life cover (PMJJBY) with auto-debit facility.",
            "tips": ["PM Suraksha Bima Yojana: ₹2 Lakh accidental cover at nominal annual fee", "PM Jeevan Jyoti Bima Yojana: ₹2 Lakh life coverage for 18-50 age bracket", "Easy renewal linked to Jan Dhan savings account"],
        },
    }

    recs = recommend_financial_resources(profile, df_financial)
    rec_score_map = {r["title"]: r["score"] for r in recs}
    rec_reason_map = {r["title"]: r["reasons"] for r in recs}

    for tab_idx, (area_key, service_key) in area_mapping.items():
        with fin_tabs[tab_idx]:
            matched_rows = df_financial[
                (df_financial["area"].str.lower() == area_key.lower())
                | (df_financial["service"].str.lower() == service_key.lower())
            ]

            info = educational_guides.get(area_key, {})
            st.markdown(f"#### {info.get('icon', '💡')} {service_key}")
            st.write(info.get("guide", ""))

            c_left, c_right = st.columns([1.5, 1])

            with c_left:
                st.markdown("**Dataset Resource Records:**")
                if matched_rows.empty:
                    st.info("No specific dataset entries for this category.")
                else:
                    for _, row in matched_rows.iterrows():
                        svc = row.get("service", "N/A")
                        area = row.get("area", "N/A")
                        target = row.get("target_group", "N/A")
                        purpose = row.get("purpose", "N/A")
                        score = rec_score_map.get(svc, 40)
                        reasons = rec_reason_map.get(svc, [])

                        st.markdown(
                            f"""
                            <div class="b360-card" style="border-top: 3px solid #16A34A;">
                                <div style="display:flex; justify-content:space-between;">
                                    <strong style="color: #FFFFFF;">{svc}</strong>
                                    <span class="b360-badge badge-green">{score}% Match</span>
                                </div>
                                <div style="margin: 0.3rem 0;">
                                    <span class="b360-badge badge-blue">Area: {area}</span>
                                    <span class="b360-badge badge-amber">For: {target}</span>
                                </div>
                                <div style="font-size: 0.88rem; color: #CBD5E1;"><strong>Purpose:</strong> {purpose}</div>
                                <div style="font-size: 0.8rem; color: #6EE7B7; margin-top: 0.4rem;">
                                    💡 <em>{reasons[0] if reasons else 'Essential financial literacy topic.'}</em>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

            with c_right:
                st.markdown("**Actionable Literacy Best Practices:**")
                for tip in info.get("tips", []):
                    st.markdown(f"✅ {tip}")
                st.markdown(
                    """
                    <div style="font-size:0.78rem; color:#64748B; margin-top:0.8rem; border-top:1px solid #E2E8F0; padding-top:0.5rem;">
                        <strong>Safety Rule:</strong> No bank official will ever ask for your PIN, CVV, or OTP over telephone or SMS.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def _render_mobility_tab(profile: Dict[str, Any], df_transport: pd.DataFrame):
    """
    Render Tab 4: Mobility & Public Transit.
    Uses transport.csv. Allows filtering by State, City, Transport mode, Service type.
    """
    st.markdown("### 🚆 Mobility & Public Transit Hub")
    st.caption("Explore municipal and regional transit networks, bus connectivity, and rail routes.")

    if df_transport.empty:
        st.warning("No mobility records found in transport dataset.")
        return

    m_col1, m_col2, m_col3, m_col4 = st.columns(4)

    states = sorted(df_transport["state"].dropna().unique().tolist())
    with m_col1:
        sel_states = st.multiselect("State", options=states, default=[], key="gov_mob_state")

    available_cities = df_transport
    if sel_states:
        available_cities = available_cities[available_cities["state"].isin(sel_states)]
    cities = sorted(available_cities["city"].dropna().unique().tolist())
    with m_col2:
        sel_cities = st.multiselect("City", options=cities, default=[], key="gov_mob_city")

    modes = sorted(df_transport["mode"].dropna().unique().tolist())
    with m_col3:
        sel_modes = st.multiselect("Transport Mode", options=modes, default=[], key="gov_mob_mode")

    services = sorted(df_transport["service_type"].dropna().unique().tolist())
    with m_col4:
        sel_services = st.multiselect("Service Type", options=services, default=[], key="gov_mob_svc")

    filtered_df = df_transport.copy()
    if sel_states:
        filtered_df = filtered_df[filtered_df["state"].isin(sel_states)]
    if sel_cities:
        filtered_df = filtered_df[filtered_df["city"].isin(sel_cities)]
    if sel_modes:
        filtered_df = filtered_df[filtered_df["mode"].isin(sel_modes)]
    if sel_services:
        filtered_df = filtered_df[filtered_df["service_type"].isin(sel_services)]

    st.markdown(f"**Showing {len(filtered_df)} of {len(df_transport)} transit services**")

    if filtered_df.empty:
        st.info("No transit options match your current filter selections.")
        return

    # Visual Location / Route Map
    st.markdown("#### 🗺️ Regional Transit Hub Visualizer")
    map_data = []
    for _, r in filtered_df.iterrows():
        c_name = str(r.get("city", "")).strip().lower()
        coords = KNOWN_CITY_COORDINATES.get(c_name, None)
        if coords:
            map_data.append({
                "city": r.get("city"),
                "state": r.get("state"),
                "mode": r.get("mode"),
                "service_type": r.get("service_type"),
                "purpose": r.get("purpose"),
                "lat": coords["lat"],
                "lon": coords["lon"],
            })

    if map_data:
        map_df = pd.DataFrame(map_data)
        city_summary = map_df.groupby(["city", "state", "lat", "lon"]).agg(
            services=("service_type", lambda x: ", ".join(x.unique())),
            modes=("mode", lambda x: ", ".join(x.unique())),
            count=("mode", "count"),
        ).reset_index()

        fig_map = px.scatter_geo(
            city_summary,
            lat="lat",
            lon="lon",
            text="city",
            size="count",
            hover_name="city",
            hover_data={"state": True, "modes": True, "services": True, "lat": False, "lon": False, "count": False},
            title="Active Transit Nodes in Andhra Pradesh & Surrounding Hubs",
            size_max=20,
            color="city",
        )
        fig_map.update_geos(
            scope="asia",
            center=dict(lat=16.9, lon=81.8),
            projection_scale=6,
            showcountries=True,
            showland=True,
            landcolor="#F8FAFC",
            showrivers=True,
            rivercolor="#BAE6FD",
        )
        fig_map.update_layout(
            margin=dict(l=0, r=0, t=35, b=0),
            height=300,
            showlegend=False,
        )
        st.plotly_chart(fig_map, use_container_width=True)

    view_mode = st.radio("Display format:", options=["Cards View", "Table View"], horizontal=True, key="gov_mob_view_mode")

    if view_mode == "Table View":
        display_cols = ["id", "mode", "city", "state", "service_type", "purpose"]
        valid_cols = [c for c in display_cols if c in filtered_df.columns]
        st.dataframe(filtered_df[valid_cols], use_container_width=True, hide_index=True)
    else:
        t_cols = st.columns(2)
        for idx, (_, row) in enumerate(filtered_df.iterrows()):
            mode = row.get("mode", "N/A")
            city = row.get("city", "N/A")
            state = row.get("state", "N/A")
            svc_type = row.get("service_type", "N/A")
            purpose = row.get("purpose", "N/A")

            icon = "🚌" if "bus" in mode.lower() else "🚆"
            is_user_city = (city.lower() == str(profile.get("city", "")).lower())

            with t_cols[idx % 2]:
                st.markdown(
                    f"""
                    <div class="b360-card" style="border-top: 3px solid #0284C7;">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                            <h4 style="margin:0; font-size:1.05rem; color:#FFFFFF;">{icon} {mode} — {city}</h4>
                            {'<span class="b360-badge badge-green">📍 Your City</span>' if is_user_city else ''}
                        </div>
                        <div style="margin: 0.3rem 0;">
                            <span class="b360-badge badge-blue">{svc_type}</span>
                            <span class="b360-badge badge-amber">{state}</span>
                        </div>
                        <p style="margin:0.4rem 0 0.2rem 0; font-size:0.88rem; color:#CBD5E1;">
                            <strong>Mobility Purpose:</strong> {purpose}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def _render_analytics_tab(df_schemes: pd.DataFrame, df_financial: pd.DataFrame, df_transport: pd.DataFrame):
    """
    Render Tab 5: Analytics.
    Interactive Plotly visualizations based on actual CSV data.
    """
    st.markdown("### 📊 Governance, Finance & Mobility Analytics")
    st.caption("Real-time visual aggregations computed directly from verified platform datasets.")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### 🏛️ Schemes by Category")
        if not df_schemes.empty and "category" in df_schemes.columns:
            schemes_cat = df_schemes["category"].value_counts().reset_index()
            schemes_cat.columns = ["Category", "Count"]

            fig_schemes = px.bar(
                schemes_cat,
                x="Category",
                y="Count",
                color="Category",
                text="Count",
                color_discrete_sequence=px.colors.qualitative.Prism,
                title="Welfare Schemes Distributed Across Sectors",
            )
            fig_schemes.update_layout(
                xaxis_title="Sector Category",
                yaxis_title="Number of Schemes",
                showlegend=False,
                margin=dict(l=20, r=20, t=40, b=20),
                height=300,
            )
            fig_schemes.update_traces(textposition="outside")
            st.plotly_chart(fig_schemes, use_container_width=True)
        else:
            st.info("No scheme category data to display.")

    with col_b:
        st.markdown("#### 💳 Financial Services by Focus Area")
        if not df_financial.empty and "area" in df_financial.columns:
            fin_area = df_financial["area"].value_counts().reset_index()
            fin_area.columns = ["Focus Area", "Count"]

            fig_fin = px.pie(
                fin_area,
                names="Focus Area",
                values="Count",
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Safe,
                title="Inclusion & Awareness Domains Breakdown",
            )
            fig_fin.update_layout(
                margin=dict(l=20, r=20, t=40, b=20),
                height=300,
            )
            st.plotly_chart(fig_fin, use_container_width=True)
        else:
            st.info("No financial inclusion area data to display.")

    st.markdown("---")

    st.markdown("#### 🚆 Public Transit Services by City and Mode")
    if not df_transport.empty and "city" in df_transport.columns and "mode" in df_transport.columns:
        trans_agg = df_transport.groupby(["city", "mode"]).size().reset_index(name="Services")

        fig_trans = px.bar(
            trans_agg,
            x="city",
            y="Services",
            color="mode",
            barmode="group",
            text="Services",
            color_discrete_map={"City Bus": "#0284C7", "Rail": "#D97706"},
            title="Public Transit Infrastructure Distribution Across Cities",
        )
        fig_trans.update_layout(
            xaxis_title="City",
            yaxis_title="Active Transit Lines",
            margin=dict(l=20, r=20, t=40, b=20),
            height=300,
        )
        fig_trans.update_traces(textposition="outside")
        st.plotly_chart(fig_trans, use_container_width=True)
    else:
        st.info("No transport infrastructure data to display.")


def render_governance_module():
    """
    Main entrypoint function for the Governance + Finance + Mobility module.
    Exposed for the unified Bharat360 application.
    """
    # 1. Dynamic Data Loading
    data_bundle = load_all_governance_data()
    df_schemes = data_bundle["schemes"]
    df_financial = data_bundle["financial"]
    df_transport = data_bundle["transport"]
    errors = data_bundle["errors"]

    if errors:
        for err in errors:
            st.warning(f"⚠️ Dataset Warning: {err}")

    schemes_count = len(df_schemes)
    financial_count = len(df_financial)
    transport_count = len(df_transport)
    cities_count = len(df_transport["city"].dropna().unique()) if not df_transport.empty and "city" in df_transport.columns else 0

    # 2. Hero Section & Key Metrics
    _render_hero_section(schemes_count, financial_count, transport_count, cities_count)

    # 3. Citizen Profile Controller
    profile = _render_citizen_profile(df_transport)

    # 4. Tabbed Navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🤖 My Recommendations",
        "🏛️ Scheme Finder",
        "💳 Financial Inclusion",
        "🚆 Mobility Hub",
        "📊 Analytics",
    ])

    with tab1:
        _render_recommendations_tab(profile, df_schemes, df_financial, df_transport)

    with tab2:
        _render_schemes_tab(profile, df_schemes)

    with tab3:
        _render_financial_tab(profile, df_financial)

    with tab4:
        _render_mobility_tab(profile, df_transport)

    with tab5:
        _render_analytics_tab(df_schemes, df_financial, df_transport)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Bharat360 - Governance, Finance & Mobility",
        page_icon="🏛️",
        layout="wide",
    )
    render_governance_module()
