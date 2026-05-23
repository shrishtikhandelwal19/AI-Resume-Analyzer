import streamlit as st

def render_sidebar():
    """Renders the custom styled navigation sidebar with responsive light/dark themes."""
    # Ensure theme is initialized
    if "theme" not in st.session_state:
        st.session_state["theme"] = "dark"
        
    theme = st.session_state["theme"]

    # Configure dynamic theme variables for hardcoded HTML blocks
    if theme == "light":
        header_border = "rgba(0, 0, 0, 0.08)"
        analyzer_color = "#374151"
        version_color = "#6b7280"
        footer_bg = "rgba(0, 0, 0, 0.03)"
        footer_border = "rgba(0, 0, 0, 0.08)"
        footer_name_color = "#111827"
        footer_text_color = "#4b5563"
    else:
        header_border = "rgba(255, 255, 255, 0.06)"
        analyzer_color = "#f1f1f7"
        version_color = "rgba(255, 255, 255, 0.45)"
        footer_bg = "rgba(255, 255, 255, 0.03)"
        footer_border = "rgba(255, 255, 255, 0.05)"
        footer_name_color = "#f3f4f6"
        footer_text_color = "#9ca3af"

    with st.sidebar:
        # Title branding with blue-purple gradient
        st.markdown(f"""
            <div style="padding: 10px 0 20px 0; text-align: center; border-bottom: 1px solid {header_border}; margin-bottom: 20px;">
                <h2 style="font-weight: 700; font-size: 1.4rem; letter-spacing: -0.5px; margin: 0; color: {analyzer_color};">
                    <span style="background: linear-gradient(135deg, #00f2fe, #b927fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        Resume Analyzer
                    </span>
                    <span style="font-weight: 300; font-size: 1.1rem; opacity: 0.85; margin-left: 5px;">Analyzer</span>
                </h2>
                <span style="font-size: 0.70rem; opacity: 0.65; color: {version_color}; font-family: monospace;">Enterprise Edition v1.2</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Initialization of navigation if not in state
        if "active_page" not in st.session_state:
            st.session_state["active_page"] = "Dashboard"

        col_theme1, col_theme2 = st.columns([3, 1])
        with col_theme1:
            st.caption(f"Current Theme: {theme.capitalize()}")
        with col_theme2:
            theme_btn = "☀️" if theme == "dark" else "🌙"
            if st.button(theme_btn, key="theme_toggle_btn", help="Toggle Light/Dark Contrast"):
                new_theme = "light" if theme == "dark" else "dark"
                st.session_state["theme"] = new_theme
                if st.session_state.get("logged_in"):
                    from auth.auth_manager import update_theme_preference
                    update_theme_preference(st.session_state["user_id"], new_theme)
                st.rerun()

        st.markdown("<p style='font-size:0.75rem; font-weight:600; opacity:0.5; margin: 15px 0 5px 0; text-transform: uppercase;'>Main Menu</p>", unsafe_allow_html=True)

        pages = [
            {"name": "Dashboard", "icon": ""},
            {"name": "Upload Resume", "icon": ""},
            {"name": "ATS Analysis", "icon": ""},
            {"name": "Skills Analysis", "icon": ""},
            {"name": "Missing Skills", "icon": ""},
            {"name": "Reports", "icon": ""},
            {"name": "Settings & Profile", "icon": "👤"}
        ]
        
        for page in pages:
            is_active = st.session_state["active_page"] == page["name"]
            btn_label = f"{page['icon']}  {page['name']}"
            
            # Active styling wrapper for custom sibling selector match
            if is_active:
                st.markdown("""
                <div style="background: linear-gradient(90deg, rgba(79, 172, 254, 0.15), rgba(185, 39, 252, 0.15)); border-left: 3px solid #00f2fe; border-radius: 4px; padding: 1px 0px;">
                </div>
                """, unsafe_allow_html=True)
            
            if st.button(btn_label, key=f"nav_btn_{page['name']}", use_container_width=True):
                st.session_state["active_page"] = page["name"]
                st.rerun()
                
        # Candidate Profile summary in Sidebar Footer (Dynamical contrasting container)
        user_fullname = st.session_state.get("user_full_name", "Shrisht Khandelwal")
        user_title = st.session_state.get("job_title", "Product Manager & Developer")
        
        name_parts = user_fullname.split()
        initials = "".join([part[0].upper() for part in name_parts[:2]]) if name_parts else "SK"

        st.markdown(f"""
            <div style="margin-top: 40px; padding: 12px; border-radius: 12px; background: {footer_bg}; border: 1px solid {footer_border}; text-align: center; margin-bottom: 10px;">
                <div style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #00f2fe, #b927fc); margin: 0 auto 10px auto; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white;">
                    {initials}
                </div>
                <div style="font-weight: 600; font-size: 0.85rem; margin: 0; color: {footer_name_color};">{user_fullname}</div>
                <div style="font-size: 0.7rem; color: {footer_text_color}; margin-bottom: 5px;">{user_title}</div>
                <span style="background: rgba(16, 185, 129, 0.15); color: #10b981; padding: 2px 8px; border-radius: 10px; font-size: 0.6rem; font-weight: bold;">PREMIUM ACTIVE</span>
            </div>
        """, unsafe_allow_html=True)
        
        from auth.auth_manager import logout_active_user
        if st.button("🔓 End Active Session", key="logout_sidebar_btn", use_container_width=True):
            logout_active_user()
            st.success("Logging out...")
            st.rerun()

