import streamlit as st
import os

# 1. Set global Streamlit Page Config MUST occur first
st.set_page_config(
    page_title="Resume Analyzer - Modern Resume Analyzer & ATS Optimizer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils.helpers import load_css, local_css_theme
from components.sidebar import render_sidebar
from components.dashboard_view import render_dashboard_view
from components.upload_view import render_upload_view
from components.ats_view import render_ats_view
from components.skills_view import render_skills_view
from components.missing_skills_view import render_missing_skills_view
from components.reports_view import render_reports_view
from components.settings_view import render_settings_view

def main():
    # 2. Inject raw custom CSS & setup theme parameters
    load_css(os.path.join(os.path.dirname(__file__), "styles", "main.css"))
    local_css_theme()

    # 2.1. Authentication Shield
    if not st.session_state.get("logged_in", False):
        from components.auth_view import render_auth_view
        render_auth_view()
        return

    # 3. Render sidebars & handle menu items state Management
    render_sidebar()
    active_view = st.session_state.get("active_page", "Dashboard")

    # 4. View router
    if active_view == "Dashboard":
        render_dashboard_view()
    elif active_view == "Upload Resume":
        render_upload_view()
    elif active_view == "ATS Analysis":
        render_ats_view()
    elif active_view == "Skills Analysis":
        render_skills_view()
    elif active_view == "Missing Skills":
        render_missing_skills_view()
    elif active_view == "Reports":
        render_reports_view()
    elif active_view == "Settings & Profile":
        render_settings_view()

if __name__ == "__main__":
    main()
