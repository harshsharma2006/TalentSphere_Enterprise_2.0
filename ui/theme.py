"""
TalentSphere Enterprise 2.0 - UI Theme & Design System
Light Blue + White Palette:
- Primary: #2563EB
- Dark Blue: #174A82
- Light Blue: #EFF6FF
- Background: #F8FAFC
- Cards: #FFFFFF
- Text: #1E293B
- Secondary: #64748B
- Border: #E2E8F0
- Success: #16A34A
- Warning: #D97706
- Danger: #DC2626
"""

import streamlit as st

THEME = {
    "primary": "#2563EB",
    "dark_blue": "#174A82",
    "light_blue": "#EFF6FF",
    "background": "#F8FAFC",
    "card": "#FFFFFF",
    "text": "#1E293B",
    "secondary": "#64748B",
    "border": "#E2E8F0",
    "success": "#16A34A",
    "warning": "#D97706",
    "danger": "#DC2626",
    "font_family": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
}

def apply_custom_theme():
    """Injects high-contrast enterprise light theme CSS styling into Streamlit."""
    custom_css = f"""
    <style>
        /* Import Google Inter Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* Global Reset & Base Styling - Force Light Mode Regardless of OS Settings */
        html, body, .stApp, [data-testid="stAppViewContainer"], .main {{
            font-family: {THEME['font_family']} !important;
            color: #1E293B !important;
            background-color: #F8FAFC !important;
        }}

        /* Header bar */
        header[data-testid="stHeader"] {{
            background-color: #F8FAFC !important;
        }}

        /* Main app container */
        .main .block-container {{
            padding-top: 1.5rem !important;
            padding-bottom: 3rem !important;
            max-width: 1280px !important;
            color: #1E293B !important;
        }}

        /* Hide Streamlit default header/footer */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}

        /* Typography - Deep Navy Contrast */
        h1, h2, h3, h4, h5, h6 {{
            font-family: {THEME['font_family']} !important;
            font-weight: 700 !important;
            color: #0F2D59 !important;
            letter-spacing: -0.02em !important;
        }}
        h1 {{ font-size: 1.85rem !important; margin-bottom: 0.5rem !important; }}
        h2 {{ font-size: 1.45rem !important; margin-top: 1rem !important; margin-bottom: 0.5rem !important; }}
        h3 {{ font-size: 1.15rem !important; margin-top: 0.8rem !important; margin-bottom: 0.4rem !important; }}

        /* General text elements */
        p, span, div, label, li {{
            color: #1E293B;
        }}

        /* Sidebar Styling - Clean White with Crisp Dark Text */
        section[data-testid="stSidebar"] {{
            background-color: #FFFFFF !important;
            border-right: 1px solid #E2E8F0 !important;
            box-shadow: 1px 0 3px rgba(0, 0, 0, 0.02) !important;
        }}
        section[data-testid="stSidebar"] .block-container {{
            padding-top: 1.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}

        /* Sidebar Radio Navigation Items */
        section[data-testid="stSidebar"] div[data-testid="stRadio"] {{
            gap: 0.25rem !important;
        }}
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label {{
            background-color: transparent !important;
            padding: 0.45rem 0.65rem !important;
            border-radius: 8px !important;
            transition: all 0.15s ease-in-out !important;
            cursor: pointer !important;
        }}
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {{
            background-color: #EFF6FF !important;
        }}
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label p {{
            color: #1E293B !important;
            font-weight: 600 !important;
            font-size: 0.925rem !important;
            margin: 0 !important;
        }}
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover p {{
            color: #2563EB !important;
        }}
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"] p,
        section[data-testid="stSidebar"] div[data-testid="stRadio"] [aria-checked="true"] + div p {{
            color: #2563EB !important;
            font-weight: 700 !important;
        }}

        /* Primary Button Styling */
        .stButton > button {{
            background: linear-gradient(135deg, #2563EB 0%, #174A82 100%) !important;
            color: #FFFFFF !important;
            border: 1px solid transparent !important;
            border-radius: 8px !important;
            padding: 0.5rem 1.25rem !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
            transition: all 0.2s ease-in-out !important;
        }}
        .stButton > button:hover {{
            background: linear-gradient(135deg, #1D4ED8 0%, #0F3260 100%) !important;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2) !important;
            transform: translateY(-1px) !important;
        }}
        .stButton > button p {{
            color: #FFFFFF !important;
        }}

        div[data-testid="stFormSubmitButton"] > button {{
            background: #2563EB !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }}
        div[data-testid="stFormSubmitButton"] > button p {{
            color: #FFFFFF !important;
        }}

        /* Form Controls - Crisp Light Inputs */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > div,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {{
            border-radius: 8px !important;
            border: 1px solid #CBD5E1 !important;
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            padding: 0.5rem 0.75rem !important;
            font-size: 0.925rem !important;
            font-weight: 500 !important;
        }}
        .stSelectbox span, .stSelectbox div {{
            color: #0F172A !important;
        }}

        /* Dropdowns menu */
        ul[data-testid="stSelectboxVirtualDropdown"] li,
        div[data-baseweb="popover"] div {{
            background-color: #FFFFFF !important;
            color: #0F172A !important;
        }}

        /* File Uploader styling */
        section[data-testid="stFileUploadDropzone"] {{
            background-color: #FFFFFF !important;
            border: 2px dashed #93C5FD !important;
            border-radius: 10px !important;
        }}
        section[data-testid="stFileUploadDropzone"] div,
        section[data-testid="stFileUploadDropzone"] span,
        section[data-testid="stFileUploadDropzone"] small {{
            color: #334155 !important;
        }}

        /* Card container */
        .ts-card {{
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 12px !important;
            padding: 1.25rem 1.5rem !important;
            margin-bottom: 1.25rem !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.02) !important;
            color: #1E293B !important;
        }}
        .ts-card:hover {{
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.07) !important;
        }}
        .ts-card p {{
            color: #334155 !important;
            font-size: 0.925rem !important;
        }}
        .ts-card h1, .ts-card h2, .ts-card h3, .ts-card h4, .ts-card h5, .ts-card h6 {{
            color: #0F2D59 !important;
        }}

        /* Metric cards */
        .ts-metric-card {{
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 10px !important;
            padding: 1rem 1.25rem !important;
            display: flex !important;
            flex-direction: column !important;
            gap: 0.25rem !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
            border-left: 4px solid #2563EB !important;
        }}
        .ts-metric-title {{
            font-size: 0.825rem !important;
            font-weight: 700 !important;
            color: #475569 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
        }}
        .ts-metric-val {{
            font-size: 1.85rem !important;
            font-weight: 800 !important;
            color: #0F172A !important;
            line-height: 1.2 !important;
        }}
        .ts-metric-sub {{
            font-size: 0.825rem !important;
            color: #64748B !important;
            font-weight: 500 !important;
        }}

        /* Badges */
        .ts-badge {{
            display: inline-block !important;
            padding: 0.25rem 0.65rem !important;
            border-radius: 9999px !important;
            font-size: 0.775rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.02em !important;
        }}
        .ts-badge-blue {{ background: #EFF6FF !important; color: #1D4ED8 !important; border: 1px solid #BFDBFE !important; }}
        .ts-badge-green {{ background: #DCFCE7 !important; color: #15803D !important; border: 1px solid #BBF7D0 !important; }}
        .ts-badge-yellow {{ background: #FEF3C7 !important; color: #92400E !important; border: 1px solid #FDE68A !important; }}
        .ts-badge-red {{ background: #FEE2E2 !important; color: #B91C1C !important; border: 1px solid #FECACA !important; }}
        .ts-badge-gray {{ background: #F1F5F9 !important; color: #475569 !important; border: 1px solid #E2E8F0 !important; }}

        /* DataTables */
        .dataframe {{
            border-collapse: collapse !important;
            width: 100% !important;
            border-radius: 8px !important;
            overflow: hidden !important;
            border: 1px solid #CBD5E1 !important;
            background-color: #FFFFFF !important;
        }}
        .dataframe th {{
            background-color: #F1F5F9 !important;
            color: #0F2D59 !important;
            font-weight: 700 !important;
            padding: 0.75rem 0.85rem !important;
            text-align: left !important;
            border-bottom: 1px solid #CBD5E1 !important;
        }}
        .dataframe td {{
            padding: 0.7rem 0.85rem !important;
            border-bottom: 1px solid #E2E8F0 !important;
            color: #1E293B !important;
            background-color: #FFFFFF !important;
        }}
        .dataframe tr:hover td {{
            background-color: #EFF6FF !important;
        }}

        /* Progress bars */
        .stProgress > div > div > div > div {{
            background-color: #2563EB !important;
            border-radius: 4px !important;
        }}

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 1.5rem !important;
            border-bottom: 2px solid #E2E8F0 !important;
        }}
        .stTabs [data-baseweb="tab"] {{
            padding-top: 0.5rem !important;
            padding-bottom: 0.75rem !important;
            font-weight: 600 !important;
            color: #64748B !important;
        }}
        .stTabs [aria-selected="true"] {{
            color: #2563EB !important;
            border-bottom: 2px solid #2563EB !important;
        }}

        /* Expander */
        .streamlit-expanderHeader {{
            color: #1E293B !important;
            font-weight: 600 !important;
        }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def render_badge(text: str, badge_type: str = "blue") -> str:
    """Renders a styled HTML badge."""
    return f'<span class="ts-badge ts-badge-{badge_type}">{text}</span>'
