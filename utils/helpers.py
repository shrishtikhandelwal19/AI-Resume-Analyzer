import streamlit as st

def load_css(file_path):
    """Loads a CSS file and injects it into the Streamlit app."""
    try:
        with open(file_path, "r") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading CSS: {e}")

def local_css_theme():
    """Injects state-dependent theme classes with scoped selectors that do not break native form widgets."""
    if "theme" not in st.session_state:
        st.session_state["theme"] = "dark"
    
    # Base layout styles for Streamlit blocks to remove excessive padding
    st.markdown("""
        <style>
            .block-container {
                padding-top: 2rem !important;
                padding-bottom: 2rem !important;
                max-width: 1200px !important;
            }
            div.stButton > button {
                border-radius: 8px !important;
            }
        </style>
    """, unsafe_allow_html=True)

    if st.session_state["theme"] == "light":
        st.markdown("""
            <style>
                /* Inject light mode base overlay */
                .stApp {
                    background: radial-gradient(circle at 50% 50%, #f4f5fa, #e9ecf5) !important;
                }
                
                /* Scoped text and card colors for light theme */
                .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
                .resume-analyzer-header p,
                .glass-card, .glass-card h3, .glass-card h4, .glass-card p, .glass-card b {
                    color: #1e1e2f !important;
                }
                
                /* Target only user custom page elements and paragraphs inside markdown */
                .stMarkdown p, .stMarkdown li, .stMarkdown div, .stMarkdown label:not([data-testid="stWidgetLabel"]) {
                    color: #1e1e2f !important;
                }
                
                .glass-card {
                    background: rgba(255, 255, 255, 0.75) !important;
                    border: 1px solid rgba(0, 0, 0, 0.08) !important;
                    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05) !important;
                }
                
                /* Light Mode Sidebar Settings */
                [data-testid="stSidebar"] {
                    background-color: #ffffff !important;
                    border-right: 1px solid rgba(0, 0, 0, 0.08) !important;
                }
                [data-testid="stSidebar"] p, [data-testid="stSidebar"] caption {
                    color: #4b5563 !important;
                }
                
                /* Circular metrics overrides */
                .circle-chart-text {
                    color: #1e1e2f !important;
                }
                .circle-chart-bg {
                    stroke: rgba(0, 0, 0, 0.08) !important;
                }
                .skill-badge-neutral {
                    background: rgba(0, 0, 0, 0.05) !important;
                    color: #4b5563 !important;
                }
                
                /* Sidebar Buttons in Light Mode */
                [data-testid="stSidebar"] div.stButton > button {
                    background-color: transparent !important;
                    border: none !important;
                    color: #4b5563 !important;
                    text-align: left !important;
                    padding: 10px 15px !important;
                    width: 100% !important;
                    font-weight: 500 !important;
                    transition: all 0.2s ease !important;
                }
                [data-testid="stSidebar"] div.stButton > button:hover {
                    background-color: rgba(0, 0, 0, 0.04) !important;
                    color: #111827 !important;
                }
                [data-testid="stSidebar"] div[style*="linear-gradient"] + div.stButton > button {
                    background: linear-gradient(90deg, rgba(79, 172, 254, 0.1), rgba(185, 39, 252, 0.1)) !important;
                    border-left: 3px solid #00f2fe !important;
                    color: #111827 !important;
                    font-weight: 700 !important;
                }
                
                /* Progress indicators */
                .custom-progress-bar {
                    background-color: rgba(0, 0, 0, 0.06) !important;
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
                /* Inject dark mode base overlay */
                .stApp {
                    background: radial-gradient(circle at 50% 50%, #0a0721, #030206) !important;
                }
                
                /* Scoped text and card colors for dark theme */
                .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
                .resume-analyzer-header p,
                .glass-card, .glass-card h3, .glass-card h4, .glass-card p, .glass-card b {
                    color: #f1f1f7 !important;
                }
                
                .stMarkdown p, .stMarkdown li, .stMarkdown div {
                    color: #f1f1f7 !important;
                }
                
                /* Dark Mode Sidebar Settings */
                [data-testid="stSidebar"] {
                    background-color: #0b0720 !important;
                    border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
                }
                [data-testid="stSidebar"] p, [data-testid="stSidebar"] caption {
                    color: #9ca3af !important;
                }
                
                /* Circular metrics overrides */
                .circle-chart-text {
                    color: #f1f1f7 !important;
                }
                .circle-chart-bg {
                    stroke: rgba(255, 255, 255, 0.1) !important;
                }
                .skill-badge-neutral {
                    background: rgba(255, 255, 255, 0.05) !important;
                    color: #a1a1aa !important;
                }
                
                /* Sidebar Buttons in Dark Mode */
                [data-testid="stSidebar"] div.stButton > button {
                    background-color: transparent !important;
                    border: none !important;
                    color: #a1a1aa !important;
                    text-align: left !important;
                    padding: 10px 15px !important;
                    width: 100% !important;
                    font-weight: 500 !important;
                    transition: all 0.2s ease !important;
                }
                [data-testid="stSidebar"] div.stButton > button:hover {
                    background-color: rgba(255, 255, 255, 0.05) !important;
                    color: #ffffff !important;
                }
                [data-testid="stSidebar"] div[style*="linear-gradient"] + div.stButton > button {
                    background: linear-gradient(90deg, rgba(79, 172, 254, 0.15), rgba(185, 39, 252, 0.15)) !important;
                    border-left: 3px solid #00f2fe !important;
                    color: #ffffff !important;
                    font-weight: 700 !important;
                }
                
                /* Progress indicators */
                .custom-progress-bar {
                    background-color: rgba(255, 255, 255, 0.08) !important;
                }
            </style>
        """, unsafe_allow_html=True)

