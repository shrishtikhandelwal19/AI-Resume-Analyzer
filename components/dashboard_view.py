import streamlit as st
import time
from utils.helpers import glass_card_start, glass_card_end, render_progress_row
from utils.analyzer import perform_local_analysis
from utils.default_data import DEFAULT_RESUME, DEFAULT_JOB_DESC

def render_dashboard_view():
    """Renders the dynamic AI Resume Analyzer Dashboard View."""
    
    # Dynamic SQLite History Initialization
    user_id = st.session_state.get("user_id")
    if user_id:
        from database.db_manager import get_analysis_history_db
        db_history = get_analysis_history_db(user_id)
        if db_history:
            eval_history = []
            for h in db_history:
                score = h["analysis_results"].get("ats_score", 70)
                status = "Optimized" if score >= 80 else ("Action Required" if score >= 70 else "High Missing Gaps")
                eval_history.append({
                    "id": h["id"],
                    "file": h["filename"],
                    "role": h["job_title"],
                    "date": h["uploaded_at"][:16] if h["uploaded_at"] else "May 22, 2026",
                    "score": score,
                    "status": status,
                    "results_dict": h["analysis_results"]
                })
            st.session_state["eval_history"] = eval_history
            
            # Map recent analysis results
            if "analysis_results" not in st.session_state or st.session_state.get("is_default_results", True):
                st.session_state["analysis_results"] = db_history[0]["analysis_results"]
                st.session_state["is_default_results"] = False
        else:
          
          # if "analysis_results" not in st.session_state:
           #     user_full_name = st.session_state.get("user_full_name", "Shrisht Khandelwal")
           #     user_title = st.session_state.get("job_title", "Senior Product Architect")
                
             #   results = perform_local_analysis(DEFAULT_RESUME, user_title, DEFAULT_JOB_DESC)
             #   results["candidate_name"] = user_full_name
              #  results["candidate_title"] = user_title
                
               # st.session_state["analysis_results"] = results
                #st.session_state["is_default_results"] = True 
                
                
            st.session_state["eval_history"] = []
    else:
        # Fallback for offline/standalone execution
        if "analysis_results" not in st.session_state:
            results = perform_local_analysis(DEFAULT_RESUME, "Senior Product Architect", DEFAULT_JOB_DESC)
            st.session_state["analysis_results"] = results
            st.session_state["is_default_results"] = True
            
        if "eval_history" not in st.session_state:
            st.session_state["eval_history"] = [
                {"file": "Resume_PM_Architect_V3.pdf", "role": "Senior Product Architect", "date": "May 22, 2026", "score": st.session_state["analysis_results"]["ats_score"], "status": "Optimized"},
                {"file": "Developer_Resume_Backend_V4.docx", "role": "Fullstack Engineering Lead", "date": "May 20, 2026", "score": 75, "status": "Action Required"},
                {"file": "Product_Manager_Consulting_V2.pdf", "role": "Product Leader", "date": "May 15, 2026", "score": 68, "status": "High Missing Gaps"}
            ]

    results = st.session_state["analysis_results"]

    st.markdown(f"""
        <div class="resume-analyzer-header">
            <h1 style="font-weight: 700; margin-bottom: 5px;">Welcome back, {results['candidate_name'].split()[0]}!</h1>
            <p style="opacity: 0.6; font-size: 0.95rem; margin-top: 0;"> View your candidate overview and core performance stats.</p>
        </div>
    """, unsafe_allow_html=True)

    # 1. Premium Greeting Banner Card
    st.markdown(f"""
    {glass_card_start()}
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 20px;">
            <div>
                <h2 style="margin: 0 0 8px 0; font-weight: 700;">
                    Unlocking Your Career Potential with <span class="gradient-text-blue-purple">AI Intelligence</span>
                </h2>
                <p style="opacity: 0.8; max-width: 650px; font-size: 0.95rem; margin-top: 0; line-height: 1.5;">
                    Your CV has been analyzed against top-tech industry profiles. We discovered key enhancements for your <b>{results['candidate_title']}</b> resume. Explore missing skills and job matches to increase interviews by up to <b>35%</b>.
                </p>
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <span style="background: rgba(0, 242, 254, 0.1); color: #00f2fe; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">System Ready</span>
                    <span style="background: rgba(185, 39, 252, 0.1); color: #b927fc; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">Interview Ready</span>
                </div>
            </div>
            <div>
                <div style="background: linear-gradient(135deg, rgba(0, 242, 254, 0.2), rgba(185, 39, 252, 0.2)); border: 1px solid rgba(0, 242, 254, 0.3); padding: 20px; border-radius: 12px; text-align: center; min-width: 180px;">
                    <span style="opacity: 0.7; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">Overall Rank</span>
                    <h1 style="font-size: 3rem; font-weight: 800; margin: 10px 0 5px 0; font-family: 'JetBrains Mono', monospace; background: linear-gradient(90deg, #00f2fe, #b927fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{results['overall_rank']}</h1>
                    <span style="font-size: 0.8rem; font-weight: 500; color: #10b981;">Top Placed Candidate</span>
                </div>
            </div>
        </div>
    {glass_card_end()}
    """, unsafe_allow_html=True)

    # 2. Statistics Grid
    st.markdown("""<h3 style="font-weight: 600; margin-bottom: 15px; margin-top: 25px;">Core Analytics</h3>""", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        {glass_card_start("", "")}
            <div style="font-size: 0.75rem; text-transform: uppercase; font-weight: 600; opacity: 0.6; margin-bottom: 8px;">ATS Match Score</div>
            <h2 style="margin: 0; font-weight: 700; color: #00f2fe; font-family: 'JetBrains Mono', monospace; font-size: 2rem;">{results['ats_score']}<span style="font-size: 1.1rem; opacity: 0.7;">%</span></h2>
            <div style="font-size: 0.75rem; color: #10b981; margin-top: 5px; font-weight: 500;">↗ Dynamic calculation match</div>
        {glass_card_end()}
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        {glass_card_start("", "")}
            <div style="font-size: 0.75rem; text-transform: uppercase; font-weight: 600; opacity: 0.6; margin-bottom: 8px;">Keyword Alignment</div>
            <h2 style="margin: 0; font-weight: 700; color: #b927fc; font-family: 'JetBrains Mono', monospace; font-size: 2rem;">{results['keyword_density_match']}<span style="font-size: 1.1rem; opacity: 0.7;">%</span></h2>
            <div style="font-size: 0.75rem; color: #a1a1aa; margin-top: 5px; font-weight: 500;">Optimized parsing depth</div>
        {glass_card_end()}
        """, unsafe_allow_html=True)

    with col3:
        num_gaps = len(results['gaps'])
        status_gap = "High Profile Gap" if num_gaps >= 3 else ("Normal" if num_gaps > 0 else "Perfect Match")
        color_gap = "#ef4444" if num_gaps >= 3 else "#f59e0b"
        st.markdown(f"""
        {glass_card_start("", "")}
            <div style="font-size: 0.75rem; text-transform: uppercase; font-weight: 600; opacity: 0.6; margin-bottom: 8px;">Missing Core Skills</div>
            <h2 style="margin: 0; font-weight: 700; color: {color_gap}; font-family: 'JetBrains Mono', monospace; font-size: 2rem;">{num_gaps}</h2>
            <div style="font-size: 0.75rem; color: #f59e0b; margin-top: 5px; font-weight: 500;">⚠ Requires Attention</div>
        {glass_card_end()}
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        {glass_card_start("", "")}
            <div style="font-size: 0.75rem; text-transform: uppercase; font-weight: 600; opacity: 0.6; margin-bottom: 8px;">Interview Probability</div>
            <h2 style="margin: 0; font-weight: 700; color: #10b981; font-family: 'JetBrains Mono', monospace; font-size: 2rem;">{results['interview_probability']}<span style="font-size: 1.1rem; opacity: 0.7;">%</span></h2>
            <div style="font-size: 0.75rem; color: #10b981; margin-top: 5px; font-weight: 500;">Top Placement Chance</div>
        {glass_card_end()}
        """, unsafe_allow_html=True)

    # 3. Two columns: Profile Summary vs Recent Scans
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown(f"{glass_card_start('Skill Mastery Breakdown', 'Candidate metrics across core industries')}", unsafe_allow_html=True)
        bd = results["score_breakdown"]
        render_progress_row("Product Management", bd.get("product_mgmt", 80), "#00f2fe")
        render_progress_row("Software Engineering", bd.get("software_eng", 75), "#4facfe")
        render_progress_row("System Design & Architecture", bd.get("system_design", 85), "#8a2be2")
        render_progress_row("Cloud Technologies (AWS/GCP)", bd.get("cloud_tech", 65), "#b927fc")
        render_progress_row("Data Science & AI/ML", bd.get("ai_ml", 45), "#e935a1")
        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)

    with col_right:
        st.markdown(f"{glass_card_start('Candidate Profile Card', 'Identified career dimensions')}", unsafe_allow_html=True)
        
        st.write(f"**Full Name:** {results['candidate_name']}")
        st.write(f"**Target Title:** {results['candidate_title']}")
        st.write(f"**Experience Level:** {results['experience_level']}")
        st.write(f"**Primary Industry:** {results['primary_industry']}")
        
        st.markdown("<p style='font-size:0.85rem; font-weight:600; margin:15px 0 5px 0; opacity: 0.8;'>Top Strengths Matches:</p>", unsafe_allow_html=True)
        
        badges_html = ""
        for str_match in results["top_strengths_matches"]:
            badges_html += f'<span class="skill-badge skill-badge-match" style="margin: 0">{str_match}</span>'
        
        st.markdown(f"""
            <div style="display: flex; flex-wrap: wrap; gap: 6px;">
            {badges_html}
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)

    # 4. Recent evaluations section
    st.markdown("""<h3 style="font-weight: 600; margin-bottom: 15px; margin-top: 25px;">Recent Evaluations Log</h3>""", unsafe_allow_html=True)
    
    recent_scans = st.session_state["eval_history"]

    if not recent_scans:
        st.info("No resume evaluations scanned yet! Click 'Upload Resume' in the menu to analyze your first file.")
    else:
        for scan in recent_scans:
            color_score = "#10b981" if scan["score"] >= 80 else ("#f59e0b" if scan["score"] >= 70 else "#ef4444")
            st.markdown(f"""
            <div class="glass-card" style="padding: 15px 20px; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 15px; margin-bottom: 12px;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="background: rgba(255,255,255,0.04); font-size: 1.5rem; width: 45px; height: 45px; border-radius: 8px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(255,255,255,0.06);">
                    </div>
                    <div>
                        <h4 style="margin: 0; font-weight: 600; font-size: 0.95rem;">{scan["file"]}</h4>
                        <p style="margin: 2px 0 0 0; font-size: 0.8rem; opacity: 0.6;">Targeting: <b>{scan["role"]}</b> • Scanned on {scan["date"]}</p>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 20px;">
                    <div style="text-align: right;">
                        <div style="font-weight: 700; color: {color_score}; font-size: 1.15rem; font-family: 'JetBrains Mono', monospace;">{scan["score"]}%</div>
                        <span style="font-size: 0.7rem; font-weight: 600; opacity: 0.8;">Score</span>
                    </div>
                    <div style="background: rgba(255,255,255,0.02); padding: 5px 12px; border-radius: 6px; font-size: 0.75rem; border: 1px solid rgba(255,255,255,0.05); font-weight: 500;">
                        {scan["status"]}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
