import streamlit as st
from utils.helpers import glass_card_start, glass_card_end, render_circular_metric
from utils.analyzer import perform_local_analysis
from utils.default_data import DEFAULT_RESUME, DEFAULT_JOB_DESC

def render_ats_view():
    """Renders the high-fidelity ATS Scorecard and parser checks dynamically."""
    
    # Pre-condition safety check
    if "analysis_results" not in st.session_state:
        results = perform_local_analysis(DEFAULT_RESUME, "Senior Product Architect", DEFAULT_JOB_DESC)
        st.session_state["analysis_results"] = results
        
    results = st.session_state["analysis_results"]

    st.markdown(f"""
        <div class="resume-analyzer-header">
            <h1 style="font-weight: 700; margin-bottom: 5px;">ATS Scoring & Analysis</h1>
            <p style="opacity: 0.6; font-size: 0.95rem; margin-top: 0;">Comprehensive breakdown of how ATS software evaluates your file for <b>{results['candidate_title']}</b> positions.</p>
        </div>
    """, unsafe_allow_html=True)

    # 1. Row of Circular Charts
    col1, col2, col3 = st.columns(3)
    with col1:
        render_circular_metric(results["ats_score"], "Overall ATS Score", "#00f2fe", "#4facfe")
    with col2:
        render_circular_metric(results["keyword_density_match"], "Keyword Density Match", "#b927fc", "#e935a1")
    with col3:
        render_circular_metric(results["formatting_layout_score"], "Formatting & Layout", "#10b981", "#059669")

    # 2. Text layout analysis details
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown(f"{glass_card_start('Detailed Section Checklist', 'Verification of standard resume structure')}", unsafe_allow_html=True)
        
        checks = results["checklist_checks"]

        for check in checks:
            badge = "✅ PASS" if check["passed"] else "⚠️ WARN"
            color_badge = "#10b981" if check["passed"] else "#f59e0b"
            bg_badge_channel = "16, 185, 129" if check["passed"] else "245, 158, 11"
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.05); padding: 10px 0;">
                <div>
                    <span style="font-weight: 600; font-size: 0.9rem;">{check["title"]}</span>
                    <p style="margin: 2px 0 0 0; font-size: 0.75rem; opacity: 0.6;">{check["desc"]}</p>
                </div>
                <span style="font-size: 0.75rem; font-weight: 700; color: {color_badge}; background: rgba({bg_badge_channel}, 0.15); padding: 4px 10px; border-radius: 6px;">
                    {badge}
                </span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)

    with col_right:
        st.markdown(f"{glass_card_start('Keyword Optimization Engine', 'Top matched keywords parsed')}", unsafe_allow_html=True)
        
        keywords = results["top_keywords_parsed"]

        for kw in keywords:
            # Parse numerical density from string format e.g., "4.2% (Perfect)"
            try:
                numeric_density = float(kw["density"].split("%")[0])
            except Exception:
                numeric_density = 2.0
            
            # Map percentage (usually 0 to 5%) to a nice display bar (0 to 100%)
            progress_width = min(100, int(numeric_density * 20))
            
            st.markdown(f"""
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 3px;">
                    <span style="font-weight: 500;">{kw["name"]}</span>
                    <span style="opacity: 0.7; font-family: monospace;">{kw["density"]}</span>
                </div>
                <div class="custom-progress-bar" style="margin: 0; height: 6px;">
                    <div class="custom-progress-fill" style="width: {progress_width}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)
        
        # Action criteria adjustment
        st.markdown(f"{glass_card_start('Analysis Feedback', 'Key optimization takeaway')}", unsafe_allow_html=True)
        st.write(f"Your document has **exceptional alignment** with core industry requirements. However, adding several highlighted skills will optimize density matching score further.")
        
        saved_score = r_score = results["ats_score"]
        optimize_slider = st.slider("Required ATS Optimization level", 50, 100, int(r_score), help="Set a goal to see matching tips.")
        
        additional_skills_qty = max(0, int((optimize_slider - saved_score) / 5))
        if additional_skills_qty > 0:
            st.info(f"Targeting a higher ATS threshold of {optimize_slider}% requires completing at least **{additional_skills_qty}** more skill additions.")
        else:
            st.success(f"Excellent! Your current score of **{saved_score}%** meets or exceeds your targeted threshold of {optimize_slider}%.")
            
        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)
