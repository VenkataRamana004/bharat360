"""
Bharat360 - Healthcare & Public Services Module
Member 2 Responsibility

Main Entrypoint:
render_healthcare_module()

Features:
1. Dynamic Location Filtering (State & City)
2. Hospital Finder with Cards & Map Visualization
3. Healthcare Services Catalog with Categories & Cost Tiers
4. Health Awareness Section (Informational Guidance & Advisory Disclaimer)
5. Rule-Based Healthcare Service Recommender
6. Healthcare Analytics Dashboard with Plotly
"""

import sys
from pathlib import Path
from typing import Optional
import pandas as pd
import streamlit as st

# Handle both relative package import and standalone module import
try:
    from .data_loader import (
        load_all_healthcare_data,
        get_unique_states,
        get_unique_cities,
        get_unique_managements,
        get_unique_hospital_types,
        get_unique_cost_categories,
    )
    from .recommender import recommend_healthcare_resources
except ImportError:
    # Ensure current directory is in sys.path for direct execution
    current_dir = Path(__file__).resolve().parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    from data_loader import (
        load_all_healthcare_data,
        get_unique_states,
        get_unique_cities,
        get_unique_managements,
        get_unique_hospital_types,
        get_unique_cost_categories,
    )
    from recommender import recommend_healthcare_resources


