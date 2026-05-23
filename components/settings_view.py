import streamlit as st
from utils.helpers import glass_card_start, glass_card_end

def render_settings_view():
    """Renders the User Settings & Profile configurations page."""
    st.markdown("""
        <div class="resume-analyzer-header">
            <h1 style="font-weight: 700; margin-bottom: 5px;">Settings & Career Profile</h1>
            <p style="opacity: 0.6; font-size: 0.95rem; margin-top: 0;">Configure your primary target job, user settings, and resume parsing criteria.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"{glass_card_start('Personal Information', 'Core profile data used in scoring headers')}", unsafe_allow_html=True)
        # Pull values dynamically from session results if available
        results = st.session_state.get("analysis_results")
        default_name = st.session_state.get("user_full_name", results["candidate_name"] if results else "Shrisht Khandelwal")
        default_email = st.session_state.get("user_email", "shrishtikhandelwal19@gmail.com")
        
        prof_name = st.text_input("Full Name", value=default_name)
        prof_email = st.text_input("Primary Contact Email", value=default_email)
        prof_phone = st.text_input("Phone Number", value="+1 (555) 019-2834")
        prof_location = st.text_input("Location / City", value="Bengaluru, Karnataka, India")
        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)

        st.markdown(f"{glass_card_start('AI Parsing Model Selection', 'Configure processing models')}", unsafe_allow_html=True)
        model_choice = st.selectbox(
            "Select LLM Base Model",
            ["Gemini Pro (Default - Speed Optimized)", "Gemini Flash (Ultra low latency)", "Gemini Ultra (High reasoning strength)"],
            index=0
        )
        temp_select = st.slider("Strict Parsing temperature", 0.0, 1.0, 0.2, step=0.1, help="Lower value parses exact matches; higher parses semantic variations")
        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)

    with col2:
        st.markdown(f"{glass_card_start('Target Job Requirements', 'Tune analyzer scoring algorithms')}", unsafe_allow_html=True)
        default_title = st.session_state.get("job_title", results["candidate_title"] if results else "Senior Product Architect")
        default_industry = results["primary_industry"] if results else "Tech / SaaS Product Management & Architecture"
        
        target_role = st.text_input("Primary Target Role", value=default_title)
        
        industry_options = ["Tech / SaaS Product Management & Architecture", "SaaS / Technical Products", "Finance & Fintech", "Healthcare & Biotech", "Consulting / Strategy", "Traditional Engineering"]
        industry_index = industry_options.index(default_industry) if default_industry in industry_options else 0
        
        selected_industry = st.selectbox(
            "Primary Industry Sector",
            industry_options,
            index=industry_index
        )
        min_ats_target = st.slider("Target Minimum ATS Pass score", 60, 100, 80, help="Highlight profiles falling below this target limit")
        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)

        st.markdown(f"{glass_card_start('🔑 Account Security & Password', 'Change your authentication password securely')}", unsafe_allow_html=True)
        current_pwd = st.text_input("Current Password", type="password", key="settings_curr_pwd", placeholder="••••••••")
        new_pwd = st.text_input("New Password", type="password", key="settings_new_pwd", placeholder="••••••••")
        confirm_pwd = st.text_input("Confirm New Password", type="password", key="settings_conf_pwd", placeholder="••••••••")
        
        if st.button("🔄 Update Password", key="update_password_btn", use_container_width=True):
            if not current_pwd or not new_pwd or not confirm_pwd:
                st.error("Please fill in all password fields!")
            elif new_pwd != confirm_pwd:
                st.error("New passwords do not match!")
            elif len(new_pwd) < 6:
                st.error("New password must be at least 6 characters long!")
            else:
                from auth.auth_manager import change_user_password
                success, msg = change_user_password(st.session_state["user_id"], current_pwd, new_pwd)
                if success:
                    st.success(msg)
                    st.toast("Credentials updated!")
                else:
                    st.error(msg)
        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)

    # Global Save Button
    st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
    if st.button("💾 Save Profile Configurations", type="primary", use_container_width=True):
        st.session_state["user_full_name"] = prof_name
        st.session_state["user_email"] = prof_email
        st.session_state["job_title"] = target_role
        
        if st.session_state.get("logged_in"):
            from auth.auth_manager import update_profile
            update_profile(
                user_id=st.session_state["user_id"],
                email=prof_email,
                full_name=prof_name,
                target_role=target_role,
                industry=selected_industry
            )
            
        if "analysis_results" in st.session_state:
            st.session_state["analysis_results"]["candidate_name"] = prof_name
            st.session_state["analysis_results"]["candidate_title"] = target_role
            st.session_state["analysis_results"]["primary_industry"] = selected_industry
        
        st.success(f"Profile configurations persisted successfully! Matching benchmarks calibrated for: {target_role}.")
        st.toast("Settings updated!")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
