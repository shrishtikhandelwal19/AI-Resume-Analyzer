import streamlit as st
import time
from utils.helpers import glass_card_start, glass_card_end
from utils.analyzer import extract_resume_text, analyze_resume

def render_upload_view():
    """Renders the resume upload and analysis configuration view."""
    st.markdown("""
        <div class="resume-analyzer-header">
            <h1 style="font-weight: 700; margin-bottom: 5px;">Upload Resume</h1>
            <p style="opacity: 0.6; font-size: 0.95rem; margin-top: 0;">Upload your PDF or DOCX resume, paste your target job description, and run our proprietary ATS Analyzer engine.</p>
        </div>
    """, unsafe_allow_html=True)

    col_up, col_desc = st.columns([1, 1])

    with col_up:
        st.markdown(f"{glass_card_start('1. Drop Your Resume')}", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload your latest resume file", 
            type=["pdf", "docx"], 
            help="Select or drag and drop your file here."
        )
        if uploaded_file is not None:
            st.success(f"Successfully loaded: {uploaded_file.name}")
        else:
            st.markdown("""
                <div style="border: 2px dashed rgba(79, 172, 254, 0.3); border-radius: 10px; background: rgba(255,255,255,0.02); padding: 40px 20px; text-align: center; margin-top: 10px;">
                    <span style="font-size: 2.5rem;">📄</span>
                    <h5 style="margin: 15px 0 5px 0; font-weight: 600;">Drag and Drop CV</h5>
                    <p style="font-size: 0.75rem; opacity: 0.5; margin: 0;">PDF or DOCX format only • Verified by secure sandbox</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)

        st.markdown(f"{glass_card_start('3. Job Role & Title')}", unsafe_allow_html=True)
        # Pull previously configured title if present
        saved_title = st.session_state.get("job_title", "Senior Product Architect")
        job_title = st.text_input("Target Job Title", value=saved_title, placeholder="e.g. Lead Devops Architect")
        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)

    with col_desc:
        st.markdown(f"{glass_card_start('2. Job Description')}", unsafe_allow_html=True)
        saved_jd = st.session_state.get("job_desc", "")
        job_desc_text = st.text_area(
            "Paste full Job Description content here",
            value=saved_jd,
            height=305,
            placeholder="Paste text contents from LinkedIn, Indeed, or internal portals here..."
        )
        st.markdown(f"{glass_card_end()}", unsafe_allow_html=True)

    # Trigger action button
    st.markdown("<div style='text-align: center; margin-top: 30px;'>", unsafe_allow_html=True)
    
    # Styled analyze button
    col_empty1, col_center, col_empty2 = st.columns([1, 2, 1])
    with col_center:
        analyze_clicked = st.button(" Analyze Resume -> ", use_container_width=True, type="primary")

    if analyze_clicked:
        if uploaded_file is None:
            st.warning("Please upload a resume file first before initiating AI Analysis!")
        else:
            # High-fidelity loading sequence simulation with REAL text processing
            status_container = st.empty()
            progress_bar = st.progress(0)
            
            try:
                # Step 1
                status_container.markdown("""
                <div style="background: rgba(185, 39, 252, 0.1); border: 1px solid rgba(185, 39, 252, 0.3); border-radius: 8px; padding: 15px; margin-top: 20px; text-align: center;">
                    <span style="font-weight: 500; font-size: 0.95rem;">🔍 Extracting resume text & scanning header sections...</span>
                </div>
                """, unsafe_allow_html=True)
                progress_bar.progress(20)
                time.sleep(0.5)
                
                resume_text = extract_resume_text(uploaded_file)
                st.session_state["resume_text"] = resume_text
                st.session_state["resume_name"] = uploaded_file.name
                st.session_state["job_title"] = job_title
                st.session_state["job_desc"] = job_desc_text
                
                # Step 2
                status_container.markdown("""
                <div style="background: rgba(185, 39, 252, 0.1); border: 1px solid rgba(185, 39, 252, 0.3); border-radius: 8px; padding: 15px; margin-top: 20px; text-align: center;">
                    <span style="font-weight: 500; font-size: 0.95rem;">🧠 Running NLP vectorizations & TF-IDF matrix generation...</span>
                </div>
                """, unsafe_allow_html=True)
                progress_bar.progress(50)
                time.sleep(0.5)
                
                # Step 3
                status_container.markdown("""
                <div style="background: rgba(185, 39, 252, 0.1); border: 1px solid rgba(185, 39, 252, 0.3); border-radius: 8px; padding: 15px; margin-top: 20px; text-align: center;">
                    <span style="font-weight: 500; font-size: 0.95rem;">🎯 Calculating Cosine Similarity match index & keyword gaps...</span>
                </div>
                """, unsafe_allow_html=True)
                progress_bar.progress(80)
                
                # Run actual evaluation
                analysis_results = analyze_resume(resume_text, job_title, job_desc_text)
                st.session_state["analysis_results"] = analysis_results
                
                # Persist to local database if user is authenticated
                if st.session_state.get("logged_in"):
                    user_id = st.session_state["user_id"]
                    from database.db_manager import add_analysis_record_db
                    add_analysis_record_db(
                        user_id=user_id,
                        filename=uploaded_file.name,
                        resume_text=resume_text,
                        job_title=job_title,
                        job_desc=job_desc_text,
                        results_dict=analysis_results
                    )
                    # Wipe session state cache to force database-backed historical reload
                    if "eval_history" in st.session_state:
                        del st.session_state["eval_history"]
                
                # If there's an evaluation history list, prepend this result
                if "eval_history" not in st.session_state:
                    st.session_state["eval_history"] = []
                
                # Avoid duplicates
                st.session_state["eval_history"].insert(0, {
                    "file": uploaded_file.name,
                    "role": job_title,
                    "date": time.strftime("%b %d, %Y"),
                    "score": analysis_results["ats_score"],
                    "status": "Optimized" if analysis_results["ats_score"] >= 80 else ("Action Required" if analysis_results["ats_score"] >= 70 else "High Missing Gaps")
                })
                
                # Step 4
                status_container.markdown("""
                <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 15px; margin-top: 20px; text-align: center;">
                    <span style="font-weight: 600; font-size: 0.95rem; color: #10b981;">✨ Done! Dashboard analytics compiled successfully.</span>
                </div>
                """, unsafe_allow_html=True)
                progress_bar.progress(100)
                time.sleep(0.5)
                
                st.session_state["active_page"] = "ATS Analysis"
                st.rerun()
                
            except Exception as ex:
                st.error(f"An error occurred during resume analysis: {str(ex)}")

    st.markdown("</div>", unsafe_allow_html=True)