def _inject_custom_styles():
    """Injects high-contrast, clean visual styles tailored to the Bharat360 theme."""
    st.markdown(
        """
        <style>
        /* Card Containers */
        .b360-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 18px 22px;
            margin-bottom: 16px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            transition: all 0.2s ease-in-out;
        }
        .b360-card:hover {
            border-color: #0284C7;
            box-shadow: 0 4px 14px rgba(2, 132, 199, 0.12);
            transform: translateY(-2px);
        }
        .b360-card-header {
            font-size: 1.15rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .b360-card-subtitle {
            font-size: 0.9rem;
            color: #64748B;
            margin-bottom: 12px;
        }
        .b360-card-body {
            font-size: 0.95rem;
            color: #334155;
            line-height: 1.5;
            margin-bottom: 12px;
        }
        /* Pill Badges */
        .b360-badge {
            display: inline-block;
            font-size: 0.78rem;
            font-weight: 600;
            padding: 3px 10px;
            border-radius: 9999px;
            margin-right: 6px;
            margin-bottom: 6px;
        }
        .b360-badge-green {
            background-color: #DCFCE7;
            color: #166534;
            border: 1px solid #BBF7D0;
        }
        .b360-badge-blue {
            background-color: #E0F2FE;
            color: #0369A1;
            border: 1px solid #BAE6FD;
        }
        .b360-badge-purple {
            background-color: #F3E8FF;
            color: #6B21A8;
            border: 1px solid #E9D5FF;
        }
        .b360-badge-amber {
            background-color: #FEF3C7;
            color: #92400E;
            border: 1px solid #FDE68A;
        }
        .b360-badge-gray {
            background-color: #F1F5F9;
            color: #475569;
            border: 1px solid #E2E8F0;
        }
        /* Metric Box */
        .b360-stat-box {
            background: linear-gradient(135deg, #F0FDF4 0%, #E0F2FE 100%);
            border: 1px solid #CBD5E1;
            border-radius: 10px;
            padding: 14px 18px;
            text-align: center;
        }
        .b360-stat-num {
            font-size: 1.6rem;
            font-weight: 800;
            color: #0E7490;
        }
        .b360-stat-label {
            font-size: 0.85rem;
            font-weight: 600;
            color: #475569;
        }
        /* Hero Banner */
        .b360-hero-box {
            background: linear-gradient(135deg, #0F766E 0%, #0369A1 100%);
            color: #FFFFFF;
            border-radius: 14px;
            padding: 24px 28px;
            margin-bottom: 24px;
            box-shadow: 0 4px 16px rgba(15, 118, 110, 0.18);
        }
        .b360-hero-title {
            font-size: 2.1rem;
            font-weight: 800;
            margin-bottom: 6px;
            color: #FFFFFF;
        }
        .b360-hero-sub {
            font-size: 1.1rem;
            color: #E0F2FE;
            margin-bottom: 0px;
        }
        .b360-disclaimer {
            background-color: #FFFBEB;
            border-left: 4px solid #F59E0B;
            padding: 14px 18px;
            border-radius: 0 8px 8px 0;
            margin: 16px 0;
            color: #78350F;
            font-size: 0.88rem;
            line-height: 1.5;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_hero_section():
    """Renders the standard Hero banner matching the Bharat360 specification."""
    try:
        from modules.ui_theme import inject_master_styles
        inject_master_styles()
    except Exception:
        pass
    st.markdown(
        """
        <div class="b360-module-header">
            <div>
                <h1 class="b360-module-title">🏥 Healthcare & Public Services</h1>
                <p class="b360-module-sub">Find healthcare resources and public services that matter to you.</p>
            </div>
            <div>
                <span class="b360-tag-pill" style="background: #E0F2FE; color: #0369A1; border: 1px solid #BAE6FD;">
                    Viksit Bharat 2047 • Universal Health
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_kpis(df_hospitals: pd.DataFrame, df_services: pd.DataFrame, df_awareness: pd.DataFrame):
    """Renders quick metric highlights."""
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
            <div class="b360-stat-box">
                <div class="b360-stat-num">{len(df_hospitals)}</div>
                <div class="b360-stat-label">Hospitals & Centers</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="b360-stat-box">
                <div class="b360-stat-num">{len(df_services)}</div>
                <div class="b360-stat-label">Public Health Services</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
            <div class="b360-stat-box">
                <div class="b360-stat-num">{len(df_awareness)}</div>
                <div class="b360-stat-label">Awareness Guides</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        unique_cities = len(df_hospitals["city"].unique()) if not df_hospitals.empty else 0
        st.markdown(
            f"""
            <div class="b360-stat-box">
                <div class="b360-stat-num">{unique_cities}</div>
                <div class="b360-stat-label">Cities Covered</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)


def _render_hospital_card(row: pd.Series):
    """Renders a single hospital facility card."""
    name = row.get("name", "Unknown Hospital")
    city = row.get("city", "Unknown City")
    state = row.get("state", "Unknown State")
    mgmt = row.get("management", "Government")
    h_type = row.get("type", "General")
    lat = row.get("latitude")
    lon = row.get("longitude")

    coord_badge = (
        f'<span class="b360-badge b360-badge-gray">📍 Lat: {lat:.4f}, Lon: {lon:.4f}</span>'
        if pd.notnull(lat) and pd.notnull(lon)
        else '<span class="b360-badge b360-badge-gray">📍 Coordinates N/A</span>'
    )

    mgmt_badge = (
        f'<span class="b360-badge b360-badge-green">🏛️ {mgmt}</span>'
        if str(mgmt).lower() == "government"
        else f'<span class="b360-badge b360-badge-blue">🏢 {mgmt}</span>'
    )
    type_badge = f'<span class="b360-badge b360-badge-purple">🏷️ {h_type}</span>'

    card_html = f"""
    <div class="b360-card">
        <div class="b360-card-header">🏥 {name}</div>
        <div class="b360-card-subtitle">📍 <strong>{city}</strong>, {state}</div>
        <div style="margin-top: 10px;">
            {mgmt_badge}
            {type_badge}
            {coord_badge}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def _render_service_card(row: pd.Series):
    """Renders a single healthcare service card."""
    service_name = row.get("service", "Healthcare Service")
    desc = row.get("description", "Public health provision.")
    available_at = row.get("available_at", "Government facilities")
    cost_cat = str(row.get("cost_category", "Not Specified"))

    # Dynamic badge styling for cost
    cost_lower = cost_cat.lower()
    if "free" in cost_lower and "low" not in cost_lower:
        cost_badge = f'<span class="b360-badge b360-badge-green">💰 Cost: {cost_cat}</span>'
    elif "low" in cost_lower:
        cost_badge = f'<span class="b360-badge b360-badge-blue">💰 Cost: {cost_cat}</span>'
    else:
        cost_badge = f'<span class="b360-badge b360-badge-amber">💰 Cost: {cost_cat}</span>'

    # Icon detection
    srv_lower = service_name.lower()
    if "opd" in srv_lower:
        icon = "🩺"
    elif "maternal" in srv_lower:
        icon = "🤰"
    elif "immuniz" in srv_lower or "vaccin" in srv_lower:
        icon = "💉"
    elif "emergency" in srv_lower:
        icon = "🚨"
    elif "diagnostic" in srv_lower:
        icon = "🔬"
    else:
        icon = "✨"

    card_html = f"""
    <div class="b360-card">
        <div class="b360-card-header">{icon} {service_name}</div>
        <div class="b360-card-body">{desc}</div>
        <div style="font-size: 0.88rem; color: #475569; margin-bottom: 8px;">
            <strong>Available At:</strong> {available_at}
        </div>
        <div>
            {cost_badge}
            <span class="b360-badge b360-badge-gray">Civic Scheme</span>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def _render_hospital_finder_tab(df_hospitals: pd.DataFrame, default_state: str, default_city: str):
    """Renders the Hospital Finder section with filters, cards, and map."""
    st.markdown("### 🏥 Find Healthcare Facilities")
    st.caption("Locate verified government hospitals, community health centers, and specialty centers.")

    if df_hospitals.empty:
        st.info("No hospital data available. Please verify the dataset.")
        return

    # Filters row
    col1, col2, col3, col4 = st.columns([1.2, 1.2, 1.2, 1.5])

    # Available options
    states = ["All States"] + get_unique_states(df_hospitals)
    selected_state_idx = states.index(default_state) if default_state in states else 0
    with col1:
        f_state = st.selectbox("State Filter", states, index=selected_state_idx, key="hf_state_filter")

    cities = ["All Cities"] + get_unique_cities(df_hospitals, None if f_state == "All States" else f_state)
    selected_city_idx = cities.index(default_city) if default_city in cities else 0
    with col2:
        f_city = st.selectbox("City Filter", cities, index=selected_city_idx, key="hf_city_filter")

    managements = ["All Managements"] + get_unique_managements(df_hospitals)
    with col3:
        f_mgmt = st.selectbox("Management", managements, key="hf_mgmt_filter")

    types = ["All Types"] + get_unique_hospital_types(df_hospitals)
    with col4:
        f_type = st.selectbox("Hospital Type", types, key="hf_type_filter")

    search_query = st.text_input("🔍 Search Hospital by Name or Locality", "", key="hf_search_query")

    # Apply filters
    filtered_df = df_hospitals.copy()
    if f_state != "All States":
        filtered_df = filtered_df[filtered_df["state"].str.lower() == f_state.lower()]
    if f_city != "All Cities":
        filtered_df = filtered_df[filtered_df["city"].str.lower() == f_city.lower()]
    if f_mgmt != "All Managements":
        filtered_df = filtered_df[filtered_df["management"].str.lower() == f_mgmt.lower()]
    if f_type != "All Types":
        filtered_df = filtered_df[filtered_df["type"].str.lower() == f_type.lower()]
    if search_query.strip():
        q = search_query.strip().lower()
        filtered_df = filtered_df[
            filtered_df["name"].str.lower().str.contains(q, na=False) |
            filtered_df["city"].str.lower().str.contains(q, na=False)
        ]

    st.markdown(f"**Showing {len(filtered_df)} facility(ies)** matching your criteria")

    # Optional Map Display
    map_data = filtered_df.dropna(subset=["latitude", "longitude"])
    show_map = st.toggle("🗺️ Show Facilities on Interactive Map", value=True)

    if show_map:
        if not map_data.empty:
            st.caption("📍 Interactive location markers for hospitals in the filtered view.")
            st.map(map_data[["latitude", "longitude"]], zoom=8)
        else:
            st.info("No valid geographical coordinates found for the current filter.")

    st.divider()

    # Hospital Cards Display
    if filtered_df.empty:
        st.warning("No healthcare facilities matched the selected filters. Try broadening your search.")
    else:
        # Render cards in a 2-column grid
        card_cols = st.columns(2)
        for idx, (_, row) in enumerate(filtered_df.iterrows()):
            with card_cols[idx % 2]:
                _render_hospital_card(row)


def _render_services_tab(df_services: pd.DataFrame):
    """Renders Healthcare Services catalog with search and filters."""
    st.markdown("### 🩺 Public Healthcare Services")
    st.caption("Discover essential public healthcare services, eligibility, and facility types.")

    if df_services.empty:
        st.info("No health services records available.")
        return

    scol1, scol2 = st.columns([2, 1])
    with scol1:
        search_kw = st.text_input("🔍 Search Services by keyword (e.g. Immunization, OPD, Diagnostic)", "", key="serv_search")
    with scol2:
        cost_categories = ["All Costs"] + get_unique_cost_categories(df_services)
        selected_cost = st.selectbox("Filter by Cost Category", cost_categories, key="serv_cost_filter")

    filtered_services = df_services.copy()

    if selected_cost != "All Costs":
        filtered_services = filtered_services[
            filtered_services["cost_category"].str.lower() == selected_cost.lower()
        ]

    if search_kw.strip():
        kw = search_kw.strip().lower()
        filtered_services = filtered_services[
            filtered_services["service"].str.lower().str.contains(kw, na=False) |
            filtered_services["description"].str.lower().str.contains(kw, na=False) |
            filtered_services["available_at"].str.lower().str.contains(kw, na=False)
        ]

    st.markdown(f"**Available Services ({len(filtered_services)} found):**")

    if filtered_services.empty:
        st.warning("No healthcare services matched your search criteria.")
    else:
        s_cols = st.columns(2)
        for idx, (_, row) in enumerate(filtered_services.iterrows()):
            with s_cols[idx % 2]:
                _render_service_card(row)


def _render_awareness_tab(df_awareness: pd.DataFrame):
    """Renders the Health Awareness section with disclaimer and expandable cards."""
    st.markdown("### 💡 Citizen Health Awareness & Guidance")
    st.caption("Civic awareness and preventive public health advisories for everyday wellness.")

    # Mandatory Medical Advisory Callout
    st.markdown(
        """
        <div class="b360-disclaimer">
            <strong>⚠️ CITIZEN HEALTH ADVISORY & DISCLAIMER:</strong><br>
            The health awareness information provided here is strictly for public education and resource discovery 
            under the Viksit Bharat 2047 initiative. 
            <strong>It does not provide diagnosis, medical prescriptions, or personalized medical treatment recommendations.</strong><br>
            In the event of acute symptoms or a medical emergency, please dial <strong>108 (Emergency)</strong> or <strong>102 (Ambulance)</strong>, 
            or consult a certified medical practitioner immediately.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df_awareness.empty:
        st.info("No health awareness records available.")
        return

    # Filter by target group
    target_groups = ["All Groups"] + sorted(list(df_awareness["target_group"].dropna().unique()))
    selected_tg = st.selectbox("Filter by Target Group", target_groups, key="aware_tg_filter")

    filtered_awareness = df_awareness.copy()
    if selected_tg != "All Groups":
        filtered_awareness = filtered_awareness[
            filtered_awareness["target_group"].str.lower() == selected_tg.lower()
        ]

    # Topic Icons mapping
    topic_icons = {
        "hand hygiene": "🧼",
        "vaccination awareness": "💉",
        "nutrition awareness": "🥗",
        "maternal health": "🤰",
        "preventive checkups": "🩺",
    }

    for _, row in filtered_awareness.iterrows():
        topic = row.get("topic", "Health Guidance")
        guidance = row.get("guidance", "Follow regular public health advice.")
        target_group = row.get("target_group", "General public")

        icon = topic_icons.get(str(topic).strip().lower(), "📘")

        with st.expander(f"{icon} {topic} — Recommended for: {target_group}", expanded=True):
            st.markdown(f"**Guidance & Best Practice:**\n\n> {guidance}")
            st.markdown(
                f"""
                <div style="margin-top: 8px;">
                    <span class="b360-badge b360-badge-blue">🎯 Target: {target_group}</span>
                    <span class="b360-badge b360-badge-green">Civic Health Advisory</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_recommender_tab(
    df_hospitals: pd.DataFrame,
    df_services: pd.DataFrame,
    df_awareness: pd.DataFrame,
    default_state: str,
    default_city: str
):
    """Renders the Rule-Based Service Recommendation Engine."""
    st.markdown("### 🎯 Smart Healthcare Resource Recommender")
    st.caption("Receive rule-based recommendations for public health services, local facilities, and guidance.")

    # Advisory notice
    st.info("ℹ️ Recommendations are generated deterministically from verified public datasets based on your inputs.")

    with st.form("recommendation_form"):
        rcol1, rcol2, rcol3 = st.columns(3)

        with rcol1:
            age_group = st.selectbox(
                "Age Group",
                [
                    "Infants & Children (0 - 12 yrs)",
                    "Youth & Adolescents (13 - 24 yrs)",
                    "Adults (25 - 59 yrs)",
                    "Senior Citizens (60+ yrs)",
                    "Expecting / New Mothers",
                    "General / All Ages",
                ],
                key="rec_age_group",
            )

        with rcol2:
            states = ["All States"] + get_unique_states(df_hospitals)
            def_st_idx = states.index(default_state) if default_state in states else 0
            rec_state = st.selectbox("State", states, index=def_st_idx, key="rec_state_select")

            cities = ["All Cities"] + get_unique_cities(df_hospitals, None if rec_state == "All States" else rec_state)
            def_ct_idx = cities.index(default_city) if default_city in cities else 0
            rec_city = st.selectbox("City / Town", cities, index=def_ct_idx, key="rec_city_select")

        with rcol3:
            service_interest = st.selectbox(
                "Service Need / Interest",
                [
                    "General Medical Consultation (OPD)",
                    "Maternal & Prenatal Health",
                    "Child Immunization & Routine Vaccines",
                    "Emergency & Urgent Medical Assistance",
                    "Diagnostic Laboratory Tests & Screenings",
                    "Preventive Health & Wellness",
                    "Comprehensive / All Available Services",
                ],
                key="rec_service_interest",
            )

        submit_btn = st.form_submit_button("🔍 Discover Recommended Healthcare Resources", use_container_width=True)

    if submit_btn:
        res = recommend_healthcare_resources(
            age_group=age_group,
            selected_state=rec_state,
            selected_city=rec_city,
            service_interest=service_interest,
            df_hospitals=df_hospitals,
            df_services=df_services,
            df_awareness=df_awareness,
        )

        st.markdown("---")
        st.markdown("### 🤖 **AI-Powered Recommendations**")

        # Rationale Callout
        if res["rationale"]:
            with st.container():
                st.markdown("**Why these recommendations match your criteria:**")
                for r in res["rationale"]:
                    st.markdown(f"- {r}")

        st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

        # 1. Recommended Services
        st.markdown("#### 1. Matching Public Health Services")
        matched_services = res["services"]
        if matched_services.empty:
            st.warning("No specific health services matched the criteria in the dataset.")
        else:
            scols = st.columns(2)
            for idx, (_, row) in enumerate(matched_services.iterrows()):
                with scols[idx % 2]:
                    _render_service_card(row)

        # 2. Recommended Facilities
        st.markdown("#### 2. Local Healthcare Facilities")
        matched_hospitals = res["hospitals"]
        if matched_hospitals.empty:
            st.warning(f"No registered hospitals found matching {rec_city}, {rec_state} in the dataset.")
        else:
            hcols = st.columns(2)
            for idx, (_, row) in enumerate(matched_hospitals.iterrows()):
                with hcols[idx % 2]:
                    _render_hospital_card(row)

        # 3. Matched Awareness Guidance
        st.markdown("#### 3. Relevant Health Awareness Guidance")
        matched_awareness = res["awareness"]
        if matched_awareness.empty:
            st.info("No specific awareness guidance found for this category.")
        else:
            for _, row in matched_awareness.iterrows():
                topic = row.get("topic", "Health Information")
                guidance = row.get("guidance", "")
                tg = row.get("target_group", "General")
                with st.expander(f"📘 {topic} (Target: {tg})", expanded=True):
                    st.markdown(f"> {guidance}")

        # Disclaimer
        st.markdown(
            f"""
            <div class="b360-disclaimer">
                <strong>Medical Notice:</strong> {res['disclaimer']}
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_analytics_tab(df_hospitals: pd.DataFrame, df_services: pd.DataFrame):
    """Renders useful Plotly charts using actual CSV datasets."""
    st.markdown("### 📊 Healthcare Analytics & Insights")
    st.caption("Visual data analysis based on verified civic health records.")

    try:
        import plotly.express as px
    except ImportError:
        st.error("Plotly is required to display analytics charts. Please install plotly.")
        return

    tab_col1, tab_col2 = st.columns(2)

    # Chart 1: Hospitals by City
    with tab_col1:
        st.markdown("##### 🏥 Hospitals Distribution by City")
        if not df_hospitals.empty and "city" in df_hospitals.columns:
            city_counts = df_hospitals["city"].value_counts().reset_index()
            city_counts.columns = ["City", "Number of Hospitals"]
            fig_city = px.bar(
                city_counts,
                x="City",
                y="Number of Hospitals",
                color="Number of Hospitals",
                color_continuous_scale="Teal",
                text="Number of Hospitals",
            )
            fig_city.update_layout(
                margin=dict(l=20, r=20, t=30, b=30),
                coloraxis_showscale=False,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )
            fig_city.update_traces(textposition="outside")
            st.plotly_chart(fig_city, use_container_width=True)
        else:
            st.info("No city data available for chart.")

    # Chart 2: Hospitals by Management
    with tab_col2:
        st.markdown("##### 🏛️ Facilities by Management")
        if not df_hospitals.empty and "management" in df_hospitals.columns:
            mgmt_counts = df_hospitals["management"].value_counts().reset_index()
            mgmt_counts.columns = ["Management", "Count"]
            fig_mgmt = px.pie(
                mgmt_counts,
                names="Management",
                values="Count",
                hole=0.45,
                color_discrete_sequence=["#0E7490", "#0284C7", "#10B981", "#F59E0B"],
            )
            fig_mgmt.update_layout(
                margin=dict(l=20, r=20, t=30, b=30),
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_mgmt, use_container_width=True)
        else:
            st.info("No management data available for chart.")

    tab_col3, tab_col4 = st.columns(2)

    # Chart 3: Hospital Types Distribution
    with tab_col3:
        st.markdown("##### 🏷️ Distribution of Hospital Types")
        if not df_hospitals.empty and "type" in df_hospitals.columns:
            type_counts = df_hospitals["type"].value_counts().reset_index()
            type_counts.columns = ["Hospital Type", "Count"]
            fig_type = px.bar(
                type_counts,
                x="Count",
                y="Hospital Type",
                orientation="h",
                color="Count",
                color_continuous_scale="Blues",
                text="Count",
            )
            fig_type.update_layout(
                margin=dict(l=20, r=20, t=30, b=30),
                coloraxis_showscale=False,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )
            fig_type.update_traces(textposition="outside")
            st.plotly_chart(fig_type, use_container_width=True)
        else:
            st.info("No hospital type data available for chart.")

    # Chart 4: Healthcare Services by Cost Category
    with tab_col4:
        st.markdown("##### 💰 Healthcare Services by Cost Category")
        if not df_services.empty and "cost_category" in df_services.columns:
            cost_counts = df_services["cost_category"].value_counts().reset_index()
            cost_counts.columns = ["Cost Category", "Services Count"]
            fig_cost = px.bar(
                cost_counts,
                x="Cost Category",
                y="Services Count",
                color="Cost Category",
                color_discrete_sequence=["#059669", "#0284C7", "#D97706", "#64748B"],
                text="Services Count",
            )
            fig_cost.update_layout(
                margin=dict(l=20, r=20, t=30, b=30),
                showlegend=False,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )
            fig_cost.update_traces(textposition="outside")
            st.plotly_chart(fig_cost, use_container_width=True)
        else:
            st.info("No service cost data available for chart.")


def render_healthcare_module():
    """
    Main entrypoint function for the Bharat360 Healthcare & Public Services Module.
    Called by the unified Bharat360 Streamlit application.
    """
    _inject_custom_styles()
    _render_hero_section()

    # Load datasets dynamically
    data_bundle = load_all_healthcare_data()
    df_hospitals = data_bundle["hospitals"]
    df_services = data_bundle["services"]
    df_awareness = data_bundle["awareness"]
    errors = data_bundle.get("errors", [])

    if errors:
        for err in errors:
            st.warning(f"⚠️ Dataset Notice: {err}")

    # Top KPI highlights
    _render_kpis(df_hospitals, df_services, df_awareness)

    # Section 1: Global Location Selector
    st.markdown("#### 📍 Location Selection")
    loc_c1, loc_c2, loc_c3 = st.columns([1.5, 1.5, 3])

    available_states = get_unique_states(df_hospitals)
    state_options = ["All States"] + available_states

    with loc_c1:
        selected_state = st.selectbox("Select State", state_options, key="b360_global_state")

    available_cities = get_unique_cities(
        df_hospitals,
        None if selected_state == "All States" else selected_state
    )
    city_options = ["All Cities"] + available_cities

    with loc_c2:
        selected_city = st.selectbox("Select City", city_options, key="b360_global_city")

    with loc_c3:
        # Context summary badge
        st.markdown(
            f"""
            <div style="padding-top: 14px;">
                <span class="b360-badge b360-badge-blue">📍 Active Region: {selected_state} &rarr; {selected_city}</span>
                <span class="b360-badge b360-badge-green">🇮🇳 Viksit Bharat 2047</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Core Navigation Tabs
    tab_hospitals, tab_services, tab_awareness, tab_recommender, tab_analytics = st.tabs(
        [
            "🏥 Hospital Finder",
            "🩺 Healthcare Services",
            "💡 Health Awareness",
            "🎯 Service Recommender",
            "📊 Analytics & Insights",
        ]
    )

    with tab_hospitals:
        _render_hospital_finder_tab(df_hospitals, selected_state, selected_city)

    with tab_services:
        _render_services_tab(df_services)

    with tab_awareness:
        _render_awareness_tab(df_awareness)

    with tab_recommender:
        _render_recommender_tab(df_hospitals, df_services, df_awareness, selected_state, selected_city)

    with tab_analytics:
        _render_analytics_tab(df_hospitals, df_services)


# Standalone runner for testing and development
if __name__ == "__main__":
    st.set_page_config(
        page_title="Bharat360 - Healthcare & Public Services",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    render_healthcare_module()
