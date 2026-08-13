import streamlit as st

def inject_custom_styles():
    """Injects high-end enterprise CSS design system into Streamlit UI."""
    custom_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background: #080C14;
        color: #F1F5F9;
    }

    /* Enterprise Hero Banner */
    .hero-header {
        background: radial-gradient(circle at 10% 20%, rgba(14, 165, 233, 0.08) 0%, rgba(15, 23, 42, 0.6) 90%), #0F172A;
        border: 1px solid rgba(56, 189, 248, 0.18);
        border-radius: 12px;
        padding: 30px 40px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }

    .hero-tag {
        display: inline-block;
        background: rgba(14, 165, 233, 0.12);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 4px;
        padding: 3px 10px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .hero-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 2.1rem;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.6px;
        margin-bottom: 6px;
    }

    .hero-subtitle {
        font-size: 0.98rem;
        color: #94A3B8;
        font-weight: 400;
        letter-spacing: 0.1px;
    }

    /* Premium Metric Stat Cards */
    .stat-card {
        background: #0F172A;
        border: 1px solid #1E293B;
        border-top: 3px solid #0EA5E9;
        border-radius: 10px;
        padding: 18px 20px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .stat-card:hover {
        transform: translateY(-2px);
        border-color: #38BDF8;
    }
    .stat-number {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.7rem;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.2;
    }
    .stat-label {
        font-size: 0.75rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 6px;
        font-weight: 700;
    }

    /* Source Citation Cards */
    .citation-card {
        background: #0F172A;
        border: 1px solid #1E293B;
        border-left: 4px solid #0EA5E9;
        border-radius: 8px;
        padding: 14px 18px;
        margin-top: 10px;
        margin-bottom: 10px;
        font-size: 0.88rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    .citation-badge {
        display: inline-block;
        background: rgba(14, 165, 233, 0.15);
        color: #38BDF8;
        border: 1px solid rgba(14, 165, 233, 0.3);
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 0.72rem;
        font-weight: 700;
        margin-right: 8px;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Modern Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: #0F172A;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid #1E293B;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 10px 20px;
        color: #94A3B8;
        font-weight: 600;
        font-size: 0.88rem;
        border: none !important;
        transition: all 0.15s ease;
    }
    .stTabs [aria-selected="true"] {
        background: #0284C7 !important;
        color: #FFFFFF !important;
        font-weight: 700;
        box-shadow: 0 2px 10px rgba(2, 132, 199, 0.3);
    }

    /* Sidebar Container */
    section[data-testid="stSidebar"] {
        background: #0B0F19 !important;
        border-right: 1px solid #1E293B;
    }

    /* Premium Buttons */
    .stButton button {
        background: linear-gradient(180deg, #0284C7 0%, #0369A1 100%);
        color: white;
        border: 1px solid #0284C7;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 0.88rem;
        letter-spacing: 0.2px;
        transition: all 0.15s ease;
        box-shadow: 0 2px 8px rgba(2, 132, 199, 0.25);
    }
    .stButton button:hover {
        background: linear-gradient(180deg, #0369A1 0%, #075985 100%);
        border-color: #38BDF8;
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.4);
    }

    /* Input & Text Area styling */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: #0F172A !important;
        border: 1px solid #1E293B !important;
        color: #F8FAFC !important;
        border-radius: 8px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #0EA5E9 !important;
        box-shadow: 0 0 0 1px #0EA5E9 !important;
    }

    /* Tech Stack Tech Pills */
    .tech-pill {
        display: inline-block;
        background: rgba(14, 165, 233, 0.1);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 6px;
        padding: 5px 14px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 4px;
    }

    /* Footer Text */
    .footer-text {
        text-align: center;
        color: #475569;
        font-size: 0.82rem;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #1E293B;
        letter-spacing: 0.3px;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
