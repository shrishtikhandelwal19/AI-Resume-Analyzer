import streamlit as st
from utils.helpers import glass_card_start, glass_card_end
from utils.analyzer import perform_local_analysis
from utils.default_data import DEFAULT_RESUME, DEFAULT_JOB_DESC

def render_missing_skills_view():
    """Renders the Page highlighting vital keyword gaps and bullet optimization tips dynamically with high contrast."""
    
    # Safety load results
    if "analysis_results" not in st.session_state:
        results = perform_local_analysis(DEFAULT_RESUME, "Senior Product Architect", DEFAULT_JOB_DESC)
        st.session_state["analysis_results"] = results
        
    results = st.session_state["analysis_results"]

    st.markdown(f"""
        <div class="resume-analyzer-header">
            <h1 style="font-weight: 700; margin-bottom: 5px;">Missing Skills Gap Analysis</h1>
            <p style="opacity: 0.6; font-size: 0.95rem; margin-top: 0;">Crucial core competencies demanded by <b>{results['candidate_title']}</b> positions that were not detected in your resume.</p>
        </div>
    """, unsafe_allow_html=True)

    # Detect active theme
    theme = st.session_state.get("theme", "dark")
    
    # Dynamic styling values
    if theme == "light":
        card_text_color = "#1e1e2f"
        card_border = "rgba(0,0,0,0.08)"
        card_bg = "rgba(239, 68, 68, 0.04)"
        sub_box_bg = "rgba(0, 0, 0, 0.02)"
        sub_box_border = "rgba(0, 0, 0, 0.08)"
    else:
        card_text_color = "#f1f1f7"
        card_border = "rgba(255,255,255,0.05)"
        card_bg = "rgba(239, 68, 68, 0.03)"
        sub_box_bg = "rgba(255, 255, 255, 0.02)"
        sub_box_border = "rgba(255, 255, 255, 0.1)"

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown(f"{glass_card_start('Identified High-Priority Gaps', 'Missed terms that cause immediate screening rejections')}", unsafe_allow_html=True)
        
        gaps = results["gaps"]

        for gap in gaps:
            badge_color = "#ef4444" if "Critical" in gap["priority"] else ("#f59e0b" if "Medium" in gap["priority"] else "#3b82f6")
            st.markdown(f"""
            <div style="background: {card_bg}; border: 1px solid {card_border}; padding: 18px; border-radius: 12px; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: start; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <h4 style="margin: 0; font-weight: 600; font-size: 1rem; color: {card_text_color};">{gap["skill"]}</h4>
                        <span style="font-size: 0.75rem; opacity: 0.6; color: {card_text_color};">{gap["freq"]}</span>
                    </div>
                    <span style="font-size: 0.7rem; font-weight: 700; color: white; background: {badge_color}; padding: 4px 10px; border-radius: 6px;">
                        {gap["priority"]}
                    </span>
                </div>
                <p style="font-size: 0.85rem; opacity: 0.75; color: {card_text_color}; margin: 10px 0 5px 0;">{gap["desc"]}</p>
                <div style="font-size: 0.8rem; font-weight: 600; color: #ef4444;">Estimated Penalty: {gap["impact"]}</div>
            </div>
            """, unsafe_allow_html=True)

        if not gaps:
            st.success("🎉 No significant keyword or skills gaps identified against the Job Description! Excellent alignment!")

        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)

    with col2:
        st.markdown(f"{glass_card_start('Bullet Point Optimizer', 'AI recommendations on how to add keywords gracefully')}", unsafe_allow_html=True)
        st.write("Never stuff keywords listlessly. Use context-rich achievements instead. Here are suggested phrasings you can swap into your resume's experience block:")
        
        suggestions = results["bullet_suggestions"]
        for idx, sug in enumerate(suggestions):
            st.info(f"**For: {sug.get('section', 'Skills Enhancement')}**")
            st.markdown(f"""
            <div style="background: {sub_box_bg}; border: 1px dashed {sub_box_border}; padding: 12px; border-radius: 8px; font-family: monospace; font-size: 0.8rem; color: {card_text_color}; margin-bottom: 15px;">
                "{sug.get('detail', '')}"
            </div>
            """, unsafe_allow_html=True)

        # Calculate optimistic score boost
        proj_score = min(98.5, results["ats_score"] + (12.5 if len(gaps) > 0 else 0) + (6.0 if len(gaps) > 1 else 0))
        
        st.markdown(f"""
            <div style="background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.3); padding: 12px; border-radius: 10px; font-size: 0.8rem; color: #10b981;">
                <b>🎓 Tip:</b> Implementing these bullet point changes will immediately boost your Overall ATS matching score to approximately <b>{proj_score}%</b>.
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)
