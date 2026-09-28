"""
Bharat360 - Unified UI/UX Design System
Provides master CSS, consistent typography, card systems, compact metrics,
navigation helpers, and responsive layout styling across all Bharat360 modules.
"""

import streamlit as st

MASTER_CSS = """
<style>
/* =========================================================
   BHARAT360 UNIFIED DESIGN SYSTEM
   Indian Civic-Tech • Modern • Premium • Space-Optimized
   ========================================================= */

/* 1. Global Layout Optimization: Eliminate Excessive Empty Spaces */
.main .block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 1360px !important;
}

/* Reduce vertical gaps between Streamlit elements */
div[data-testid="stVerticalBlock"] > div {
    gap: 0.65rem !important;
}

div[data-testid="stHorizontalBlock"] {
    align-items: stretch;
    gap: 0.75rem !important;
}

/* 2. Indian Tricolor Brand Bar */
.b360-tricolor-bar {
    height: 4px;
    background: linear-gradient(90deg, #FF9933 0%, #FF9933 33.3%, #FFFFFF 33.3%, #FFFFFF 66.6%, #138808 66.6%, #138808 100%);
    border-radius: 2px;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* 3. Hero Sections - Compact & Impactful */
.b360-landing-hero {
    background: linear-gradient(135deg, #071E3D 0%, #0F3460 50%, #162447 100%);
    border-radius: 16px;
    padding: 2.2rem 2.6rem;
    color: #FFFFFF;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 24px rgba(7, 30, 61, 0.2);
    position: relative;
    overflow: hidden;
    border-left: 6px solid #FF9933;
}

.b360-landing-hero::after {
    content: "🇮🇳";
    position: absolute;
    right: 24px;
    bottom: -10px;
    font-size: 7rem;
    opacity: 0.12;
    pointer-events: none;
}

.b360-landing-title {
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
    margin: 0 0 0.4rem 0 !important;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.b360-landing-subtitle {
    font-size: 1.25rem !important;
    font-weight: 600 !important;
    color: #FFB74D !important;
    margin: 0 0 0.6rem 0 !important;
}

.b360-landing-desc {
    font-size: 1rem !important;
    color: #E2E8F0 !important;
    max-width: 820px;
    line-height: 1.5;
    margin: 0 0 1rem 0 !important;
}

.b360-tag-pill {
    display: inline-block;
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.25);
    color: #FFFFFF;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 3px 12px;
    border-radius: 20px;
    margin-right: 8px;
    letter-spacing: 0.4px;
}

/* 4. Compact Module Header */
.b360-module-header {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}

.b360-module-title {
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    color: #0B2545 !important;
    margin: 0 !important;
    display: flex;
    align-items: center;
    gap: 10px;
}

.b360-module-sub {
    font-size: 0.92rem !important;
    color: #64748B !important;
    margin: 3px 0 0 0 !important;
}

/* 5. Standardized Dashboard Cards */
.b360-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 12px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
    transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.b360-card:hover {
    box-shadow: 0 6px 16px rgba(11, 37, 69, 0.09);
    border-color: #CBD5E1;
    transform: translateY(-2px);
}

.b360-card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 8px;
}

.b360-card-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #0B2545;
    margin: 0;
    line-height: 1.3;
}

/* Domain Navigation Cards on Landing Page */
.b360-domain-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 20px;
    height: 100%;
    box-shadow: 0 3px 10px rgba(0,0,0,0.04);
    transition: all 0.2s ease-in-out;
    border-top: 4px solid #1E88E5;
}

.b360-domain-card:hover {
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    transform: translateY(-3px);
}

.b360-domain-icon {
    font-size: 2.2rem;
    margin-bottom: 10px;
}

.b360-domain-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 6px;
}

.b360-domain-desc {
    font-size: 0.9rem;
    color: #64748B;
    line-height: 1.45;
    margin-bottom: 14px;
    min-height: 48px;
}

/* 6. Metric Cards */
.b360-metric-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 12px 14px;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03);
    margin-bottom: 8px;
}

.b360-metric-num {
    font-size: 1.7rem;
    font-weight: 800;
    color: #0B2545;
    line-height: 1.2;
}

.b360-metric-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 2px;
}

/* 7. Recommendation Banner & Highlight */
.b360-rec-box {
    background: linear-gradient(135deg, #F0FDF4 0%, #ECFDF5 100%);
    border: 1.5px solid #86EFAC;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 14px;
    box-shadow: 0 2px 8px rgba(22, 163, 74, 0.08);
}

.b360-rec-header {
    font-size: 1.25rem;
    font-weight: 700;
    color: #166534;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
}

/* 8. Standardized Badges */
.b360-badge {
    display: inline-block;
    font-size: 0.76rem;
    font-weight: 600;
    padding: 2.5px 8px;
    border-radius: 6px;
    margin-right: 5px;
    margin-bottom: 4px;
}

.badge-blue { background-color: #E0F2FE; color: #0369A1; border: 1px solid #BAE6FD; }
.badge-green { background-color: #DCFCE7; color: #166534; border: 1px solid #BBF7D0; }
.badge-amber { background-color: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
.badge-purple { background-color: #F3E8FF; color: #6B21A8; border: 1px solid #E9D5FF; }
.badge-red { background-color: #FEE2E2; color: #991B1B; border: 1px solid #FECACA; }
.badge-gray { background-color: #F1F5F9; color: #475569; border: 1px solid #E2E8F0; }

/* 9. Compact Tabs & Controls */
button[data-baseweb="tab"] {
    padding: 8px 18px !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
}

/* 10. Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #F8FAFC !important;
    border-right: 1px solid #E2E8F0 !important;
}

.b360-sidebar-brand {
    padding: 12px 14px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    margin-bottom: 12px;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
}

/* 11. Footer */
.b360-footer {
    border-top: 1px solid #E2E8F0;
    padding: 1.2rem 0;
    margin-top: 2.5rem;
    text-align: center;
    color: #64748B;
    font-size: 0.85rem;
}

.b360-footer strong {
    color: #0B2545;
}

/* 12. Empty States */
.b360-empty-state {
    background: #F8FAFC;
    border: 1.5px dashed #CBD5E1;
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    color: #64748B;
    margin: 1rem 0;
}
.b360-empty-state h4 {
    color: #334155;
    margin-bottom: 0.3rem;
}
</style>
"""


def inject_master_styles():
    """Injects the global Bharat360 master stylesheet into the active page."""
    st.markdown(MASTER_CSS, unsafe_allow_html=True)


def render_brand_bar():
    """Renders the subtle Indian tricolor brand bar."""
    st.markdown('<div class="b360-tricolor-bar"></div>', unsafe_allow_html=True)


def render_compact_footer():
    """Renders the standardized, compact hackathon footer."""
    st.markdown(
        """
        <div class="b360-footer">
            <strong>Bharat360</strong> — One Platform. Multiple Needs.<br>
            <span>Built for the <strong>Innovation for Viksit Bharat 2047</strong> Open Innovation Challenge.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(message: str = "No matching results found.", suggestion: str = "Try changing or resetting your filters."):
    """Renders a responsive, clean empty state when filters return zero results."""
    st.markdown(
        f"""
        <div class="b360-empty-state">
            <div style="font-size: 2.2rem; margin-bottom: 6px;">🔍</div>
            <h4 style="margin: 0 0 4px 0;">{message}</h4>
            <p style="margin: 0; font-size: 0.9rem;">{suggestion}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
