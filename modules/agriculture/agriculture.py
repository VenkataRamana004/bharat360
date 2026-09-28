"""
Bharat360 - Agriculture & Sustainability Module
Member 3: Agriculture & Sustainability
Unified decision-support dashboard for crops, irrigation, rainfall, and sustainability.
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

# Custom CSS for Bharat360 Visual Identity
BHARAT360_CSS = """
<style>
/* Main Container Styling */
.b360-header {
    background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 60%, #388E3C 100%);
    color: white;
    padding: 2.2rem 2.4rem;
    border-radius: 14px;
    box-shadow: 0 4px 16px rgba(27, 94, 32, 0.18);
    margin-bottom: 1.5rem;
}
.b360-header h1 {
    color: #FFFFFF !important;
    font-size: 2.35rem !important;
    font-weight: 800 !important;
    margin: 0 0 0.4rem 0 !important;
    letter-spacing: -0.5px;
}
.b360-header p {
    color: #E8F5E9 !important;
    font-size: 1.15rem !important;
    margin: 0 !important;
    font-weight: 400;
}
.b360-tag {
    display: inline-block;
    background: rgba(255, 255, 255, 0.22);
    color: #FFF;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
    margin-top: 0.8rem;
    letter-spacing: 0.5px;
}
/* Cards */
.b360-card {
    background: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 12px;
    padding: 1.25rem 1.4rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.b360-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}
