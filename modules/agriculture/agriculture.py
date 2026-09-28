"""
Bharat360 - Agriculture & Sustainability Module
Member 3: Agriculture & Sustainability
Unified decision-support dashboard for crops, irrigation, rainfall, and sustainability.

Visual Storytelling:
1. Header & Civic-Tech Hero (Green visual identity)
2. Compact Farmer Context Section:
   Farmer | Location | Crop | Season | Water Availability | Rainfall
3. Key Metrics Cards
4. Existing Sections:
   - 1. Farmer Profile
   - 2. Crop Explorer
   - 3. Irrigation Advisor
   - 4. Rainfall Dashboard
   - 5. Sustainability Hub
   - 6. Smart Recommendations (Visually Prominent)
"""

from typing import Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from .data_loader import load_all_agriculture_data
from .recommender import (
    recommend_irrigation,
    compute_smart_agriculture_recommendations,
    get_crop_profile,
    get_district_rainfall,
)
from modules.ui_theme import inject_master_styles, render_brand_bar


def _render_hero():
    """Renders the standard Hero banner matching the Bharat360 specification."""
    inject_master_styles()
    render_brand_bar()
    st.markdown(
        """
        <div class="b360-module-header" style="border-left: 4px solid #16A34A;">
            <div>
                <h1 class="b360-module-title">🌾 Agriculture & Sustainability</h1>
                <p class="b360-module-sub">Make smarter agricultural, irrigation, and resource decisions grounded in verified agro-climatic data.</p>
            </div>
            <div>
                <span class="b360-tag-pill" style="background: #F0FDF4; color: #15803D; border: 1px solid #BBF7D0;">
                    Viksit Bharat 2047 • Agro-Intelligence
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _init_session_state(crop_df: pd.DataFrame, rainfall_df: pd.DataFrame):
    """Initializes interactive farmer profile session state defaults."""
    crops_available = sorted(crop_df["crop"].dropna().unique().tolist()) if not crop_df.empty else ["Rice"]
    districts_available = sorted(rainfall_df["district"].dropna().unique().tolist()) if not rainfall_df.empty else ["Kakinada"]
    states_available = sorted(rainfall_df["state"].dropna().unique().tolist()) if not rainfall_df.empty else ["Andhra Pradesh"]

    if "fp_state" not in st.session_state:
        st.session_state.fp_state = states_available[0] if states_available else "Andhra Pradesh"
    if "fp_district" not in st.session_state:
        st.session_state.fp_district = districts_available[0] if districts_available else "Kakinada"
    if "fp_crop" not in st.session_state:
        st.session_state.fp_crop = crops_available[0] if crops_available else "Rice"
    if "fp_season" not in st.session_state:
        st.session_state.fp_season = "Kharif"
    if "fp_water_avail" not in st.session_state:
        st.session_state.fp_water_avail = "Medium"
    if "fp_irrig_pref" not in st.session_state:
        st.session_state.fp_irrig_pref = "Balanced / Any"


def _render_farmer_context_card(crop_df: pd.DataFrame, rainfall_df: pd.DataFrame):
    """
    Renders the compact context section at the top showing:
    Farmer | Location | Crop | Season | Water availability | Rainfall
    """
    state = st.session_state.get("fp_state", "Andhra Pradesh")
    district = st.session_state.get("fp_district", "Kakinada")
    crop = st.session_state.get("fp_crop", "Rice")
    season = st.session_state.get("fp_season", "Kharif")
    water_avail = st.session_state.get("fp_water_avail", "Medium")

    dist_data = get_district_rainfall(rainfall_df, district)
    rain_val = dist_data.get("annual_rainfall_mm", "N/A") if dist_data else "N/A"

    st.markdown(
        f"""
        <div class="b360-farmer-context-grid">
            <div class="b360-fc-item">
                <span class="b360-fc-label">👤 Farmer</span>
                <span class="b360-fc-val">Active Citizen</span>
            </div>
            <div class="b360-fc-item">
                <span class="b360-fc-label">📍 Location</span>
                <span class="b360-fc-val">{district}, {state}</span>
            </div>
            <div class="b360-fc-item">
                <span class="b360-fc-label">🌱 Crop</span>
                <span class="b360-fc-val">{crop}</span>
            </div>
            <div class="b360-fc-item">
                <span class="b360-fc-label">☀️ Season</span>
                <span class="b360-fc-val">{season}</span>
            </div>
            <div class="b360-fc-item">
                <span class="b360-fc-label">💧 Water Availability</span>
                <span class="b360-fc-val">{water_avail}</span>
            </div>
            <div class="b360-fc-item">
                <span class="b360-fc-label">🌧️ Rainfall</span>
                <span class="b360-fc-val">{rain_val} mm</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_key_metrics_row(crop_df: pd.DataFrame, rainfall_df: pd.DataFrame):
    """Renders key metrics cards below the context card."""
    district = st.session_state.get("fp_district", "Kakinada")
    crop = st.session_state.get("fp_crop", "Rice")
    water_avail = st.session_state.get("fp_water_avail", "Medium")

    crop_info = get_crop_profile(crop_df, crop)
    dist_rain_data = get_district_rainfall(rainfall_df, district)
    annual_rain = dist_rain_data.get("annual_rainfall_mm", "N/A") if dist_rain_data else "N/A"
    water_req = crop_info.get("water_requirement", "Medium") if crop_info else "Medium"
    input_req = crop_info.get("input_requirement", "Medium") if crop_info else "Medium"

    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    with p_col1:
        st.markdown(
            f"""
            <div class="b360-metric-card" style="border-top: 3px solid #16A34A;">
                <div class="b360-metric-num" style="color: #16A34A;">{annual_rain} mm</div>
                <div class="b360-metric-label">District Rainfall</div>
                <small style="color: #64748B;">{district} Annual</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p_col2:
        st.markdown(
            f"""
            <div class="b360-metric-card" style="border-top: 3px solid #0D9488;">
                <div class="b360-metric-num" style="color: #0D9488;">{water_req}</div>
                <div class="b360-metric-label">Crop Water Demand</div>
                <small style="color: #64748B;">For {crop}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p_col3:
        st.markdown(
            f"""
            <div class="b360-metric-card" style="border-top: 3px solid #D97706;">
                <div class="b360-metric-num" style="color: #D97706;">{input_req}</div>
                <div class="b360-metric-label">Input Requirement</div>
                <small style="color: #64748B;">Seed & Fertilizer</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p_col4:
        st.markdown(
            f"""
            <div class="b360-metric-card" style="border-top: 3px solid #38BDF8;">
                <div class="b360-metric-num" style="color: #38BDF8;">{water_avail}</div>
                <div class="b360-metric-label">Water Supply</div>
                <small style="color: #94A3B8;">Farmer Baseline</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)


def _render_farmer_profile_section(crop_df: pd.DataFrame, rainfall_df: pd.DataFrame):
    """Section 1: Farmer Profile configuration."""
    st.markdown("### 🚜 1. Farmer Profile")
    st.caption("Configure the primary agro-climatic profile to drive recommendations and analytics.")

    states = sorted(rainfall_df["state"].dropna().unique().tolist()) if not rainfall_df.empty else ["Andhra Pradesh"]

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        current_state = st.session_state.get("fp_state", states[0] if states else "Andhra Pradesh")
        state_idx = states.index(current_state) if current_state in states else 0
        selected_state = st.selectbox("State", options=states, index=state_idx, key="fp_state_select")
        st.session_state.fp_state = selected_state

    state_rainfall_df = rainfall_df[rainfall_df["state"] == selected_state] if not rainfall_df.empty else rainfall_df
    districts = sorted(state_rainfall_df["district"].dropna().unique().tolist()) if not state_rainfall_df.empty else ["Kakinada"]

    with col2:
        current_district = st.session_state.get("fp_district", districts[0] if districts else "Kakinada")
        dist_idx = districts.index(current_district) if current_district in districts else 0
        selected_district = st.selectbox("District", options=districts, index=dist_idx, key="fp_district_select")
        st.session_state.fp_district = selected_district

    crops = sorted(crop_df["crop"].dropna().unique().tolist()) if not crop_df.empty else ["Rice"]
    with col3:
        current_crop = st.session_state.get("fp_crop", crops[0] if crops else "Rice")
        crop_idx = crops.index(current_crop) if current_crop in crops else 0
        selected_crop = st.selectbox("Crop", options=crops, index=crop_idx, key="fp_crop_select")
        st.session_state.fp_crop = selected_crop

    crop_info = get_crop_profile(crop_df, selected_crop)
    seasons = ["Kharif", "Rabi", "Kharif/Rabi", "Annual"]
    default_season = crop_info.get("season", "Kharif") if crop_info else "Kharif"
    current_season = st.session_state.get("fp_season", default_season)
    season_idx = seasons.index(current_season) if current_season in seasons else (seasons.index(default_season) if default_season in seasons else 0)

    with col4:
        selected_season = st.selectbox("Season", options=seasons, index=season_idx, key="fp_season_select")
        st.session_state.fp_season = selected_season

    with col5:
        water_options = ["Low", "Medium", "High"]
        current_water = st.session_state.get("fp_water_avail", "Medium")
        water_idx = water_options.index(current_water) if current_water in water_options else 1
        selected_water = st.selectbox("Water Availability", options=water_options, index=water_idx, key="fp_water_select")
        st.session_state.fp_water_avail = selected_water


def _render_crop_explorer_section(crop_df: pd.DataFrame):
    """Section 2: Crop Explorer with cards, table, and sunburst chart."""
    st.markdown("### 🌾 2. Crop Explorer")
    st.caption("Explore crop characteristics, water intensity, and seasonal windows with dynamic filters.")

    if crop_df.empty:
        st.warning("Crop dataset is currently empty or unavailable.")
        return

    f_col1, f_col2, f_col3, f_col4 = st.columns([1.5, 1, 1, 1])

    with f_col1:
        search_query = st.text_input("🔍 Search Crop Name", placeholder="e.g. Rice, Chilli, Groundnut...", key="crop_search").strip().lower()

    with f_col2:
        seasons_list = ["All"] + sorted(crop_df["season"].dropna().unique().tolist())
        selected_season_filter = st.selectbox("Filter Season", seasons_list, key="crop_season_filt")

    with f_col3:
        water_reqs = ["All"] + sorted(crop_df["water_requirement"].dropna().unique().tolist())
        selected_water_filter = st.selectbox("Water Requirement", water_reqs, key="crop_water_filt")

    with f_col4:
        input_reqs = ["All"] + sorted(crop_df["input_requirement"].dropna().unique().tolist())
        selected_input_filter = st.selectbox("Input Requirement", input_reqs, key="crop_input_filt")

    filtered_df = crop_df.copy()
    if search_query:
        filtered_df = filtered_df[filtered_df["crop"].astype(str).str.lower().str.contains(search_query)]
    if selected_season_filter != "All":
        filtered_df = filtered_df[filtered_df["season"] == selected_season_filter]
    if selected_water_filter != "All":
        filtered_df = filtered_df[filtered_df["water_requirement"] == selected_water_filter]
    if selected_input_filter != "All":
        filtered_df = filtered_df[filtered_df["input_requirement"] == selected_input_filter]

    st.markdown(f"**Showing {len(filtered_df)} of {len(crop_df)} crops**")

    tab_cards, tab_table, tab_chart = st.tabs(["📇 Crop Cards", "📊 Data Table", "📈 Requirements Visualizer"])

    with tab_cards:
        if filtered_df.empty:
            st.info("No crops match the selected filter criteria.")
        else:
            cols = st.columns(min(max(len(filtered_df), 1), 3))
            for i, (_, row) in enumerate(filtered_df.iterrows()):
                col_idx = i % 3
                with cols[col_idx]:
                    w_req = row.get("water_requirement", "Medium")
                    badge_class = "badge-red" if "High" in str(w_req) else ("badge-green" if "Low" in str(w_req) else "badge-amber")

                    st.markdown(
                        f"""
                        <div class="b360-card" style="border-top: 3px solid #16A34A;">
                            <div class="b360-card-header">
                                <h4 class="b360-card-title">🌱 {row.get('crop', 'Unknown')}</h4>
                                <span class="b360-badge {badge_class}">💧 {w_req} Water</span>
                            </div>
                            <div style="margin-bottom: 6px;">
                                <span class="b360-badge badge-blue">{row.get('category', 'General')}</span>
                            </div>
                            <p style="margin: 4px 0; font-size: 0.88rem; color: #CBD5E1;">
                                <strong>Season:</strong> {row.get('season', 'N/A')}<br>
                                <strong>Input Requirement:</strong> {row.get('input_requirement', 'N/A')}<br>
                                <strong>Catalog ID:</strong> #{row.get('id', 'N/A')}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    with tab_table:
        display_cols = [c for c in ["id", "crop", "season", "water_requirement", "input_requirement", "category"] if c in filtered_df.columns]
        st.dataframe(
            filtered_df[display_cols].rename(columns={
                "id": "ID",
                "crop": "Crop Name",
                "season": "Season",
                "water_requirement": "Water Requirement",
                "input_requirement": "Input Requirement",
                "category": "Category",
            }),
            use_container_width=True,
            hide_index=True,
        )

    with tab_chart:
        if not crop_df.empty:
            fig = px.sunburst(
                crop_df,
                path=["water_requirement", "season", "crop"],
                title="Crop Distribution by Water Requirement & Season",
                color="water_requirement",
                color_discrete_map={
                    "Very High": "#DC2626",
                    "High": "#EA580C",
                    "Medium": "#D97706",
                    "Low": "#16A34A",
                },
            )
            fig.update_layout(margin=dict(t=40, l=10, r=10, b=10), height=360)
            st.plotly_chart(fig, use_container_width=True)


def _render_irrigation_advisor_section(crop_df: pd.DataFrame, irrigation_df: pd.DataFrame):
    """Section 3: Irrigation Advisor rule-based matching."""
    st.markdown("### 💧 3. Irrigation Advisor")
    st.caption("Rule-based recommendation engine matching crops and water supplies to irrigation systems.")

    if irrigation_df.empty:
        st.warning("Irrigation dataset is currently empty or unavailable.")
        return

    i_col1, i_col2, i_col3 = st.columns(3)

    crops = sorted(crop_df["crop"].dropna().unique().tolist()) if not crop_df.empty else ["Rice"]
    current_crop = st.session_state.get("fp_crop", crops[0])
    crop_idx = crops.index(current_crop) if current_crop in crops else 0

    with i_col1:
        sel_crop = st.selectbox("Select Crop", options=crops, index=crop_idx, key="irrig_crop_select")

    water_options = ["Low", "Medium", "High"]
    current_water = st.session_state.get("fp_water_avail", "Medium")
    water_idx = water_options.index(current_water) if current_water in water_options else 1

    with i_col2:
        sel_water = st.selectbox("Water Availability Level", options=water_options, index=water_idx, key="irrig_water_select")

    pref_options = ["Balanced / Any", "Efficiency-First", "Low Cost", "Supplemental / Storage"]
    current_pref = st.session_state.get("fp_irrig_pref", "Balanced / Any")
    pref_idx = pref_options.index(current_pref) if current_pref in pref_options else 0

    with i_col3:
        sel_pref = st.selectbox("Irrigation Preference", options=pref_options, index=pref_idx, key="irrig_pref_select")
        st.session_state.fp_irrig_pref = sel_pref

    rec_result = recommend_irrigation(
        crop_name=sel_crop,
        water_availability=sel_water,
        preference=sel_pref,
        crop_df=crop_df,
        irrigation_df=irrigation_df,
    )

    top_method = rec_result.get("top_method")
    ranked = rec_result.get("ranked_methods", [])

    if top_method:
        st.markdown(
            f"""
            <div class="b360-rec-box">
                <div class="b360-rec-header">
                    💧 Recommended Irrigation Approach: {top_method['method']}
                </div>
                <p style="font-size: 0.95rem; color: #CBD5E1; margin-bottom: 8px;">
                    {rec_result.get('reason', '')}
                </p>
                <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                    <span class="b360-badge badge-blue">⚡ Efficiency: {top_method['water_efficiency']}</span>
                    <span class="b360-badge badge-green">💰 Cost Level: {top_method['cost_level']}</span>
                    <span class="b360-badge badge-amber">🎯 Suitable For: {top_method['suitable_for']}</span>
                    <span class="b360-badge badge-purple">⭐ Rule Score: {top_method['score']} pts</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("#### 📋 Comparative Irrigation Evaluation Grounded in irrigation.csv")
    if ranked:
        ranked_display_data = []
        for r in ranked:
            ranked_display_data.append({
                "Method": r["method"],
                "Water Efficiency": r["water_efficiency"],
                "Cost Level": r["cost_level"],
                "Suitable For": r["suitable_for"],
                "Rule Score": f"{r['score']} pts",
                "Dataset Attribute Justification": r["justification"],
            })
        st.dataframe(pd.DataFrame(ranked_display_data), use_container_width=True, hide_index=True)


def _render_rainfall_dashboard_section(rainfall_df: pd.DataFrame):
    """Section 4: Rainfall Dashboard and visual comparisons."""
    st.markdown("### 🌧️ 4. Rainfall Dashboard")
    st.caption("Precipitation patterns, district comparisons, and baseline benchmarks from rainfall.csv.")

    if rainfall_df.empty:
        st.warning("Rainfall dataset is currently empty or unavailable.")
        return

    avg_rainfall = rainfall_df["annual_rainfall_mm"].mean()
    max_row = rainfall_df.loc[rainfall_df["annual_rainfall_mm"].idxmax()]
    min_row = rainfall_df.loc[rainfall_df["annual_rainfall_mm"].idxmin()]
    user_dist = st.session_state.get("fp_district", rainfall_df["district"].iloc[0])
    user_dist_data = get_district_rainfall(rainfall_df, user_dist)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            f"""
            <div class="b360-metric-card" style="border-top: 3px solid #0284C7;">
                <div class="b360-metric-num" style="color: #0284C7;">{avg_rainfall:.1f} mm</div>
                <div class="b360-metric-label">State Mean Rainfall</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        diff = user_dist_data.get('rainfall_diff_pct', 0)
        st.markdown(
            f"""
            <div class="b360-metric-card" style="border-top: 3px solid #16A34A;">
                <div class="b360-metric-num" style="color: #16A34A;">{user_dist_data.get('annual_rainfall_mm', 0):.0f} mm</div>
                <div class="b360-metric-label">{user_dist} ({diff:+.1f}%)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f"""
            <div class="b360-metric-card" style="border-top: 3px solid #0D9488;">
                <div class="b360-metric-num" style="color: #0D9488;">{max_row['annual_rainfall_mm']} mm</div>
                <div class="b360-metric-label">Highest: {max_row['district']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            f"""
            <div class="b360-metric-card" style="border-top: 3px solid #D97706;">
                <div class="b360-metric-num" style="color: #D97706;">{min_row['annual_rainfall_mm']} mm</div>
                <div class="b360-metric-label">Lowest: {min_row['district']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    c_tab1, c_tab2, c_tab3 = st.tabs(["📊 Rainfall by District", "⚖️ District Variance (%)", "📑 Raw Rainfall Data"])

    with c_tab1:
        colors = ["#16A34A" if d == user_dist else "#93C5FD" for d in rainfall_df["district"]]
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=rainfall_df["district"],
            y=rainfall_df["annual_rainfall_mm"],
            marker_color=colors,
            text=rainfall_df["annual_rainfall_mm"].apply(lambda v: f"{v} mm"),
            textposition="auto",
            hovertemplate="<b>%{x}</b><br>Rainfall: %{y} mm<extra></extra>",
        ))
        fig_bar.add_hline(
            y=avg_rainfall,
            line_dash="dash",
            line_color="#E65100",
            annotation_text=f"State Mean: {avg_rainfall:.0f} mm",
            annotation_position="top right",
        )
        fig_bar.update_layout(
            title="Annual Rainfall by District (2024)",
            xaxis_title="District",
            yaxis_title="Annual Rainfall (mm)",
            margin=dict(t=50, l=10, r=10, b=10),
            height=340,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with c_tab2:
        dev_df = rainfall_df.copy()
        dev_df["diff_pct"] = ((dev_df["annual_rainfall_mm"] - avg_rainfall) / avg_rainfall) * 100
        dev_df["color"] = dev_df["diff_pct"].apply(lambda x: "#16A34A" if x >= 0 else "#DC2626")

        fig_dev = go.Figure(go.Bar(
            x=dev_df["district"],
            y=dev_df["diff_pct"],
            marker_color=dev_df["color"],
            text=dev_df["diff_pct"].apply(lambda v: f"{v:+.1f}%"),
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Variance: %{y:+.1f}%<extra></extra>",
        ))
        fig_dev.add_hline(y=0, line_color="#64748B", line_width=1)
        fig_dev.update_layout(
            title="District Rainfall Variance from State Average (%)",
            xaxis_title="District",
            yaxis_title="Deviation (%)",
            margin=dict(t=50, l=10, r=10, b=10),
            height=340,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_dev, use_container_width=True)

    with c_tab3:
        st.dataframe(
            rainfall_df.rename(columns={
                "id": "ID",
                "district": "District",
                "state": "State",
                "year": "Year",
                "annual_rainfall_mm": "Annual Rainfall (mm)",
            }),
            use_container_width=True,
            hide_index=True,
        )


def _render_sustainability_hub_section(sustainability_df: pd.DataFrame):
    """Section 5: Sustainability Hub."""
    st.markdown("### ♻️ 5. Sustainability Hub")
    st.caption("Explore sustainable interventions, water conservation models, and green farm practices.")

    if sustainability_df.empty:
        st.warning("Sustainability dataset is currently empty or unavailable.")
        return

    s_col1, s_col2 = st.columns(2)
    with s_col1:
        impact_areas = ["All"] + sorted(sustainability_df["impact_area"].dropna().unique().tolist())
        selected_area = st.selectbox("Filter Impact Area", impact_areas, key="sust_area_filter")
    with s_col2:
        target_groups = ["All", "Farmers", "Households/Farms", "Communities/Farms", "Citizens"]
        selected_user = st.selectbox("Filter Target Users", target_groups, key="sust_user_filter")

    filtered_sust = sustainability_df.copy()
    if selected_area != "All":
        filtered_sust = filtered_sust[filtered_sust["impact_area"] == selected_area]
    if selected_user != "All":
        filtered_sust = filtered_sust[filtered_sust["target_users"].astype(str).str.contains(selected_user, case=False, na=False)]

    s_tab1, s_tab2, s_tab3 = st.tabs(["💡 Sustainable Initiatives", "📊 Impact Breakdown", "📑 Master List"])

    with s_tab1:
        if filtered_sust.empty:
            st.info("No initiatives match the chosen filter.")
        else:
            cols = st.columns(min(max(len(filtered_sust), 1), 3))
            for i, (_, row) in enumerate(filtered_sust.iterrows()):
                col_idx = i % 3
                with cols[col_idx]:
                    impact_lvl = row.get("potential_impact", "Medium")
                    impact_badge = "badge-green" if "High" in str(impact_lvl) else "badge-amber"

                    st.markdown(
                        f"""
                        <div class="b360-card" style="border-top: 3px solid #16A34A;">
                            <div class="b360-card-header">
                                <h4 class="b360-card-title">🌱 {row.get('initiative', 'Initiative')}</h4>
                                <span class="b360-badge {impact_badge}">⚡ {impact_lvl} Impact</span>
                            </div>
                            <div style="margin-bottom: 4px;">
                                <span class="b360-badge badge-blue">{row.get('impact_area', 'General')}</span>
                            </div>
                            <p style="margin: 4px 0; font-size: 0.88rem; color: #CBD5E1;">
                                <strong>Target Users:</strong> {row.get('target_users', 'General')}<br>
                                <strong>Catalog ID:</strong> #{row.get('id', 'N/A')}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    with s_tab2:
        if not sustainability_df.empty:
            fig = px.bar(
                sustainability_df,
                x="impact_area",
                color="potential_impact",
                title="Initiatives Count by Impact Area & Potential Impact",
                barmode="stack",
                color_discrete_map={"High": "#16A34A", "Medium": "#D97706"},
            )
            fig.update_layout(
                xaxis_title="Impact Area",
                yaxis_title="Count of Initiatives",
                margin=dict(t=50, l=10, r=10, b=10),
                height=340,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig, use_container_width=True)

    with s_tab3:
        st.dataframe(
            sustainability_df.rename(columns={
                "id": "ID",
                "initiative": "Initiative",
                "impact_area": "Impact Area",
                "potential_impact": "Potential Impact",
                "target_users": "Target Users",
            }),
            use_container_width=True,
            hide_index=True,
        )


def _render_smart_recommendations_section(
    crop_df: pd.DataFrame,
    rainfall_df: pd.DataFrame,
    irrigation_df: pd.DataFrame,
    sustainability_df: pd.DataFrame,
):
    """
    Section 6: Smart Agriculture Recommendations (VISUALLY PROMINENT).
    Rule-based recommendations combining crop, water availability, rainfall, and sustainability.
    """
    st.markdown("### 🤖 **AI-Powered Recommendations**")
    st.caption("Multi-factor synthesis connecting agronomic demand, rainfall realities, and green practices.")

    crop = st.session_state.get("fp_crop", "Rice")
    district = st.session_state.get("fp_district", "Kakinada")
    water_avail = st.session_state.get("fp_water_avail", "Medium")
    pref = st.session_state.get("fp_irrig_pref", "Balanced / Any")

    smart_rec = compute_smart_agriculture_recommendations(
        crop_name=crop,
        district_name=district,
        water_availability=water_avail,
        irrigation_preference=pref,
        crop_df=crop_df,
        rainfall_df=rainfall_df,
        irrigation_df=irrigation_df,
        sustainability_df=sustainability_df,
    )

    stress = smart_rec.get("water_stress", {})
    irrig_rec = smart_rec.get("irrigation_recommendation", {})
    top_irrig = irrig_rec.get("top_method")
    sust_recs = smart_rec.get("sustainability_recommendations", [])
    factors_list = smart_rec.get("factors_table", [])

    stress_bg = "rgba(239, 68, 68, 0.20)" if "High" in stress.get("level", "") else ("rgba(245, 158, 11, 0.20)" if "Moderate" in stress.get("level", "") else "rgba(16, 185, 129, 0.20)")
    stress_border = "#EF4444" if "High" in stress.get("level", "") else ("#F59E0B" if "Moderate" in stress.get("level", "") else "#10B981")
    stress_text = "#FCA5A5" if "High" in stress.get("level", "") else ("#FDE68A" if "Moderate" in stress.get("level", "") else "#86EFAC")

    st.markdown(
        f"""
        <div style="background-color: {stress_bg}; border: 1.5px solid {stress_border}; border-radius: 18px; padding: 18px 22px; margin-bottom: 1.2rem; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);">
            <div style="font-size: 1.2rem; font-weight: 700; color: {stress_text}; margin-bottom: 6px;">
                🌊 Water Stress Diagnosis: {stress.get('level', 'Normal')}
            </div>
            <p style="font-size: 0.92rem; color: #CBD5E1; margin: 0; line-height: 1.5;">
                {stress.get('description', '')}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    r_col1, r_col2 = st.columns(2)

    with r_col1:
        st.markdown(
            f"""
            <div class="b360-card" style="border-top: 4px solid #0284C7; height: 100%;">
                <div class="b360-card-title">💧 Recommended Irrigation Pathway</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: #38BDF8; margin: 6px 0 8px 0;">
                    {top_irrig['method'] if top_irrig else 'Canal / Drip'}
                </div>
                <p style="font-size: 0.88rem; color: #CBD5E1; line-height: 1.45; margin-bottom: 10px;">
                    {irrig_rec.get('reason', '')}
                </p>
                <div style="margin-top: 6px;">
                    <span class="b360-badge badge-blue">Efficiency: {top_irrig['water_efficiency'] if top_irrig else 'N/A'}</span>
                    <span class="b360-badge badge-green">Cost: {top_irrig['cost_level'] if top_irrig else 'N/A'}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with r_col2:
        st.markdown(
            """
            <div class="b360-card" style="border-top: 4px solid #16A34A; height: 100%;">
                <div class="b360-card-title">♻️ Aligned Sustainable Initiatives</div>
                <p style="font-size: 0.86rem; color: #94A3B8; margin-bottom: 8px;">
                    Ground-level interventions matched from the sustainability catalog:
                </p>
            """,
            unsafe_allow_html=True,
        )
        if sust_recs:
            for s in sust_recs[:3]:
                st.markdown(
                    f"""
                    <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 8px; padding: 8px 12px; margin-bottom: 8px;">
                        <strong style="color: #6EE7B7;">🌱 {s['initiative']}</strong> <span style="font-size: 0.78rem; color: #94A3B8;">({s['impact_area']})</span><br>
                        <small style="color: #CBD5E1;">{s['relevance_reason']}</small>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("General sustainability practices apply.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("#### 🔍 Transparent Factors Used in Recommendations")
    st.caption("Every recommendation is strictly rule-based and derived directly from dataset attributes without invented claims.")

    st.dataframe(pd.DataFrame(factors_list), use_container_width=True, hide_index=True)


def render_agriculture_module():
    """
    Main entry point for the Bharat360 Agriculture & Sustainability Module.
    Can be invoked inside the unified Bharat360 app.py or tested standalone.
    """
    # 1. Render Header
    _render_hero()

    # 2. Dynamic Data Loading
    data = load_all_agriculture_data()
    crop_df = data.get("crop_data", pd.DataFrame())
    rainfall_df = data.get("rainfall", pd.DataFrame())
    irrigation_df = data.get("irrigation", pd.DataFrame())
    sustainability_df = data.get("sustainability", pd.DataFrame())

    if not data.get("all_loaded", False):
        with st.expander("⚠️ Dataset Diagnostics & Status", expanded=True):
            st.error("Some agriculture datasets could not be located in standard candidate paths.")
            for err in data.get("errors", []):
                st.write(f"- {err}")

    # 3. Initialize Interactive State
    _init_session_state(crop_df, rainfall_df)

    # 4. Compact Farmer Context Section: Farmer | Location | Crop | Season | Water availability | Rainfall
    _render_farmer_context_card(crop_df, rainfall_df)

    # 5. Key Metrics Row
    _render_key_metrics_row(crop_df, rainfall_df)

    # 6. View Mode Switcher
    c1, c2 = st.columns([3, 1])
    with c2:
        view_mode = st.radio("Dashboard View", ["📑 Tabbed Sections", "📜 Full Sequential Report"], horizontal=True, label_visibility="collapsed")

    if view_mode == "📑 Tabbed Sections":
        tabs = st.tabs([
            "🚜 1. Farmer Profile",
            "🌾 2. Crop Explorer",
            "💧 3. Irrigation Advisor",
            "🌧️ 4. Rainfall Dashboard",
            "♻️ 5. Sustainability Hub",
            "🤖 6. Smart Recommendations",
        ])

        with tabs[0]:
            _render_farmer_profile_section(crop_df, rainfall_df)

        with tabs[1]:
            _render_crop_explorer_section(crop_df)

        with tabs[2]:
            _render_irrigation_advisor_section(crop_df, irrigation_df)

        with tabs[3]:
            _render_rainfall_dashboard_section(rainfall_df)

        with tabs[4]:
            _render_sustainability_hub_section(sustainability_df)

        with tabs[5]:
            _render_smart_recommendations_section(crop_df, rainfall_df, irrigation_df, sustainability_df)

    else:
        _render_farmer_profile_section(crop_df, rainfall_df)
        st.divider()
        _render_crop_explorer_section(crop_df)
        st.divider()
        _render_irrigation_advisor_section(crop_df, irrigation_df)
        st.divider()
        _render_rainfall_dashboard_section(rainfall_df)
        st.divider()
        _render_sustainability_hub_section(sustainability_df)
        st.divider()
        _render_smart_recommendations_section(crop_df, rainfall_df, irrigation_df, sustainability_df)

    # Prototype Disclaimer
    st.markdown(
        """
        <div class="b360-disclaimer" style="margin-top: 1.5rem; text-align: center;">
            <strong>Bharat360 • Agriculture & Sustainability Module Prototype</strong><br>
            Designed for Viksit Bharat 2047 Hackathon. All data dynamically loaded from project datasets.
            This demonstration platform serves educational and resource-planning purposes and does not replace live official governmental agro-advisories.
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    st.set_page_config(
        page_title="Bharat360 - Agriculture & Sustainability",
        page_icon="🌾",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    render_agriculture_module()
