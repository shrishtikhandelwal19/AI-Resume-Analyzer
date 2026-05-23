import streamlit as st
from utils.helpers import glass_card_start, glass_card_end, render_progress_row
from utils.analyzer import perform_local_analysis, generate_pdf_report_bytes
from utils.default_data import DEFAULT_RESUME, DEFAULT_JOB_DESC

def render_reports_view():
    """Renders the simplified beginner-friendly historical reports and summary completely dynamically."""
    
    # Preload verification
    if "analysis_results" not in st.session_state:
        results = perform_local_analysis(DEFAULT_RESUME, "Senior Product Architect", DEFAULT_JOB_DESC)
        st.session_state["analysis_results"] = results
        
    results = st.session_state["analysis_results"]

    st.markdown("""
        <div class="resume-analyzer-header">
            <h1 style="font-weight: 700; margin-bottom: 5px;">Performance Reports</h1>
            <p style="opacity: 0.6; font-size: 0.95rem; margin-top: 0;">Review your comprehensive resume audit report and download insights.</p>
        </div>
    """, unsafe_allow_html=True)

    # 2x2 Responsive Layout for the 4 core summaries
    col1, col2 = st.columns(2)

    with col1:
        # 1. Candidate Summary
        st.markdown(f"{glass_card_start('👤 Candidate Summary', 'Primary professional details')}", unsafe_allow_html=True)
        st.markdown(f"""
            <div style="font-size: 0.9rem; line-height: 1.8;">
                <b>Full Name:</b> {results['candidate_name']}<br>
                <b>Target Title:</b> {results['candidate_title']}<br>
                <b>Experience Level:</b> {results['experience_level']}<br>
                <b>Primary Industry:</b> {results['primary_industry']}<br>
                <b>Overall Rank:</b> <span style="background: linear-gradient(90deg, #00f2fe, #b927fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;">{results['overall_rank']}</span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)

        # 2. ATS Summary
        st.markdown(f"{glass_card_start('🎯 ATS Summary', 'How tracking systems evaluate your resume')}", unsafe_allow_html=True)
        render_progress_row("Overall ATS Match", results["ats_score"], "#00f2fe")
        render_progress_row("Keyword Density Match", results["keyword_density_match"], "#b927fc")
        render_progress_row("Formatting & Layout Quality", results["formatting_layout_score"], "#10b981")
        
        # Check standard passes
        all_passed = [c["title"] for c in results["checklist_checks"] if c["passed"]]
        all_passed_str = ", ".join(all_passed[:3]) + "..." if all_passed else "None"
        st.markdown(f"""
            <p style="font-size: 0.8rem; opacity: 0.8; margin-top: 10px; line-height: 1.4;">
                <b>Section Checklist:</b> Completed validation passes on {all_passed_str}
            </p>
        """, unsafe_allow_html=True)
        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)

    with col2:
        # 3. Skills Summary
        st.markdown(f"{glass_card_start('⚙️ Skills Summary', 'Proficiency in detected core competencies')}", unsafe_allow_html=True)
        bd = results["score_breakdown"]
        render_progress_row("Product & Business Strategy", bd.get("product_mgmt", 80), "#10b981")
        render_progress_row("System Design & API Architecture", bd.get("system_design", 85), "#4facfe")
        render_progress_row("Fullstack Web Development", bd.get("software_eng", 75), "#8a2be2")
        
        # Dynamically create skill badges from parsed list
        strength_badges = ""
        for str_sk in results["top_strengths_matches"][:3]:
            strength_badges += f'<span class="skill-badge skill-badge-match block" style="margin: 0 4px 0 0; font-size: 11px;">{str_sk}</span>'
            
        st.markdown(f"""
            <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px;">
                {strength_badges}
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)

        # 4. Missing Skills
        st.markdown(f"{glass_card_start('⚠️ Missing Skills Gaps', 'Identified critical keyword deficiencies')}", unsafe_allow_html=True)
        
        # We can dynamically set the color of text in missing skills depending on the light vs dark mode
        theme = st.session_state.get("theme", "dark")
        missing_text_color = "#111827" if theme == "light" else "#f9fafb"
        border_color_missing = "rgba(0, 0, 0, 0.08)" if theme == "light" else "rgba(255, 255, 255, 0.08)"
        
        gaps_html = ""
        gaps = results["gaps"]
        
        for idx, gap in enumerate(gaps[:3]):
            badge_color = "#ef4444" if "Critical" in gap["priority"] else ("#f59e0b" if "Medium" in gap["priority"] else "#3b82f6")
            bg_color = "rgba(239, 68, 68, 0.15)" if "Critical" in gap["priority"] else ("rgba(245, 158, 11, 0.15)" if "Medium" in gap["priority"] else "rgba(59, 130, 246, 0.15)")
            priority_label = "CRITICAL" if "Critical" in gap["priority"] else ("MEDIUM" if "Medium" in gap["priority"] else "MINOR")
            
            border_style = f"border-bottom: 1px solid {border_color_missing}; padding-bottom: 6px;" if idx < len(gaps[:3])-1 else ""
            
            gaps_html += (
              f'<div style="display:flex; justify-content:space-between; '
              f'align-items:center; {border_style} margin-bottom:6px;">'
              f'<span style="font-size:0.85rem; font-weight:500; color:inherit;">'
              f'{gap["skill"]}</span>'
              f'<span style="background:{bg_color}; color:{badge_color}; '
              f'font-size:0.7rem; font-weight:700; padding:2px 8px; '
              f'border-radius:4px; white-space:nowrap;">'
              f'{priority_label}</span>'
              f'</div>'
)
            
        if not gaps:
            gaps_html = "<div style='text-align: center; opacity: 0.6; font-size: 0.9rem;'>No skills gaps detected! Good job.</div>"

        st.markdown(f"""
            <div style="display: flex; flex-direction: column; gap: 8px; color: {missing_text_color};">
                {gaps_html}
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)

    # 5. Full-width Action Banner containing purely the Download active button
    st.markdown(f"{glass_card_start('📥 Export & Download', 'Export your resume audit results instantly')}", unsafe_allow_html=True)
    
    col_dl_left, col_dl_mid, col_dl_right = st.columns([1, 2, 1])
    with col_dl_mid:
        try:
            # Generate real PDF report bytes using reportlab compiler
            pdf_bytes = generate_pdf_report_bytes(results)
            
            st.download_button(
                label="📥 Download Complete Report PDF",
                data=pdf_bytes,
                file_name=f"CV_AI_Audit_Report_{results['candidate_name'].replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="download_report_pdf"
            )
        except Exception as e:
            st.error(f"Error compiling PDF report: {str(e)}")

    st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)