.b360-card-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #1B5E20;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
/* Metric Tile */
.b360-metric {
    background: #F8FAF9;
    border-left: 4px solid #2E7D32;
    border-radius: 8px;
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.6rem;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
}
.b360-metric-value {
    font-size: 1.55rem;
    font-weight: 700;
    color: #1B5E20;
}
.b360-metric-label {
    font-size: 0.82rem;
    color: #555555;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
/* Badges */
.badge-high {
    background-color: #FFEBEE;
    color: #C62828;
    border: 1px solid #FFCDD2;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.82rem;
    font-weight: 600;
}
.badge-medium {
    background-color: #FFF8E1;
    color: #F57F17;
    border: 1px solid #FFE082;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.82rem;
    font-weight: 600;
}
.badge-low {
    background-color: #E8F5E9;
    color: #2E7D32;
    border: 1px solid #C8E6C9;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.82rem;
    font-weight: 600;
}
.badge-neutral {
    background-color: #E3F2FD;
    color: #1565C0;
    border: 1px solid #BBDEFB;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.82rem;
    font-weight: 600;
}
/* Recommendation Banner */
.rec-banner {
    background: #F1F8E9;
    border: 2px solid #81C784;
    border-radius: 12px;
    padding: 1.25rem 1.4rem;
    margin-bottom: 1.2rem;
}
/* Quick Profile Strip */
.profile-strip {
    background: #FAFAFA;
    border: 1px solid #E0E0E0;
    border-radius: 10px;
    padding: 0.75rem 1.2rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
}
/* Disclaimer */
.b360-disclaimer {
    background-color: #FAFAFA;
    border-top: 1px solid #EEEEEE;
    color: #757575;
    font-size: 0.82rem;
    padding: 1.2rem 0;
    text-align: center;
    margin-top: 3rem;
}
</style>
"""


def _render_hero():
    """Renders the standard Hero banner required for Member 3."""
    st.markdown(BHARAT360_CSS, unsafe_allow_html=True)
    st.markdown(
        """
        <div class="b360-header">
            <h1>🌾 Agriculture & Sustainability</h1>
            <p>Make smarter agricultural and resource decisions for a sustainable future.</p>
            <div class="b360-tag">🇮🇳 Viksit Bharat 2047 • Resource Efficiency & Agro-Intelligence</div>
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


def _render_profile_strip(crop_df: pd.DataFrame, rainfall_df: pd.DataFrame):
    """Renders a clean profile strip showing active inputs at a glance."""
    state = st.session_state.get("fp_state", "Andhra Pradesh")
    district = st.session_state.get("fp_district", "Kakinada")
    crop = st.session_state.get("fp_crop", "Rice")
    season = st.session_state.get("fp_season", "Kharif")
    water_avail = st.session_state.get("fp_water_avail", "Medium")

    dist_data = get_district_rainfall(rainfall_df, district)
    rain_val = dist_data.get("annual_rainfall_mm", "N/A") if dist_data else "N/A"

    st.markdown(
        f"""
        <div class="profile-strip">
            <div>
                <span style="font-weight: 700; color: #1B5E20; margin-right: 6px;">🚜 Active Farmer Profile:</span>
                <span style="color: #333;"><strong>{district}</strong>, {state}</span>
                <span style="color: #888; margin: 0 8px;">|</span>
                <span style="color: #333;">Crop: <strong>{crop}</strong> ({season})</span>
                <span style="color: #888; margin: 0 8px;">|</span>
                <span style="color: #333;">Water: <strong>{water_avail}</strong></span>
                <span style="color: #888; margin: 0 8px;">|</span>
                <span style="color: #333;">Rainfall: <strong>{rain_val} mm</strong></span>
            </div>
            <div>
                <span class="badge-neutral">Dynamic Inputs Active</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_farmer_profile_section(crop_df: pd.DataFrame, rainfall_df: pd.DataFrame):
    """
    Section 1: Farmer Profile
    Allow: State, District, Crop, Season, Water availability. Keep it simple.
    """
    st.markdown("### 🚜 1. Farmer Profile")
    st.caption("Configure the primary agro-climatic profile to drive recommendations and analytics.")

    # Populate choices dynamically from datasets
    states = sorted(rainfall_df["state"].dropna().unique().tolist()) if not rainfall_df.empty else ["Andhra Pradesh"]
    
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        current_state = st.session_state.get("fp_state", states[0] if states else "Andhra Pradesh")
        state_idx = states.index(current_state) if current_state in states else 0
        selected_state = st.selectbox("State", options=states, index=state_idx, key="fp_state_select")
        st.session_state.fp_state = selected_state

    # Filter districts for selected state
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

    # Find the crop's natural season from dataset to guide options
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

    # Summary Cards for Farmer Profile
    dist_rain_data = get_district_rainfall(rainfall_df, selected_district)
    annual_rain = dist_rain_data.get("annual_rainfall_mm", "N/A") if dist_rain_data else "N/A"
    water_req = crop_info.get("water_requirement", "N/A") if crop_info else "N/A"
    input_req = crop_info.get("input_requirement", "N/A") if crop_info else "N/A"

    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    with p_col1:
        st.markdown(
            f"""
            <div class="b360-metric">
                <div class="b360-metric-label">Location</div>
                <div class="b360-metric-value" style="font-size: 1.25rem;">{selected_district}</div>
                <small style="color: #666;">{selected_state}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p_col2:
        st.markdown(
            f"""
            <div class="b360-metric">
                <div class="b360-metric-label">District Rainfall</div>
                <div class="b360-metric-value" style="font-size: 1.25rem;">{annual_rain} mm</div>
                <small style="color: #666;">Annual Precipitation</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p_col3:
        st.markdown(
            f"""
            <div class="b360-metric">
                <div class="b360-metric-label">Crop Demands</div>
                <div class="b360-metric-value" style="font-size: 1.25rem;">{water_req} Water</div>
                <small style="color: #666;">Input Requirement: {input_req}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p_col4:
        st.markdown(
            f"""
            <div class="b360-metric">
                <div class="b360-metric-label">Water Availability</div>
                <div class="b360-metric-value" style="font-size: 1.25rem;">{selected_water}</div>
                <small style="color: #666;">Farmer Reported Baseline</small>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_crop_explorer_section(crop_df: pd.DataFrame):
    """
    Section 2: Crop Explorer
    Display crop information: Crop, Season, Water requirement, Input requirement, Category.
    Allow filtering.
    """
    st.markdown("### 🌾 2. Crop Explorer")
    st.caption("Explore crop characteristics, water intensity, and seasonal windows with dynamic filters.")

    if crop_df.empty:
        st.warning("Crop dataset is currently empty or unavailable.")
        return

    # Filter Controls
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

    # Apply filters dynamically
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

    # Display Data View
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
                    badge_class = "badge-high" if "High" in str(w_req) else ("badge-low" if "Low" in str(w_req) else "badge-medium")
                    
                    st.markdown(
                        f"""
                        <div class="b360-card">
                            <div class="b360-card-title">🌱 {row.get('crop', 'Unknown')}</div>
                            <div style="margin-bottom: 8px;">
                                <span class="badge-neutral">{row.get('category', 'General')}</span>
                                <span class="{badge_class}">💧 {w_req} Water</span>
                            </div>
                            <p style="margin: 4px 0; font-size: 0.92rem; color: #444;">
                                <strong>Season:</strong> {row.get('season', 'N/A')}<br>
                                <strong>Input Requirement:</strong> {row.get('input_requirement', 'N/A')}<br>
                                <strong>Crop ID:</strong> #{row.get('id', 'N/A')}
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
                    "Very High": "#D32F2F",
                    "High": "#F57C00",
                    "Medium": "#FBC02D",
                    "Low": "#388E3C",
                },
            )
            fig.update_layout(margin=dict(t=40, l=10, r=10, b=10), height=380)
            st.plotly_chart(fig, use_container_width=True)


def _render_irrigation_advisor_section(crop_df: pd.DataFrame, irrigation_df: pd.DataFrame):
    """
    Section 3: Irrigation Advisor
    Rule-based recommendation engine.
    Inputs: Crop, Water availability, Irrigation preference.
    Outputs: Recommended irrigation approach and reasoning using dataset attributes.
    """
    st.markdown("### 💧 3. Irrigation Advisor")
    st.caption("Rule-based recommendation engine matching crops and water supplies to irrigation systems.")

    if irrigation_df.empty:
        st.warning("Irrigation dataset is currently empty or unavailable.")
        return

    # Advisor Inputs
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

    # Run Rule-Based Recommendation Engine
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
            <div class="rec-banner">
                <div style="font-size: 1.35rem; font-weight: 700; color: #1B5E20; margin-bottom: 6px;">
                    💧 Recommended irrigation approach: {top_method['method']}
                </div>
                <p style="font-size: 1rem; color: #2E382E; margin-bottom: 12px;">
                    {rec_result.get('reason', '')}
                </p>
                <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                    <span class="badge-neutral">⚡ Water Efficiency: {top_method['water_efficiency']}</span>
                    <span class="badge-low">💰 Cost Level: {top_method['cost_level']}</span>
                    <span class="badge-medium">🎯 Suitable For: {top_method['suitable_for']}</span>
                    <span class="badge-high">⭐ Rule Score: {top_method['score']} pts</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Dataset Attributes and Evaluation Table
    st.markdown("#### 📋 Comparative Irrigation Evaluation (Grounding in irrigation.csv)")
    if ranked:
        ranked_display_data = []
        for r in ranked:
            ranked_display_data.append({
                "Method": r["method"],
                "Water Efficiency": r["water_efficiency"],
                "Cost Level": r["cost_level"],
                "Suitable For (from dataset)": r["suitable_for"],
                "Rule Score": f"{r['score']} pts",
                "Dataset Attribute Justification": r["justification"],
            })
        st.dataframe(pd.DataFrame(ranked_display_data), use_container_width=True, hide_index=True)


def _render_rainfall_dashboard_section(rainfall_df: pd.DataFrame):
    """
    Section 4: Rainfall Dashboard
    Display rainfall information from rainfall.csv.
    Visualizations: Rainfall by district, District comparison, Annual rainfall.
    """
    st.markdown("### 🌧️ 4. Rainfall Dashboard")
    st.caption("Precipitation patterns, district comparisons, and baseline benchmarks from rainfall.csv.")

    if rainfall_df.empty:
        st.warning("Rainfall dataset is currently empty or unavailable.")
        return

    # Metric Cards
    avg_rainfall = rainfall_df["annual_rainfall_mm"].mean()
    max_row = rainfall_df.loc[rainfall_df["annual_rainfall_mm"].idxmax()]
    min_row = rainfall_df.loc[rainfall_df["annual_rainfall_mm"].idxmin()]
    user_dist = st.session_state.get("fp_district", rainfall_df["district"].iloc[0])
    user_dist_data = get_district_rainfall(rainfall_df, user_dist)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            f"""
            <div class="b360-metric">
                <div class="b360-metric-label">State Average Rainfall</div>
                <div class="b360-metric-value">{avg_rainfall:.1f} mm</div>
                <small style="color: #666;">Baseline across all districts</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f"""
            <div class="b360-metric">
                <div class="b360-metric-label">Selected: {user_dist}</div>
                <div class="b360-metric-value">{user_dist_data.get('annual_rainfall_mm', 0):.0f} mm</div>
                <small style="color: #666;">{user_dist_data.get('rainfall_diff_pct', 0):+.1f}% vs State Mean</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f"""
            <div class="b360-metric">
                <div class="b360-metric-label">Highest Rainfall District</div>
                <div class="b360-metric-value">{max_row['annual_rainfall_mm']} mm</div>
                <small style="color: #666;">{max_row['district']}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            f"""
            <div class="b360-metric">
                <div class="b360-metric-label">Lowest Rainfall District</div>
                <div class="b360-metric-value">{min_row['annual_rainfall_mm']} mm</div>
                <small style="color: #666;">{min_row['district']}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Visualizations using Plotly
    c_tab1, c_tab2, c_tab3 = st.tabs(["📊 Rainfall by District", "⚖️ District Comparison (Deviation)", "📑 Raw Rainfall Data"])

    with c_tab1:
        # Highlight selected district with a distinct color
        colors = ["#2E7D32" if d == user_dist else "#81C784" for d in rainfall_df["district"]]
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
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with c_tab2:
        # Deviation from average
        dev_df = rainfall_df.copy()
        dev_df["diff_pct"] = ((dev_df["annual_rainfall_mm"] - avg_rainfall) / avg_rainfall) * 100
        dev_df["color"] = dev_df["diff_pct"].apply(lambda x: "#2E7D32" if x >= 0 else "#C62828")

        fig_dev = go.Figure(go.Bar(
            x=dev_df["district"],
            y=dev_df["diff_pct"],
            marker_color=dev_df["color"],
            text=dev_df["diff_pct"].apply(lambda v: f"{v:+.1f}%"),
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Variance: %{y:+.1f}%<extra></extra>",
        ))
        fig_dev.add_hline(y=0, line_color="#424242", line_width=1)
        fig_dev.update_layout(
            title="District Rainfall Variance from State Average (%)",
            xaxis_title="District",
            yaxis_title="Deviation (%)",
            margin=dict(t=50, l=10, r=10, b=10),
            height=400,
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
    """
    Section 5: Sustainability Hub
    Display sustainable initiatives from sustainability.csv.
    Show: Initiative, Impact area, Potential impact, Target users.
    """
    st.markdown("### ♻️ 5. Sustainability Hub")
    st.caption("Explore sustainable interventions, water conservation models, and green farm practices.")

    if sustainability_df.empty:
        st.warning("Sustainability dataset is currently empty or unavailable.")
        return

    # Filters
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

    # Initiative Cards
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
                    impact_badge = "badge-high" if "High" in str(impact_lvl) else "badge-medium"
                    
                    st.markdown(
                        f"""
                        <div class="b360-card">
                            <div class="b360-card-title">🌱 {row.get('initiative', 'Initiative')}</div>
                            <div style="margin-bottom: 8px;">
                                <span class="badge-neutral">{row.get('impact_area', 'General')}</span>
                                <span class="{impact_badge}">⚡ Impact: {impact_lvl}</span>
                            </div>
                            <p style="margin: 6px 0; font-size: 0.9rem; color: #444;">
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
                color_discrete_map={"High": "#2E7D32", "Medium": "#F9A825"},
            )
            fig.update_layout(
                xaxis_title="Impact Area",
                yaxis_title="Count of Initiatives",
                margin=dict(t=50, l=10, r=10, b=10),
                height=380,
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
    Section 6: Smart Agriculture Recommendations
    Combine: selected crop, water availability, irrigation data, rainfall data, sustainability options.
    Provide transparent, rule-based recommendations. Clearly show the factors used.
    """
    st.markdown("### 🤖 6. Smart Agriculture Recommendations")
    st.caption("Multi-factor synthesis connecting agronomic demand, rainfall realities, and green practices.")

    # Current parameters from farmer profile
    crop = st.session_state.get("fp_crop", "Rice")
    district = st.session_state.get("fp_district", "Kakinada")
    water_avail = st.session_state.get("fp_water_avail", "Medium")
    pref = st.session_state.get("fp_irrig_pref", "Balanced / Any")

    # Run holistic multi-factor recommender
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

    # Top synthesis card
    stress_bg = "#FFEBEE" if "High" in stress.get("level", "") else ("#FFF8E1" if "Moderate" in stress.get("level", "") else "#E8F5E9")
    stress_border = "#EF5350" if "High" in stress.get("level", "") else ("#FFCA28" if "Moderate" in stress.get("level", "") else "#66BB6A")
    stress_text = "#C62828" if "High" in stress.get("level", "") else ("#E65100" if "Moderate" in stress.get("level", "") else "#2E7D32")

    st.markdown(
        f"""
        <div style="background-color: {stress_bg}; border: 2px solid {stress_border}; border-radius: 12px; padding: 1.4rem; margin-bottom: 1.5rem;">
            <div style="font-size: 1.25rem; font-weight: 700; color: {stress_text}; margin-bottom: 6px;">
                🌊 Water Stress Diagnosis: {stress.get('level', 'Normal')}
            </div>
            <p style="font-size: 0.98rem; color: #333333; margin: 0;">
                {stress.get('description', '')}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2 Recommendation Columns
    r_col1, r_col2 = st.columns(2)

    with r_col1:
        st.markdown(
            f"""
            <div class="b360-card" style="border-top: 4px solid #1E88E5; height: 100%;">
                <div class="b360-card-title">💧 Recommended Irrigation Pathway</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: #0D47A1; margin-bottom: 6px;">
                    {top_irrig['method'] if top_irrig else 'Canal / Drip'}
                </div>
                <p style="font-size: 0.9rem; color: #444;">
                    {irrig_rec.get('reason', '')}
                </p>
                <div style="margin-top: 10px;">
                    <span class="badge-neutral">Efficiency: {top_irrig['water_efficiency'] if top_irrig else 'N/A'}</span>
                    <span class="badge-low">Cost: {top_irrig['cost_level'] if top_irrig else 'N/A'}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with r_col2:
        st.markdown(
            """
            <div class="b360-card" style="border-top: 4px solid #43A047; height: 100%;">
                <div class="b360-card-title">♻️ Aligned Sustainable Initiatives</div>
                <p style="font-size: 0.88rem; color: #555; margin-bottom: 8px;">
                    Ground-level interventions matched from the sustainability catalog for farmers:
                </p>
            """,
            unsafe_allow_html=True,
        )
        if sust_recs:
            for s in sust_recs[:3]:
                st.markdown(
                    f"""
                    <div style="background: #F1F8E9; border-radius: 6px; padding: 6px 10px; margin-bottom: 6px;">
                        <strong>🌱 {s['initiative']}</strong> ({s['impact_area']})<br>
                        <small style="color: #444;">{s['relevance_reason']}</small>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("General sustainability practices apply.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Factors Used Table (Transparency Requirement)
    st.markdown("#### 🔍 Transparent Factors Used in Recommendations")
    st.caption("Every recommendation is strictly rule-based and derived directly from dataset attributes without invented claims.")

    st.dataframe(pd.DataFrame(factors_list), use_container_width=True, hide_index=True)


def render_agriculture_module():
    """
    Main entry point for the Bharat360 Agriculture & Sustainability Module.
    Can be invoked inside the unified Bharat360 app.py or tested standalone.
    """
    # 1. Render Hero Header
    _render_hero()

    # 2. Dynamic Data Loading with Graceful Fallbacks
    data = load_all_agriculture_data()
    crop_df = data.get("crop_data", pd.DataFrame())
    rainfall_df = data.get("rainfall", pd.DataFrame())
    irrigation_df = data.get("irrigation", pd.DataFrame())
    sustainability_df = data.get("sustainability", pd.DataFrame())

    # Handle dataset loading errors / missing files gracefully
    if not data.get("all_loaded", False):
        with st.expander("⚠️ Dataset Diagnostics & Status", expanded=True):
            st.error("Some agriculture datasets could not be located in standard candidate paths.")
            for err in data.get("errors", []):
                st.write(f"- {err}")
            st.info("The application will continue with available datasets and default schemas.")

    # 3. Initialize Interactive State
    _init_session_state(crop_df, rainfall_df)

    # 4. Profile Quick Summary Strip
    _render_profile_strip(crop_df, rainfall_df)

    # 5. View Mode Switcher
    c1, c2 = st.columns([3, 1])
    with c2:
        view_mode = st.radio("Dashboard View", ["📑 Tabbed Sections", "📜 Full Sequential Report"], horizontal=True, label_visibility="collapsed")

    if view_mode == "📑 Tabbed Sections":
        # Tabs rendered in order 1 through 6
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
        # Full Sequential Report Mode: all sections rendered linearly
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

    # 6. Prototype Disclaimer
    st.markdown(
        """
        <div class="b360-disclaimer">
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
