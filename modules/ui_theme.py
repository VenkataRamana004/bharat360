"""
Bharat360 - Unified UI/UX Design System
Provides master CSS, dark navy civic-tech aesthetic, glassmorphism cards,
cinematic India landscape background, responsive layout, high-contrast input controls,
and consistent typography and spacing across all Bharat360 modules.

Strictly preserves 100% of underlying domain data, logic, and functionality.
"""

import base64
from functools import lru_cache
from pathlib import Path
import streamlit as st


@lru_cache(maxsize=1)
def get_cinematic_bg_b64() -> str:
    """Safely loads and caches the base64-encoded cinematic India background image."""
    bg_path = Path(__file__).resolve().parent.parent / "assets" / "bharat_cinematic_bg.jpg"
    if bg_path.exists():
        try:
            return base64.b64encode(bg_path.read_bytes()).decode("utf-8")
        except Exception:
            pass
    return ""


def get_master_css() -> str:
    """Builds and returns the master stylesheet incorporating the cinematic background and polished UI rules."""
    bg_b64 = get_cinematic_bg_b64()
    
    if bg_b64:
        bg_css = f"""
        background-color: #030D22 !important;
        background: 
            linear-gradient(90deg, rgba(3, 14, 34, 0.90) 0%, rgba(3, 16, 40, 0.72) 48%, rgba(5, 22, 54, 0.35) 100%),
            url("data:image/jpeg;base64,{bg_b64}") no-repeat center top fixed !important;
        background-size: cover !important;
        """
    else:
        bg_css = """
        background-color: #030D22 !important;
        background: linear-gradient(135deg, #030E22 0%, #06193E 50%, #0A2540 100%) !important;
        """

    return f"""
<style>
/* =========================================================
   BHARAT360 UNIFIED CIVIC-TECH DESIGN SYSTEM
   Dark Navy • Cinematic India Atmosphere • Glassmorphism
   Global Polish: High-Contrast Inputs • Generous Card Padding
   ========================================================= */

/* Global Typography & Font Smoothing */
html, body, [class*="css"], [class*="st-"] {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #F8FAFC !important;
}}

/* 1. Global App Canvas with Cinematic Background */
.stApp {{
    {bg_css}
    color: #F8FAFC !important;
}}

/* 2. Global Layout Optimization: Efficient Screen Usage, Equal Spacing */
.main .block-container {{
    padding-top: 0.8rem !important;
    padding-bottom: 2.2rem !important;
    padding-left: 1.8rem !important;
    padding-right: 1.8rem !important;
    max-width: 1440px !important;
}}

div[data-testid="stVerticalBlock"] > div {{
    gap: 0.75rem !important;
}}

div[data-testid="stHorizontalBlock"] {{
    align-items: stretch;
    gap: 1.0rem !important;
}}

/* Headings and Paragraphs Default High-Contrast */
h1, h2, h3, h4, h5, h6 {{
    color: #FFFFFF !important;
    letter-spacing: -0.3px;
}}

p, span, li {{
    color: #E2E8F0;
}}

/* 3. Subtle Indian Tricolor Brand Bar */
.b360-tricolor-bar {{
    height: 3.5px;
    background: linear-gradient(90deg, #FF9933 0%, #FF9933 33.3%, #FFFFFF 33.3%, #FFFFFF 66.6%, #138808 66.6%, #138808 100%);
    border-radius: 2px;
    margin-bottom: 0.75rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}}

/* 4. Top Viksit Bharat 2047 Pill */
.b360-top-viksit-pill {{
    background: rgba(8, 26, 54, 0.75);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(16, 185, 129, 0.45);
    border-radius: 20px;
    padding: 6px 14px;
    color: #F8FAFC;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.4px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
}}

/* 5. Reference Hero Section */
.b360-ref-hero {{
    padding: 0.8rem 0 1.2rem 0;
    max-width: 950px;
}}

.b360-ref-hero-title {{
    font-size: 3.2rem !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
    letter-spacing: -1.0px;
    margin: 0 0 0.35rem 0 !important;
    line-height: 1.1;
    display: flex;
    align-items: center;
    gap: 2px;
}}

.b360-ref-hero-sub {{
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
    letter-spacing: -0.4px;
    margin: 0 0 0.4rem 0 !important;
}}

.b360-ref-hero-desc {{
    font-size: 1.05rem !important;
    color: #94A3B8 !important;
    margin: 0 0 1.1rem 0 !important;
    line-height: 1.5;
}}

.b360-ref-hero-badges {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 0.5rem;
}}

.b360-ref-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.3px;
    background: rgba(10, 35, 70, 0.65);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25);
}}

.b360-ref-badge.badge-blue {{
    border: 1px solid rgba(59, 130, 246, 0.45);
    color: #93C5FD;
}}
.b360-ref-badge.badge-amber {{
    border: 1px solid rgba(245, 158, 11, 0.45);
    color: #FCD34D;
}}
.b360-ref-badge.badge-green {{
    border: 1px solid rgba(16, 185, 129, 0.45);
    color: #6EE7B7;
}}
.b360-ref-badge.badge-purple {{
    border: 1px solid rgba(139, 92, 246, 0.45);
    color: #C4B5FD;
}}

/* 6. Four Domain Glassmorphism Cards: Generous Internal Padding & Alignment */
.b360-ref-card {{
    background: rgba(8, 26, 54, 0.70);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 18px;
    padding: 24px 22px 20px 22px;
    min-height: 270px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.2s ease-in-out;
    position: relative;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}}

.b360-ref-card:hover {{
    transform: translateY(-3px);
    border-color: rgba(255, 255, 255, 0.25);
}}

.b360-ref-card.b360-card-edu {{
    border-bottom: 2.5px solid #2563EB;
    box-shadow: 0 8px 30px -4px rgba(37, 99, 235, 0.30);
}}
.b360-ref-card.b360-card-health {{
    border-bottom: 2.5px solid #EF4444;
    box-shadow: 0 8px 30px -4px rgba(239, 68, 68, 0.30);
}}
.b360-ref-card.b360-card-agri {{
    border-bottom: 2.5px solid #10B981;
    box-shadow: 0 8px 30px -4px rgba(16, 185, 129, 0.30);
}}
.b360-ref-card.b360-card-gov {{
    border-bottom: 2.5px solid #8B5CF6;
    box-shadow: 0 8px 30px -4px rgba(139, 92, 246, 0.30);
}}

.b360-ref-icon-circle {{
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.35rem;
    margin-bottom: 14px;
}}

.b360-ref-icon-circle.bg-blue {{
    background: #2563EB;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.5);
}}
.b360-ref-icon-circle.bg-coral {{
    background: #EF4444;
    box-shadow: 0 4px 14px rgba(239, 68, 68, 0.5);
}}
.b360-ref-icon-circle.bg-green {{
    background: #10B981;
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.5);
}}
.b360-ref-icon-circle.bg-purple {{
    background: #8B5CF6;
    box-shadow: 0 4px 14px rgba(139, 92, 246, 0.5);
}}

.b360-ref-card-title {{
    color: #FFFFFF !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    margin: 0 0 4px 0 !important;
    letter-spacing: -0.2px;
}}

.b360-ref-card-quote {{
    color: #94A3B8 !important;
    font-size: 0.84rem !important;
    font-weight: 400 !important;
    margin: 0 0 16px 0 !important;
    line-height: 1.45;
    min-height: 40px;
}}

.b360-ref-card-metric {{
    margin-top: auto;
    padding-top: 10px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
}}

.b360-ref-metric-val {{
    color: #F8FAFC !important;
    font-size: 1.12rem !important;
    font-weight: 800 !important;
    margin-bottom: 2px;
}}

.b360-ref-metric-sub {{
    color: #94A3B8 !important;
    font-size: 0.75rem !important;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* 7. Column-Specific Pill Explore Buttons (With intentional top margin) */
div[data-testid="column"]:has(.b360-card-edu) .stButton,
div[data-testid="column"]:has(.b360-card-health) .stButton,
div[data-testid="column"]:has(.b360-card-agri) .stButton,
div[data-testid="column"]:has(.b360-card-gov) .stButton {{
    margin-top: 6px !important;
}}

div[data-testid="column"]:has(.b360-card-edu) .stButton > button {{
    background: #2563EB !important;
    color: #FFFFFF !important;
    border: 1px solid #3B82F6 !important;
    border-radius: 24px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.55rem 1.4rem !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
    transition: all 0.2s ease-in-out !important;
}}
div[data-testid="column"]:has(.b360-card-edu) .stButton > button:hover {{
    background: #1D4ED8 !important;
    box-shadow: 0 6px 22px rgba(37, 99, 235, 0.65) !important;
    transform: translateY(-2px);
}}

div[data-testid="column"]:has(.b360-card-health) .stButton > button {{
    background: #EF4444 !important;
    color: #FFFFFF !important;
    border: 1px solid #F87171 !important;
    border-radius: 24px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.55rem 1.4rem !important;
    box-shadow: 0 4px 14px rgba(239, 68, 68, 0.4) !important;
    transition: all 0.2s ease-in-out !important;
}}
div[data-testid="column"]:has(.b360-card-health) .stButton > button:hover {{
    background: #DC2626 !important;
    box-shadow: 0 6px 22px rgba(239, 68, 68, 0.65) !important;
    transform: translateY(-2px);
}}

div[data-testid="column"]:has(.b360-card-agri) .stButton > button {{
    background: #10B981 !important;
    color: #FFFFFF !important;
    border: 1px solid #34D399 !important;
    border-radius: 24px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.55rem 1.4rem !important;
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4) !important;
    transition: all 0.2s ease-in-out !important;
}}
div[data-testid="column"]:has(.b360-card-agri) .stButton > button:hover {{
    background: #059669 !important;
    box-shadow: 0 6px 22px rgba(16, 185, 129, 0.65) !important;
    transform: translateY(-2px);
}}

div[data-testid="column"]:has(.b360-card-gov) .stButton > button {{
    background: #8B5CF6 !important;
    color: #FFFFFF !important;
    border: 1px solid #A78BFA !important;
    border-radius: 24px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.55rem 1.4rem !important;
    box-shadow: 0 4px 14px rgba(139, 92, 246, 0.4) !important;
    transition: all 0.2s ease-in-out !important;
}}
div[data-testid="column"]:has(.b360-card-gov) .stButton > button:hover {{
    background: #7C3AED !important;
    box-shadow: 0 6px 22px rgba(139, 92, 246, 0.65) !important;
    transform: translateY(-2px);
}}

/* 8. Bharat360 at a Glance Compact Metric Cards */
.b360-ref-glance-card {{
    background: rgba(10, 35, 70, 0.65);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 16px;
    padding: 18px 18px 16px 18px;
    text-align: center;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    transition: all 0.15s ease;
    min-height: 100px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}}

.b360-ref-glance-card:hover {{
    border-color: rgba(255, 255, 255, 0.25);
    transform: translateY(-2px);
}}

.b360-ref-glance-num {{
    font-size: 1.8rem;
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
}}

.b360-ref-glance-label {{
    font-size: 0.76rem;
    font-weight: 600;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 0;
}}

/* 9. Dark Sidebar Navigation Styling */
section[data-testid="stSidebar"] {{
    background-color: #041024 !important;
    background: linear-gradient(180deg, #041024 0%, #061733 100%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    min-width: 250px !important;
    max-width: 265px !important;
}}

section[data-testid="stSidebar"] .block-container {{
    padding-top: 1.2rem !important;
    padding-left: 1.0rem !important;
    padding-right: 1.0rem !important;
}}

.b360-sidebar-brand-ref {{
    padding: 12px 14px;
    background: rgba(8, 26, 54, 0.70);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 14px;
    margin-bottom: 12px;
}}

section[data-testid="stSidebar"] div[data-testid="stRadio"] > label {{
    display: none !important;
}}

section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] {{
    gap: 4px !important;
}}

section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label {{
    background: transparent;
    border-radius: 10px;
    padding: 8px 12px !important;
    color: #94A3B8 !important;
    transition: all 0.15s ease-in-out;
    cursor: pointer;
    margin-bottom: 2px;
    border: 1px solid transparent;
}}

section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {{
    background: rgba(255, 255, 255, 0.06) !important;
    color: #FFFFFF !important;
    border-color: rgba(255, 255, 255, 0.10) !important;
}}

section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"],
section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {{
    background: rgba(37, 99, 235, 0.22) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    border: 1px solid rgba(59, 130, 246, 0.45) !important;
    box-shadow: 0 2px 10px rgba(37, 99, 235, 0.25) !important;
}}

section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label div[data-testid="stMarkdownContainer"] p {{
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    margin: 0 !important;
    color: inherit !important;
}}

section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {{
    display: none !important;
}}

/* 10. General Backwards-Compatible Glass Card Styles for Domain Pages */
.b360-card, .b360-domain-card, .b360-metric-card, .b360-module-header {{
    background: rgba(8, 26, 54, 0.70) !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 18px !important;
    color: #F8FAFC !important;
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.25) !important;
}}

.b360-card {{
    padding: 22px 24px 20px 24px !important;
    margin-bottom: 12px !important;
}}

.b360-card p, .b360-card span, .b360-card div {{
    color: #E2E8F0;
}}

.b360-card strong, .b360-card h4, .b360-card h3 {{
    color: #FFFFFF !important;
}}

.b360-card-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 10px;
    gap: 12px;
}}

.b360-card-title {{
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
    margin: 0 !important;
    line-height: 1.35 !important;
}}

.b360-module-header {{
    padding: 1.25rem 1.6rem !important;
    margin-bottom: 1.0rem !important;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}}

.b360-module-title {{
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
    margin: 0 !important;
    display: flex;
    align-items: center;
    gap: 8px;
    letter-spacing: -0.3px;
}}

.b360-module-sub {{
    font-size: 0.92rem !important;
    color: #94A3B8 !important;
    margin: 3px 0 0 0 !important;
}}

.b360-metric-card {{
    padding: 20px 20px 18px 20px !important;
    text-align: center !important;
    margin-bottom: 8px !important;
    min-height: 108px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
    transition: all 0.2s ease-in-out !important;
}}

.b360-metric-card:hover {{
    transform: translateY(-2px) !important;
    border-color: rgba(255, 255, 255, 0.25) !important;
    box-shadow: 0 8px 26px rgba(0, 0, 0, 0.35) !important;
}}

.b360-metric-num {{
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    line-height: 1.15 !important;
    letter-spacing: -0.5px !important;
    margin-bottom: 6px !important;
}}

.b360-metric-label {{
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    color: #94A3B8 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.6px !important;
    margin: 0 !important;
}}

.b360-farmer-context-grid {{
    background: rgba(8, 26, 54, 0.75) !important;
    border: 1px solid rgba(16, 185, 129, 0.45) !important;
    border-radius: 18px !important;
    padding: 16px 24px !important;
    margin-bottom: 1.2rem !important;
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)) !important;
    gap: 14px 20px !important;
    align-items: center !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25) !important;
}}

.b360-fc-item {{
    display: flex !important;
    flex-direction: column !important;
    gap: 4px !important;
}}

.b360-fc-label {{
    font-size: 0.74rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    color: #34D399 !important;
}}

.b360-fc-val {{
    font-size: 1.0rem !important;
    font-weight: 700 !important;
    color: #F8FAFC !important;
    line-height: 1.2 !important;
}}

.b360-rec-box {{
    background: rgba(8, 26, 54, 0.80) !important;
    border: 1.5px solid rgba(16, 185, 129, 0.45) !important;
    border-radius: 18px !important;
    padding: 22px 26px !important;
    margin-bottom: 14px !important;
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.3) !important;
}}

.b360-rec-header {{
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    color: #34D399 !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    margin-bottom: 8px !important;
}}

/* 11. Form Inputs and Controls - High Contrast Visibility (FIX 2) */

/* Input Labels */
label[data-testid="stWidgetLabel"] p,
label[data-testid="stWidgetLabel"] {{
    color: #CBD5E1 !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    margin-bottom: 4px !important;
}}

/* Number Input: Container, Wrapper, and Input Field (Across All Modules) */
div[data-testid="stNumberInput"] {{
    width: 100% !important;
}}

div[data-testid="stNumberInputContainer"],
div[data-testid="stNumberInput"] div[data-baseweb="input"],
div[data-testid="stNumberInput"] div[data-baseweb="base-input"] {{
    background-color: #071935 !important;
    background: #071935 !important;
    border: 1px solid rgba(255, 255, 255, 0.25) !important;
    border-radius: 12px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    color: #FFFFFF !important;
}}

div[data-testid="stNumberInputContainer"]:focus-within,
div[data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within,
div[data-testid="stNumberInput"] div[data-baseweb="base-input"]:focus-within {{
    border-color: #38BDF8 !important;
    box-shadow: 0 0 0 1px #38BDF8 !important;
}}

div[data-testid="stNumberInput"] input,
input[data-testid="stNumberInputField"] {{
    background-color: transparent !important;
    background: transparent !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 1.0rem !important;
    padding: 8px 12px !important;
    -webkit-text-fill-color: #FFFFFF !important;
}}

/* Step Buttons (- and +) with High Contrast Tile and Hover Glow */
button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"],
div[data-testid="stNumberInput"] button {{
    background-color: rgba(255, 255, 255, 0.18) !important;
    background: rgba(255, 255, 255, 0.18) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.25) !important;
    border-radius: 8px !important;
    margin: 3px 2px !important;
    width: 32px !important;
    height: 32px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    transition: all 0.15s ease-in-out !important;
}}

button[data-testid="stNumberInputStepDown"]:hover,
button[data-testid="stNumberInputStepUp"]:hover,
div[data-testid="stNumberInput"] button:hover {{
    background-color: #2563EB !important;
    background: #2563EB !important;
    border-color: #38BDF8 !important;
    color: #FFFFFF !important;
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.5) !important;
}}

button[data-testid="stNumberInputStepDown"] svg,
button[data-testid="stNumberInputStepUp"] svg,
div[data-testid="stNumberInput"] button svg {{
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
    color: #FFFFFF !important;
    width: 14px !important;
    height: 14px !important;
}}

/* Select Boxes: Container, Text, Dropdown Arrow */
div[data-baseweb="select"] {{
    border-radius: 12px !important;
}}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
div[data-baseweb="select"] > div {{
    background-color: #071935 !important;
    background: #071935 !important;
    border: 1px solid rgba(255, 255, 255, 0.25) !important;
    border-radius: 12px !important;
    color: #FFFFFF !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover,
div[data-baseweb="select"] > div:hover {{
    border-color: rgba(56, 189, 248, 0.6) !important;
}}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="select"] > div:focus-within {{
    border-color: #38BDF8 !important;
    box-shadow: 0 0 0 1px #38BDF8 !important;
}}

div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
div[data-baseweb="select"] div[aria-selected="true"],
div[data-baseweb="select"] span {{
    color: #FFFFFF !important;
    font-weight: 600 !important;
    -webkit-text-fill-color: #FFFFFF !important;
}}

div[data-baseweb="select"] svg {{
    fill: #94A3B8 !important;
    stroke: #94A3B8 !important;
    color: #94A3B8 !important;
    width: 18px !important;
    height: 18px !important;
    transition: fill 0.15s ease, color 0.15s ease !important;
}}

div[data-baseweb="select"]:hover svg {{
    fill: #38BDF8 !important;
    stroke: #38BDF8 !important;
    color: #38BDF8 !important;
}}

/* MultiSelect Tags / Pills */
div[data-baseweb="tag"] {{
    background-color: rgba(37, 99, 235, 0.30) !important;
    border: 1px solid rgba(59, 130, 246, 0.5) !important;
    border-radius: 8px !important;
}}

div[data-baseweb="tag"] span {{
    color: #F8FAFC !important;
    font-weight: 600 !important;
    -webkit-text-fill-color: #F8FAFC !important;
}}

div[data-baseweb="tag"] svg {{
    fill: #CBD5E1 !important;
}}

/* Dropdown Menu List Popovers & Streamlit 1.45+ Virtual Dropdown (OPEN STATE) */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="menu"],
div[data-baseweb="menu"] > div,
ul[data-testid="stSelectboxVirtualDropdown"],
ul[role="listbox"] {{
    background-color: #071935 !important;
    background: #071935 !important;
    border: 1px solid rgba(255, 255, 255, 0.22) !important;
    border-radius: 12px !important;
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.75) !important;
    color: #FFFFFF !important;
}}

/* All Dropdown Options / Items inside Virtual List */
ul[data-testid="stSelectboxVirtualDropdown"] li,
ul[role="listbox"] li,
div[data-baseweb="menu"] li,
div[data-baseweb="popover"] li,
li[role="option"],
div[role="option"] {{
    background-color: #071935 !important;
    background: #071935 !important;
    color: #F8FAFC !important;
    font-weight: 500 !important;
    font-size: 0.92rem !important;
    padding: 10px 16px !important;
    cursor: pointer !important;
    transition: background-color 0.12s ease !important;
    -webkit-text-fill-color: #F8FAFC !important;
}}

/* Ensure all nested text inside options is bright and readable */
ul[data-testid="stSelectboxVirtualDropdown"] li *,
ul[role="listbox"] li *,
div[data-baseweb="menu"] li *,
div[data-baseweb="popover"] li *,
li[role="option"] *,
div[role="option"] * {{
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
}}

/* Option Hover and Selected States */
ul[data-testid="stSelectboxVirtualDropdown"] li:hover,
ul[data-testid="stSelectboxVirtualDropdown"] li[aria-selected="true"],
ul[role="listbox"] li:hover,
ul[role="listbox"] li[aria-selected="true"],
div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] li[aria-selected="true"],
li[role="option"]:hover,
li[role="option"][aria-selected="true"] {{
    background-color: #1D4ED8 !important;
    background: #1D4ED8 !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}}

ul[data-testid="stSelectboxVirtualDropdown"] li:hover *,
ul[data-testid="stSelectboxVirtualDropdown"] li[aria-selected="true"] *,
ul[role="listbox"] li:hover *,
ul[role="listbox"] li[aria-selected="true"] *,
div[data-baseweb="popover"] li:hover *,
div[data-baseweb="popover"] li[aria-selected="true"] *,
li[role="option"]:hover *,
li[role="option"][aria-selected="true"] * {{
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}}

/* Text Input Fields */
div[data-testid="stTextInput"] div[data-baseweb="input"],
div[data-testid="stTextInput"] div[data-baseweb="base-input"] {{
    background-color: #071935 !important;
    background: #071935 !important;
    border: 1px solid rgba(255, 255, 255, 0.25) !important;
    border-radius: 12px !important;
}}

div[data-testid="stTextInput"] input {{
    background-color: transparent !important;
    background: transparent !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    padding: 8px 12px !important;
    -webkit-text-fill-color: #FFFFFF !important;
}}

div[data-testid="stTextInput"] input::placeholder {{
    color: #94A3B8 !important;
    -webkit-text-fill-color: #94A3B8 !important;
}}

/* Checkboxes */
div[data-testid="stCheckbox"] {{
    padding: 4px 0 !important;
}}

div[data-testid="stCheckbox"] label {{
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    cursor: pointer !important;
}}

div[data-testid="stCheckbox"] label span {{
    color: #E2E8F0 !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
}}

div[data-testid="stCheckbox"] div[role="checkbox"] {{
    border-color: rgba(255, 255, 255, 0.40) !important;
    background-color: rgba(8, 24, 48, 0.85) !important;
    border-radius: 6px !important;
}}

div[data-testid="stCheckbox"] div[role="checkbox"][aria-checked="true"] {{
    background-color: #2563EB !important;
    border-color: #38BDF8 !important;
}}

div[data-testid="stCheckbox"] svg {{
    stroke: #FFFFFF !important;
}}

/* Radio Buttons in Main Content */
.main div[data-testid="stRadio"] label p {{
    color: #CBD5E1 !important;
    font-weight: 600 !important;
}}

.main div[data-testid="stRadio"] div[role="radiogroup"] label {{
    color: #E2E8F0 !important;
    padding: 4px 8px !important;
    cursor: pointer !important;
}}

.main div[data-testid="stRadio"] div[role="radiogroup"] label:hover {{
    color: #FFFFFF !important;
}}

.main div[data-testid="stRadio"] div[role="radiogroup"] label span {{
    color: #E2E8F0 !important;
    font-size: 0.9rem !important;
}}

/* Sliders */
div[data-testid="stSlider"] {{
    padding: 6px 0 !important;
}}

div[data-testid="stSlider"] label p {{
    color: #CBD5E1 !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
}}

div[data-baseweb="slider"] div[role="slider"] {{
    background-color: #38BDF8 !important;
    border: 2px solid #FFFFFF !important;
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.6) !important;
    width: 20px !important;
    height: 20px !important;
}}

div[data-testid="stSlider"] [data-testid="stTickBar"] div,
div[data-testid="stSlider"] div[data-testid="stThumbValue"],
div[data-testid="stSlider"] div[data-testid="stTickBarMin"],
div[data-testid="stSlider"] div[data-testid="stTickBarMax"] {{
    color: #94A3B8 !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
}}

/* 12. Tabs Modernization */
div[data-testid="stTabs"] > div[role="tablist"] {{
    gap: 8px;
    border-bottom: 1.5px solid rgba(255, 255, 255, 0.12);
    padding-bottom: 0px;
}}

button[data-baseweb="tab"] {{
    padding: 10px 18px !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    border-radius: 8px 8px 0 0 !important;
    color: #94A3B8 !important;
    border: none !important;
    background: transparent !important;
    transition: all 0.15s ease !important;
}}

button[data-baseweb="tab"]:hover {{
    color: #FFFFFF !important;
    background: rgba(255, 255, 255, 0.06) !important;
}}

button[data-baseweb="tab"][aria-selected="true"] {{
    color: #38BDF8 !important;
    font-weight: 700 !important;
    border-bottom: 2.5px solid #38BDF8 !important;
}}

/* 13. General Streamlit Buttons */
.stButton > button {{
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.55rem 1.1rem !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    background-color: rgba(10, 35, 70, 0.65) !important;
    color: #F8FAFC !important;
    transition: all 0.15s ease-in-out !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25) !important;
}}

.stButton > button:hover {{
    border-color: #38BDF8 !important;
    color: #FFFFFF !important;
    background-color: rgba(14, 45, 90, 0.85) !important;
    box-shadow: 0 4px 14px rgba(56, 189, 248, 0.25) !important;
    transform: translateY(-1px);
}}

/* Back to Home Buttons */
.stButton > button[key="top_back_home"],
.stButton > button[key="sidebar_back_home"] {{
    background: rgba(37, 99, 235, 0.22) !important;
    border: 1px solid rgba(59, 130, 246, 0.45) !important;
    color: #93C5FD !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}}

.stButton > button[key="top_back_home"]:hover,
.stButton > button[key="sidebar_back_home"]:hover {{
    background: rgba(37, 99, 235, 0.45) !important;
    border-color: #38BDF8 !important;
    color: #FFFFFF !important;
}}

/* 14. Expanders & Metrics */
div[data-testid="stExpander"] {{
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 18px !important;
    background: rgba(8, 26, 54, 0.70) !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.25) !important;
    margin-bottom: 12px !important;
    overflow: hidden !important;
}}

div[data-testid="stExpander"] summary {{
    color: #FFFFFF !important;
    font-weight: 600 !important;
    padding: 12px 18px !important;
}}

div[data-testid="stExpander"] details > div {{
    padding: 18px 22px 22px 22px !important;
}}

div[data-testid="stMetric"] {{
    background: rgba(8, 26, 54, 0.70) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 18px !important;
    padding: 18px 22px !important;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.25) !important;
}}

div[data-testid="stMetricLabel"] {{
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    color: #94A3B8 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    margin-bottom: 4px !important;
}}

div[data-testid="stMetricValue"] {{
    font-size: 1.7rem !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
    line-height: 1.2 !important;
}}

/* 15. Streamlit DataFrames */
div[data-testid="stDataFrame"] {{
    background: rgba(8, 24, 48, 0.75) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 16px !important;
    padding: 8px !important;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.25) !important;
}}

/* 16. Disclaimers and Notices */
.b360-disclaimer {{
    background-color: rgba(50, 30, 5, 0.70);
    border-left: 4px solid #F59E0B;
    padding: 14px 18px;
    border-radius: 0 14px 14px 0;
    margin: 12px 0;
    color: #FDE68A;
    font-size: 0.86rem;
    line-height: 1.45;
}}

.b360-disclaimer-info {{
    background-color: rgba(10, 30, 60, 0.70);
    border-left: 4px solid #3B82F6;
    padding: 14px 18px;
    border-radius: 0 14px 14px 0;
    margin: 12px 0;
    color: #BFDBFE;
    font-size: 0.86rem;
    line-height: 1.45;
}}

/* 17. Compact Footer */
.b360-footer {{
    border-top: 1px solid rgba(255, 255, 255, 0.10);
    padding: 1.2rem 0;
    margin-top: 2.2rem;
    text-align: center;
    color: #94A3B8;
    font-size: 0.82rem;
    line-height: 1.5;
}}

.b360-footer strong {{
    color: #FFFFFF;
}}

/* 18. Empty States */
.b360-empty-state {{
    background: rgba(8, 26, 54, 0.65);
    border: 1.5px dashed rgba(255, 255, 255, 0.18);
    border-radius: 18px;
    padding: 2.2rem;
    text-align: center;
    color: #94A3B8;
    margin: 1.2rem 0;
}}
.b360-empty-state h4 {{
    color: #FFFFFF;
    margin-bottom: 0.4rem;
}}

/* 19. Badges */
.b360-badge {{
    display: inline-block;
    font-size: 0.76rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 8px;
    margin-right: 6px;
    margin-bottom: 6px;
    letter-spacing: 0.3px;
}}
.badge-blue {{ background-color: rgba(37, 99, 235, 0.25); color: #93C5FD; border: 1px solid rgba(59, 130, 246, 0.45); }}
.badge-green {{ background-color: rgba(16, 185, 129, 0.25); color: #6EE7B7; border: 1px solid rgba(16, 185, 129, 0.45); }}
.badge-amber {{ background-color: rgba(245, 158, 11, 0.25); color: #FDE68A; border: 1px solid rgba(245, 158, 11, 0.45); }}
.badge-purple {{ background-color: rgba(139, 92, 246, 0.25); color: #DDD6FE; border: 1px solid rgba(139, 92, 246, 0.45); }}
.badge-red {{ background-color: rgba(239, 68, 68, 0.25); color: #FECACA; border: 1px solid rgba(239, 68, 68, 0.45); }}
.badge-gray {{ background-color: rgba(255, 255, 255, 0.08); color: #CBD5E1; border: 1px solid rgba(255, 255, 255, 0.15); }}
.badge-teal {{ background-color: rgba(13, 148, 136, 0.25); color: #99F6E4; border: 1px solid rgba(13, 148, 136, 0.45); }}

/* 20. Plotly Charts and Alert Dark Theme Integration */
.js-plotly-plot, .plotly, .plotly div {{
    background: transparent !important;
}}
.js-plotly-plot .bg {{
    fill: transparent !important;
}}
.js-plotly-plot .gridlayer path {{
    stroke: rgba(255, 255, 255, 0.10) !important;
}}
.js-plotly-plot .zerolinelayer path {{
    stroke: rgba(255, 255, 255, 0.20) !important;
}}
.js-plotly-plot text {{
    fill: #CBD5E1 !important;
}}

div[data-testid="stAlert"] {{
    background: rgba(10, 35, 70, 0.70) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 14px !important;
    color: #F8FAFC !important;
}}

/* 21. Responsive Media Queries */
@media (max-width: 900px) {{
    .main .block-container {{
        padding-left: 1.0rem !important;
        padding-right: 1.0rem !important;
    }}
    .b360-ref-hero-title {{
        font-size: 2.4rem !important;
    }}
    .b360-ref-hero-sub {{
        font-size: 1.35rem !important;
    }}
}}
</style>
"""


def inject_master_styles():
    """Injects the global Bharat360 master stylesheet into the active page."""
    st.markdown(get_master_css(), unsafe_allow_html=True)


def render_brand_bar():
    """Renders the subtle Indian tricolor brand bar."""
    st.markdown('<div class="b360-tricolor-bar"></div>', unsafe_allow_html=True)


def render_compact_footer():
    """Renders the standardized, compact hackathon footer."""
    st.markdown(
        """
        <div class="b360-footer">
            <strong>Bharat360</strong> — One Platform. Multiple Needs.<br>
            <span>Technology-driven insights for a developed Bharat • <strong>Viksit Bharat 2047</strong></span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(message: str = "No matching results found.", suggestion: str = "Try changing or resetting your filters."):
    """Renders a responsive, clean empty state when filters return zero results."""
    st.markdown(
        f"""
        <div class="b360-empty-state">
            <div style="font-size: 2.0rem; margin-bottom: 4px;">🔍</div>
            <h4 style="margin: 0 0 4px 0;">{message}</h4>
            <p style="margin: 0; font-size: 0.88rem;">{suggestion}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
