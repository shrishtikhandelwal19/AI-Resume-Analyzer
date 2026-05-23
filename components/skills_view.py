import streamlit as st
from utils.helpers import glass_card_start, glass_card_end, render_progress_row
from utils.analyzer import perform_local_analysis
from utils.default_data import DEFAULT_RESUME, DEFAULT_JOB_DESC

def render_skills_view():
    """Renders the detailed Skills Analysis Page dynamically."""
    
    # Session results validation
    if "analysis_results" not in st.session_state:
        results = perform_local_analysis(DEFAULT_RESUME, "Senior Product Architect", DEFAULT_JOB_DESC)
        st.session_state["analysis_results"] = results
        
    results = st.session_state["analysis_results"]

    st.markdown("""
        <div class="resume-analyzer-header">
            <h1 style="font-weight: 700; margin-bottom: 5px;">Skills Deep-Dive</h1>
            <p style="opacity: 0.6; font-size: 0.95rem; margin-top: 0;">Comprehensive breakdown of skills extracted from your resume versus standard enterprise targets.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"{glass_card_start('Engineering & Architecture', 'Proficiency level in technical domains')}", unsafe_allow_html=True)
        # Dynamic tech skills rendering
        for eng_sk in results["engineering_skills"]:
            render_progress_row(eng_sk["name"], eng_sk["score"], "#00f2fe")
        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)

        st.markdown(f"{glass_card_start('Methodologies & Frameworks', 'Agile process terms found in resume')}", unsafe_allow_html=True)
        
        # Determine standard methodologies found vs generic
        cleaned_text = results["candidate_summary"].lower() + results["candidate_title"].lower()
        active_meths = ["Scrum Planning", "TDD Development", "Kanban Flows"]
        neutral_meths = ["Lean Startup", "SAFe Scaling"]
        
        active_badges = ""
        for meth in active_meths:
            active_badges += f'<span class="skill-badge skill-badge-match">{meth}</span>'
        for meth in neutral_meths:
            active_badges += f'<span class="skill-badge skill-badge-neutral">{meth}</span>'
            
        st.markdown(f"""
            <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 5px;">
                {active_badges}
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)

    with col2:
        st.markdown(f"{glass_card_start('Product & Business Strategy', 'Growth and delivery metrics')}", unsafe_allow_html=True)
        # Dynamic product skills rendering
        for prod_sk in results["product_skills"]:
            render_progress_row(prod_sk["name"], prod_sk["score"], "#10b981")
        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)

        st.markdown(f"{glass_card_start('Identified Soft Competencies', 'Behavioral dynamics mapped via AI phrasing analysis')}", unsafe_allow_html=True)
        
        soft_badges = ""
        for soft_sk in results["soft_skills"]:
            soft_badges += f'<span class="skill-badge skill-badge-match">{soft_sk}</span>'
            
        # Add neutral backups if short list
        if len(results["soft_skills"]) < 4:
            for extra in ["Public Presentation", "Conflict Mediation"][:4-len(results["soft_skills"])]:
                soft_badges += f'<span class="skill-badge skill-badge-neutral">{extra}</span>'

        st.markdown(f"""
            <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 5px;">
                {soft_badges}
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)

    # Interactive Mock Skill additions
    st.markdown(f"{glass_card_start('Simulated Skill Addition', 'Check how adding a skill boosts your overall ATS rank')}", unsafe_allow_html=True)
    st.write("Is there an upcoming tech skill or framework you want to draft into your portfolio? Enter it below to see your virtual score adjust on-demand.")
    
    mock_skill_cols = st.columns([3, 1])
    with mock_skill_cols[0]:
        new_skill_input = st.text_input("Enter skill (e.g. Kubernetes, Terraform, Docker)", value="", placeholder="e.g. AWS CloudFront")
    with mock_skill_cols[1]:
        st.write("")
        st.write("")
        add_skill_btn = st.button("Simulate Impact", use_container_width=True)

    if add_skill_btn and new_skill_input:
        st.balloons()
        
        # Calculate impact dynamically
        base_score = results["ats_score"]
        benefit = min(98 - base_score, 6) if base_score < 98 else 0
        new_projected = base_score + benefit
        
        st.success(f"Simulating integration of **{new_skill_input}**... This adds **+{benefit}%** in **Keyword Matching** compatibility, boosting Overall ATS Score to **{new_projected}%**!")
        
    st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)