def glass_card_start(title="", subtitle=""):
    """Returns the opening HTML wrapper for a premium glassmorphic card with proper dynamic text contrast support."""
    card_html = f'<div class="glass-card">'
    if title:
        card_html += f'<h3 style="margin-top: 0; margin-bottom: 5px; font-weight: 600; font-size: 1.25rem; color: inherit;">{title}</h3>'
    if subtitle:
        card_html += f'<p style="margin-top: 0; margin-bottom: 20px; font-size: 0.85rem; opacity: 0.7; color: inherit;">{subtitle}</p>'
    return card_html

def glass_card_end():
    """Returns the closing HTML tags for the card."""
    return '</div>'

def render_circular_metric(score, label, color1="#00f2fe", color2="#4facfe"):
    """Renders a beautiful circular progress metric using raw HTML / SVG styling with high theme contrast."""
    # Circumference for radius=50 is 2*pi*50 = 314
    dash_array = 314
    dash_offset = int(dash_array - (score / 100.0) * dash_array)
    
    chart_html = f"""
    <div class="glass-card" style="text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 220px;">
        <h4 style="margin-top: 0; margin-bottom: 12px; font-weight: 500; font-size: 0.95rem; opacity: 0.9; color: inherit;">{label}</h4>
        <div class="circle-chart-container">
            <svg class="circle-chart-svg" viewBox="0 0 120 120">
                <circle class="circle-chart-bg" cx="60" cy="60" r="50" />
                <defs>
                    <linearGradient id="grad-{label.replace(' ', '')}" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="{color1}" />
                        <stop offset="100%" stop-color="{color2}" />
                    </linearGradient>
                </defs>
                <circle class="circle-chart-progress" cx="60" cy="60" r="50" 
                        stroke="url(#grad-{label.replace(' ', '')})" 
                        stroke-dasharray="{dash_array}" 
                        stroke-dashoffset="{dash_offset}" />
            </svg>
            <div class="circle-chart-text">{score}%</div>
        </div>
    </div>
    """
    st.markdown(chart_html, unsafe_allow_html=True)

def render_progress_row(label, percentage, color="#00f2fe"):
    """Renders a custom horizontal progress bar with percentage."""
    row_html = f"""
    <div style="margin-bottom: 15px;">
        <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 4px; color: inherit;">
            <span style="font-weight: 500; color: inherit;">{label}</span>
            <span style="font-family: monospace; font-weight: 600; color: inherit;">{percentage}%</span>
        </div>
        <div class="custom-progress-bar">
            <div class="custom-progress-fill" style="width: {percentage}%; background: {color} !important;"></div>
        </div>
    </div>
    """
    st.markdown(row_html, unsafe_allow_html=True)
