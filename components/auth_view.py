import streamlit as st
import time
from auth.auth_manager import login_user, signup_user
from utils.helpers import glass_card_start, glass_card_end

def render_auth_view():
    """Renders a beautiful glassmorphic Login/Signup page in the center of the viewport."""
    theme = st.session_state.get("theme", "dark")
    
    # Text contrasting
    text_color = "#111827" if theme == "light" else "#f9fafb"
    muted_color = "#4b5563" if theme == "light" else "#a1a1aa"
    
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 30px; margin-top: 50px;">
            <h1 style="font-weight: 800; font-size: 2.8rem; margin: 0; background: linear-gradient(135deg, #00f2fe, #b927fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Resume Analyzer
            </h1>
            <p style="color: {muted_color}; font-size: 1.1rem; margin-top: 5px;">Enterprise-grade Resume Audit and ATS Optimizer Engine</p>
        </div>
    """, unsafe_allow_html=True)

    # Center-aligned container logic
    col_left, col_mid, col_right = st.columns([1, 2, 1])

    with col_mid:
        auth_mode = st.session_state.get("auth_mode", "login")
        
        if auth_mode == "login":
            st.markdown(f"{glass_card_start('🔑 Direct Account Login', 'Access your CV analysis history and reports')}", unsafe_allow_html=True)
            
            # Form UI
            username = st.text_input("Username", key="login_username_input", placeholder="e.g. shrisht_k").strip()
            password = st.text_input("Password", type="password", key="login_password_input", placeholder="••••••••")
            
            st.markdown("<p style='margin-bottom: 20px;'></p>", unsafe_allow_html=True)
            
            btn_login = st.button("-> Log In to Engine", type="primary", use_container_width=True)
            
            if btn_login:
                if not username or not password:
                    st.error("Please fill in both username and password fields!")
                else:
                    with st.spinner("Verifying secure credentials..."):
                        time.sleep(0.6)
                        success, message = login_user(username, password)
                        if success:
                            st.success("Successfully authenticated!")
                            st.toast("Welcome back!")
                            time.sleep(0.4)
                            st.rerun()
                        else:
                            st.error(message)

            st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)
            
            # Switch view link
            st.markdown(f"""
                <div style="text-align: center; margin-top: 15px;">
                    <span style="color: {muted_color}; font-size: 0.9rem;">New to the platform? </span>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Create a New Account", use_container_width=True, key="switch_to_register_btn"):
                st.session_state["auth_mode"] = "signup"
                st.rerun()
                
        else:
            st.markdown(f"{glass_card_start('👤 Register New Account', 'Get started with professional ATS validation metrics')}", unsafe_allow_html=True)
            
            username = st.text_input("Choose Username", key="reg_username_input", placeholder="e.g. shrisht_k").strip()
            password = st.text_input("Choose Password", type="password", key="reg_password_input", placeholder="At least 6 characters")
            email = st.text_input("Email Address", key="reg_email_input", placeholder="e.g. user@example.com").strip()
            full_name = st.text_input("Full Name", key="reg_fullname_input", placeholder="Shrisht Khandelwal").strip()
            
            # Additional career meta details
            target_role = st.text_input("Target Job Title", key="reg_title_input", placeholder="e.g. Senior Product Architect").strip()
            industry = st.selectbox(
                "Primary Industry Sector",
                ["Tech / SaaS Product Management & Architecture", "SaaS / Technical Products", "Finance & Fintech", "Healthcare & Biotech", "Consulting / Strategy", "Traditional Engineering"],
                key="reg_industry_input"
            )
            
            st.markdown("<p style='margin-bottom: 20px;'></p>", unsafe_allow_html=True)
            
            btn_signup = st.button("✨ Complete Account Registration", type="primary", use_container_width=True)
            
            if btn_signup:
                if (
    username.strip() == "" or
    password.strip() == "" or
    email.strip() == "" or
    full_name.strip() == ""
):
    
                    st.error("Please complete all required register fields (Username, Password, Email, Full Name)!")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters long!")
                else:
                    with st.spinner("Writing credentials securely to database..."):
                        time.sleep(0.7)
                        success, message = signup_user(
                            username=username,
                            password=password,
                            email=email,
                            full_name=full_name,
                            target_role=target_role or "Senior Product Architect",
                            industry=industry
                        )
                        if success:
                            st.success(f"Account for {username} registered successfully! Proceed to login.")
                            st.balloons()
                            time.sleep(1.0)
                            st.session_state["auth_mode"] = "login"
                            st.rerun()
                        else:
                            st.error(message)

            st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)
            
            # Switch view link
            st.markdown(f"""
                <div style="text-align: center; margin-top: 15px;">
                    <span style="color: {muted_color}; font-size: 0.9rem;">Already have an account? </span>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Back to Login", use_container_width=True, key="switch_to_login_btn"):
                st.session_state["auth_mode"] = "login"
                st.rerun()
