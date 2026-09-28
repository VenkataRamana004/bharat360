"""
Bharat360 - One Platform. Multiple Needs.
Viksit Bharat 2047 Hackathon Project.
Unified Streamlit Application entrypoint.
"""

import streamlit as st
from modules.agriculture import render_agriculture_module

# Configure page settings at application root
st.set_page_config(
    page_title="Bharat360 - One Platform. Multiple Needs.",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    # Sidebar Navigation for the Unified Bharat360 App
    st.sidebar.markdown(
        """
        <div style="padding: 10px 0; text-align: center;">
            <h2 style="margin: 0; color: #1B5E20; font-weight: 800;">🇮🇳 Bharat360</h2>
            <p style="margin: 0; font-size: 0.85rem; color: #555;">One Platform. Multiple Needs.<br><strong>Viksit Bharat 2047</strong></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")

    modules_list = [
        "🌾 Agriculture & Sustainability (Member 3)",
        "🎓 Education & Skills (Member 1)",
        "🏥 Healthcare & Wellness (Member 2)",
        "🏛️ Governance, Finance & Mobility (Member 4)",
    ]

    selected_module = st.sidebar.radio(
        "Select Bharat360 Domain:",
        modules_list,
        index=0,
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("🚀 Hackathon Team: 4 Members | Unified Prototype v1.0")

    if selected_module == "🌾 Agriculture & Sustainability (Member 3)":
        render_agriculture_module()
    elif selected_module == "🎓 Education & Skills (Member 1)":
        st.info("📚 **Education & Skills Module** is under active development by Member 1.")
        st.caption("Available Datasets: education_institutions.csv, scholarships.csv, skill_programs.csv")
    elif selected_module == "🏥 Healthcare & Wellness (Member 2)":
        st.info("🏥 **Healthcare & Wellness Module** is under active development by Member 2.")
        st.caption("Available Datasets: health_awareness.csv, health_services.csv, hospitals.csv")
    elif selected_module == "🏛️ Governance, Finance & Mobility (Member 4)":
        st.info("🏛️ **Governance, Finance & Mobility Module** is under active development by Member 4.")
        st.caption("Available Datasets: financial_inclusion.csv, government_schemes.csv, transport.csv")


if __name__ == "__main__":
    main()
