"""
governance.py
Main module for Bharat360: Governance, Finance & Mobility.
Exposes render_governance_module() for seamless integration into the unified Bharat360 app.
Follows the Bharat360 identity, incorporates responsive UI, explainable recommendations,
and strict informational disclaimers.
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

# City coordinates mapping for Andhra Pradesh and major hubs
KNOWN_CITY_COORDINATES = {
    "kakinada": {"lat": 16.9891, "lon": 82.2475},
    "vijayawada": {"lat": 16.5062, "lon": 80.6480},
    "visakhapatnam": {"lat": 17.6868, "lon": 83.2185},
    "rajahmundry": {"lat": 17.0005, "lon": 81.8040},
    "hyderabad": {"lat": 17.3850, "lon": 78.4867},
    "amaravati": {"lat": 16.5417, "lon": 80.5158},
    "tirupati": {"lat": 13.6288, "lon": 79.4192},
}


def _apply_custom_styles():
    """Inject lightweight modern styling matching Bharat360 identity."""
    st.markdown(
        """
        <style>
        /* Bharat360 Brand Accent Bar */
        .b360-brand-bar {
            height: 4px;
            background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
            border-radius: 2px;
            margin-bottom: 1.2rem;
        }

        /* Hero Header */
        .b360-hero-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: inherit;
            margin-bottom: 0.2rem;
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }
        .b360-hero-sub {
            font-size: 1.05rem;
            color: #64748B;
            margin-bottom: 1rem;
            font-weight: 400;
        }

        /* Card Container */
        .b360-card {
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 12px;
            padding: 1.2rem 1.4rem;
            margin-bottom: 1rem;
            background: rgba(255, 255, 255, 0.03);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        .b360-card:hover {
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
        }

        /* Badges */
        .b360-badge {
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.25rem 0.65rem;
            border-radius: 9999px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-right: 0.4rem;
            margin-bottom: 0.4rem;
        }
        .b360-badge-cat {
            background-color: #E0F2FE;
            color: #0369A1;
        }
        .b360-badge-target {
            background-color: #FEF3C7;
            color: #92400E;
        }
        .b360-badge-score {
            background-color: #DCFCE7;
            color: #166534;
        }

        /* Disclaimer Callouts */
        .b360-disclaimer {
            border-left: 4px solid #F59E0B;
            background: rgba(245, 158, 11, 0.08);
            padding: 0.8rem 1.2rem;
            border-radius: 0 8px 8px 0;
            font-size: 0.88rem;
            margin-bottom: 1.2rem;
        }
        .b360-disclaimer-info {
            border-left: 4px solid #3B82F6;
            background: rgba(59, 130, 246, 0.08);
            padding: 0.8rem 1.2rem;
            border-radius: 0 8px 8px 0;
            font-size: 0.88rem;
            margin-bottom: 1.2rem;
        }
        </style>
        <div class="b360-brand-bar"></div>
        """,
        unsafe_allow_html=True,
    )


def _render_hero_section(schemes_count: int, financial_count: int, transport_count: int, cities_count: int):
    """Render the standard Hero Header with metrics and high-level prototype notice."""
    st.markdown(
        """
        <div class="b360-hero-title">
            <span>🏛️</span>
            <span>Governance, Finance & Mobility</span>
        </div>
        <div class="b360-hero-sub">
            Discover government opportunities, financial resources and mobility services.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Key metrics row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="Verified Schemes", value=schemes_count, help="Active public schemes in dataset")
    with m2:
        st.metric(label="Financial Programs", value=financial_count, help="Financial inclusion focus areas")
    with m3:
        st.metric(label="Mobility Services", value=transport_count, help="Public transit and rail lines")
    with m4:
        st.metric(label="Connected Cities", value=cities_count, help="Municipalities mapped in database")

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

    # Extract dynamic states and cities from transport dataset
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
            age = st.number_input("Age", min_value=18, max_value=99, value=int(curr.get("age", 28)), step=1)

        with p_col2:
            default_state_idx = state_options.index(curr.get("state", "Andhra Pradesh")) if curr.get("state") in state_options else 0
            state = st.selectbox("State", options=state_options, index=default_state_idx)

        # Dynamic city list based on selected state
        city_options = ["All Cities"]
        if not df_transport.empty and "city" in df_transport.columns:
            if state != "All India" and "state" in df_transport.columns:
                filtered_cities = df_transport[df_transport["state"] == state]["city"].dropna().unique()
            else:
                filtered_cities = df_transport["city"].dropna().unique()
            city_options.extend(sorted(filtered_cities))

        with p_col3:
            default_city_idx = city_options.index(curr.get("city", "All Cities")) if curr.get("city") in city_options else 0
            city = st.selectbox("City", options=city_options, index=default_city_idx)

        with p_col4:
            default_occ_idx = occupations.index(curr.get("occupation", "General Citizen")) if curr.get("occupation") in occupations else 0
            occupation = st.selectbox("Occupation", options=occupations, index=default_occ_idx)

        with p_col5:
            default_int_idx = interests.index(curr.get("interest", "All Categories")) if curr.get("interest") in interests else 0
            interest = st.selectbox("Primary Interest", options=interests, index=default_int_idx)

    # Save to session_state
    updated_profile = {
        "age": age,
        "state": state,
        "city": city,
        "occupation": occupation,
        "interest": interest,
    }
    st.session_state.b360_citizen_profile = updated_profile

    # Active profile pill summary
    st.markdown(
        f"""
        <div style="font-size: 0.85rem; color: #475569; margin-bottom: 1rem;">
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
    Render Tab 1: Personalized Citizen Dashboard (🤖 My Bharat360 Recommendations).
    Shows explainable rule-based recommendations across schemes, finance, and transport.
    """
    st.markdown("### 🤖 My Bharat360 Recommendations")
    st.markdown(
        "Personalized discovery tailored to your profile using transparent, rule-based matching. "
        "Review why each resource is suggested for your profile below."
    )

    recs = get_personalized_recommendations(profile, df_schemes, df_financial, df_transport)

    # Top cross-domain highlights cards
    st.markdown("#### 🌟 Top Matched Highlights")
    h1, h2, h3 = st.columns(3)

    with h1:
        st.markdown("**🏛️ Recommended Scheme**")
        top_s = recs["top_scheme"]
        if top_s:
            st.markdown(
                f"""
                <div class="b360-card" style="border-top: 3px solid #0284C7;">
                    <div style="font-size: 1.1rem; font-weight: 700;">{top_s['title']}</div>
                    <span class="b360-badge b360-badge-cat">{top_s['category']}</span>
                    <span class="b360-badge b360-badge-score">{top_s['score']}% Match</span>
                    <p style="margin-top: 0.6rem; font-size: 0.9rem;"><strong>Key Benefit:</strong> {top_s['benefit']}</p>
                    <div style="font-size: 0.82rem; color: #166534; background: #DCFCE7; padding: 0.4rem 0.6rem; border-radius: 6px;">
                        {top_s['reasons'][0] if top_s['reasons'] else 'General citizen match'}
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
                <div class="b360-card" style="border-top: 3px solid #10B981;">
                    <div style="font-size: 1.1rem; font-weight: 700;">{top_f['title']}</div>
                    <span class="b360-badge b360-badge-cat">{top_f['category']}</span>
                    <span class="b360-badge b360-badge-score">{top_f['score']}% Match</span>
                    <p style="margin-top: 0.6rem; font-size: 0.9rem;"><strong>Purpose:</strong> {top_f['benefit']}</p>
                    <div style="font-size: 0.82rem; color: #166534; background: #DCFCE7; padding: 0.4rem 0.6rem; border-radius: 6px;">
                        {top_f['reasons'][0] if top_f['reasons'] else 'Universal financial literacy'}
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
                <div class="b360-card" style="border-top: 3px solid #F59E0B;">
                    <div style="font-size: 1.1rem; font-weight: 700;">{top_t['title']}</div>
                    <span class="b360-badge b360-badge-cat">{top_t['category']}</span>
                    <span class="b360-badge b360-badge-score">{top_t['score']}% Match</span>
                    <p style="margin-top: 0.6rem; font-size: 0.9rem;"><strong>Mobility Focus:</strong> {top_t['benefit']}</p>
                    <div style="font-size: 0.82rem; color: #166534; background: #DCFCE7; padding: 0.4rem 0.6rem; border-radius: 6px;">
                        {top_t['reasons'][0] if top_t['reasons'] else 'Regional public transport'}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info("No transport routes available.")

    # All Recommendations with Explainability
    st.markdown("---")
    st.markdown("#### 📋 Detailed Recommendations with Transparent Rationale")

    domain_filter = st.radio(
        "Filter recommendation view:",
        options=["All Services", "Government Schemes", "Financial Inclusion", "Mobility"],
        horizontal=True,
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
                    f"<span class='b360-badge b360-badge-cat'>{item['type']}</span>"
                    f"<span class='b360-badge b360-badge-target'>{item['category']}</span>"
                    f"<span style='font-size:0.85rem; color:#64748B;'>Target Group: <strong>{item['target_group']}</strong></span>",
                    unsafe_allow_html=True,
                )
                st.write(f"**Value / Benefit:** {item['benefit']}")

                # Transparent explainability section
                st.markdown("**Why this was recommended for your profile:**")
                for reason in item["reasons"]:
                    st.markdown(f"- {reason}")

            with col_score:
                st.metric("Profile Match", f"{item['score']}%")
                if item["type"] == "Government Scheme":
                    st.caption("ℹ️ *Verify eligibility via official nodal agency.*")
                elif item["type"] == "Financial Inclusion":
                    st.caption("ℹ️ *Informational resource; not investment advice.*")
                elif item["type"] == "Mobility":
                    st.caption("ℹ️ *Subject to municipal schedule updates.*")

            st.markdown("<hr style='margin:0.8rem 0; opacity:0.2;'>", unsafe_allow_html=True)


def _render_schemes_tab(profile: Dict[str, Any], df_schemes: pd.DataFrame):
    """
    Render Tab 2: Government Scheme Finder.
    Includes search, category/target group filters, profile matching badges,
    and mandatory eligibility disclaimer.
    """
    st.markdown("### 🏛️ Government Scheme Finder")
    st.markdown("Discover central and state public welfare programs, subsidies, and income support initiatives.")

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

    # Filter controls
    f_col1, f_col2, f_col3, f_col4 = st.columns([2, 1.5, 1.5, 1.2])

    with f_col1:
        search_query = st.text_input("🔍 Search schemes, benefits, or keywords", placeholder="e.g. Kisan, Health, Digital, Skill...")

    categories = sorted(df_schemes["category"].dropna().unique().tolist())
    with f_col2:
        selected_categories = st.multiselect("Category", options=categories, default=[])

    target_groups = sorted(df_schemes["target_group"].dropna().unique().tolist())
    with f_col3:
        selected_targets = st.multiselect("Target Group", options=target_groups, default=[])

    with f_col4:
        match_only = st.checkbox("Profile Fit Only", value=False, help="Filter to schemes with high profile alignment")

    # Apply filters dynamically
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

    # Calculate profile matches for display
    recs = recommend_schemes(profile, filtered_df)
    rec_score_map = {r["title"]: r["score"] for r in recs}
    rec_reason_map = {r["title"]: r["reasons"] for r in recs}

    if match_only:
        filtered_df = filtered_df[filtered_df["scheme"].apply(lambda s: rec_score_map.get(s, 0) >= 50)]

    st.markdown(f"**Showing {len(filtered_df)} of {len(df_schemes)} schemes**")

    if filtered_df.empty:
        st.info("No schemes match your filter criteria. Try clearing some filters or searching with different terms.")
        return

    # Render scheme cards
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
                <div class="b360-card">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <h4 style="margin:0; font-size:1.15rem;">{scheme_name}</h4>
                        <span class="b360-badge b360-badge-score">{score}% Fit</span>
                    </div>
                    <div style="margin-top:0.4rem;">
                        <span class="b360-badge b360-badge-cat">{category}</span>
                        <span class="b360-badge b360-badge-target">{target}</span>
                    </div>
                    <p style="margin:0.6rem 0 0.4rem 0; font-size:0.92rem;">
                        <strong>Key Benefit:</strong> {benefit}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Verification Guidance Expander
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
    st.markdown(
        "Empowering citizens and micro-entrepreneurs with essential financial awareness, "
        "banking accessibility, and risk protection knowledge."
    )

    # Mandatory Disclaimer Banner
    st.markdown(
        """
        <div class="b360-disclaimer">
            <strong>🛡️ Financial Awareness Notice:</strong><br>
            Bharat360 provides educational awareness regarding public banking facilities,
            digital payment safety, microcredit awareness, and social security insurance.
            <strong>Bharat360 does not provide personalized financial, legal, or investment advice.</strong>
            Please consult licensed banking correspondents or certified financial institutions for financial transactions.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df_financial.empty:
        st.warning("No financial inclusion records found in dataset.")
        return

    # 5 standard financial areas
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
            # Filter rows for this area or service
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
                            <div class="b360-card">
                                <div style="display:flex; justify-content:space-between;">
                                    <strong>{svc}</strong>
                                    <span class="b360-badge b360-badge-score">{score}% Profile Match</span>
                                </div>
                                <div style="margin: 0.3rem 0;">
                                    <span class="b360-badge b360-badge-cat">Area: {area}</span>
                                    <span class="b360-badge b360-badge-target">For: {target}</span>
                                </div>
                                <div style="font-size: 0.9rem;"><strong>Core Purpose:</strong> {purpose}</div>
                                <div style="font-size: 0.82rem; color: #15803D; margin-top: 0.4rem;">
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
                    <div style="font-size:0.8rem; color:#64748B; margin-top:1rem; border-top:1px solid #E2E8F0; padding-top:0.6rem;">
                        <strong>Safety Rule:</strong> No bank official will ever ask for your PIN, CVV, or OTP over telephone or SMS.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def _render_mobility_tab(profile: Dict[str, Any], df_transport: pd.DataFrame):
    """
    Render Tab 4: Mobility & Public Transit.
    Uses transport.csv. Allows filtering by State, City, Transport mode, Service type.
    Displays mobility options with visual cards, table view, and an interactive Plotly map/route view.
    """
    st.markdown("### 🚆 Mobility & Public Transit Hub")
    st.markdown("Explore municipal and regional transit networks, bus connectivity, and rail routes.")

    if df_transport.empty:
        st.warning("No mobility records found in transport dataset.")
        return

    # Filters
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)

    states = sorted(df_transport["state"].dropna().unique().tolist())
    with m_col1:
        sel_states = st.multiselect("State", options=states, default=[])

    # Dynamic city filter based on selected state
    available_cities = df_transport
    if sel_states:
        available_cities = available_cities[available_cities["state"].isin(sel_states)]
    cities = sorted(available_cities["city"].dropna().unique().tolist())
    with m_col2:
        sel_cities = st.multiselect("City", options=cities, default=[])

    modes = sorted(df_transport["mode"].dropna().unique().tolist())
    with m_col3:
        sel_modes = st.multiselect("Transport Mode", options=modes, default=[])

    services = sorted(df_transport["service_type"].dropna().unique().tolist())
    with m_col4:
        sel_services = st.multiselect("Service Type", options=services, default=[])

    # Filter DataFrame
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
        # Aggregate by city for clean map bubbles
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
            size_max=22,
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
            height=320,
            showlegend=False,
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.caption("Coordinates for selected city nodes will render here.")

    # Display options: Cards or Table
    view_mode = st.radio("Display format:", options=["Cards View", "Table View"], horizontal=True)

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
                    <div class="b360-card">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                            <h4 style="margin:0; font-size:1.15rem;">{icon} {mode} — {city}</h4>
                            {'<span class="b360-badge b360-badge-score">📍 Your City</span>' if is_user_city else ''}
                        </div>
                        <div style="margin: 0.4rem 0;">
                            <span class="b360-badge b360-badge-cat">{svc_type}</span>
                            <span class="b360-badge b360-badge-target">{state}</span>
                        </div>
                        <p style="margin:0.5rem 0 0.2rem 0; font-size:0.9rem;">
                            <strong>Mobility Purpose:</strong> {purpose}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def _render_analytics_tab(df_schemes: pd.DataFrame, df_financial: pd.DataFrame, df_transport: pd.DataFrame):
    """
    Render Tab 5: Analytics.
    Interactive Plotly visualizations based on actual CSV data:
    - Schemes by Category
    - Financial Services by Area
    - Transport Services by City and Mode
    """
    st.markdown("### 📊 Governance, Finance & Mobility Analytics")
    st.markdown("Real-time visual aggregations computed directly from verified platform datasets.")

    col_a, col_b = st.columns(2)

    # 1. Schemes by Category
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
                height=340,
            )
            fig_schemes.update_traces(textposition="outside")
            st.plotly_chart(fig_schemes, use_container_width=True)
        else:
            st.info("No scheme category data to display.")

    # 2. Financial Services by Area
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
                height=340,
            )
            st.plotly_chart(fig_fin, use_container_width=True)
        else:
            st.info("No financial inclusion area data to display.")

    st.markdown("---")

    # 3. Transport Services by City and Mode
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
            color_discrete_map={"City Bus": "#0284C7", "Rail": "#F59E0B"},
            title="Public Transit Infrastructure Distribution Across Cities",
        )
        fig_trans.update_layout(
            xaxis_title="City",
            yaxis_title="Active Transit Lines",
            margin=dict(l=20, r=20, t=40, b=20),
            height=340,
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
    # 1. Custom CSS & Tricolor Brand Bar
    _apply_custom_styles()

    # 2. Dynamic Data Loading with full error safety
    data_bundle = load_all_governance_data()
    df_schemes = data_bundle["schemes"]
    df_financial = data_bundle["financial"]
    df_transport = data_bundle["transport"]
    errors = data_bundle["errors"]

    # Display dataset health warnings if any dataset failed
    if errors:
        for err in errors:
            st.warning(f"⚠️ Dataset Warning: {err}")

    schemes_count = len(df_schemes)
    financial_count = len(df_financial)
    transport_count = len(df_transport)
    cities_count = len(df_transport["city"].dropna().unique()) if not df_transport.empty and "city" in df_transport.columns else 0

    # 3. Hero Section
    _render_hero_section(schemes_count, financial_count, transport_count, cities_count)

    # 4. Citizen Profile Controller
    profile = _render_citizen_profile(df_transport)

    # 5. Tabbed Navigation
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


# Enable standalone execution for direct verification
if __name__ == "__main__":
    st.set_page_config(
        page_title="Bharat360 - Governance, Finance & Mobility",
        page_icon="🏛️",
        layout="wide",
    )
    render_governance_module()
