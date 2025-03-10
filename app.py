# app.py

import os
import streamlit as st
import time
from agents.orchestrator import orchestrate_documentation
from agents.agent_feedback import evaluate_feedback
from docs.doc_consolidator import consolidate_documentation

def run_app():
    st.title("Docu-Tiger")
    st.write("Enter the project folder path and get going!")
    
    # Initialize session state variable to hold the documentation sections.
    if "doc_sections" not in st.session_state:
        st.session_state["doc_sections"] = None

    project_folder = st.text_input("Project Folder Path", key="project_folder")

    if project_folder:
        if not os.path.isdir(project_folder):
            st.error("Provided folder path is not valid.")
        else:
            if st.button("Generate Documentation"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                # Run orchestrator and store the result in session state
                st.session_state["doc_sections"] = orchestrate_documentation(
                    project_folder,
                    progress_callback=lambda p, msg: (progress_bar.progress(p), status_text.text(msg))
                )
                st.success("Documentation generated successfully!")
                time.sleep(0.5)

    # If documentation has been generated, display sections and collect feedback.
    if st.session_state.get("doc_sections") is not None:
        doc_sections = st.session_state["doc_sections"]
        st.header("Review and Provide Feedback")
        
        # Wrap feedback inputs in a form so Ctrl+Enter triggers submission.
        with st.form("feedback_form"):
            st.subheader("High-Level Description")
            st.markdown(doc_sections["high_level_desc"])
            hl_feedback = st.text_area("High-Level Description Feedback", height=100, key="hl_feedback")
            
            st.subheader("Modules Section")
            st.markdown(doc_sections["modules_section"])
            mod_feedback = st.text_area("Modules Section Feedback", height=100, key="mod_feedback")
            
            st.subheader("Requirements Section")
            st.markdown(doc_sections["requirements_section"])
            req_feedback = st.text_area("Requirements Section Feedback", height=100, key="req_feedback")
            
            submit_feedback = st.form_submit_button("Submit Feedback")
        
        if submit_feedback:
            updated = False
            # Process feedback for High-Level Description
            if hl_feedback and hl_feedback.strip().lower() not in ["", "all good"]:
                new_hl = evaluate_feedback("high_level", doc_sections["high_level_desc"], hl_feedback)
                doc_sections["high_level_desc"] = new_hl
                updated = True
            # Process feedback for Modules Section
            if mod_feedback and mod_feedback.strip().lower() not in ["", "all good"]:
                new_mod = evaluate_feedback("modules", doc_sections["modules_section"], mod_feedback)
                doc_sections["modules_section"] = new_mod
                updated = True
            # Process feedback for Requirements Section
            if req_feedback and req_feedback.strip().lower() not in ["", "all good"]:
                new_req = evaluate_feedback("requirements", doc_sections["requirements_section"], req_feedback)
                doc_sections["requirements_section"] = new_req
                updated = True
            if updated:
                # Re-consolidate final documentation with updated sections.
                final_doc = consolidate_documentation(
                    doc_sections["high_level_desc"],
                    doc_sections["folder_structure"],
                    doc_sections["requirements_section"],
                    doc_sections["modules_section"],
                    doc_sections["license_info"]
                )
                doc_sections["final_documentation"] = final_doc
                st.session_state["doc_sections"] = doc_sections
                st.success("Feedback processed. Updated documentation:")
                st.markdown(final_doc)
                st.download_button(
                    label="Download Updated Documentation",
                    data=final_doc,
                    file_name="PROJECT_DOCUMENTATION_UPDATED.md",
                    mime="text/markdown"
                )
            else:
                st.info("No actionable feedback provided. Documentation remains unchanged.")
        
        st.header("Final Documentation")
        st.markdown(doc_sections["final_documentation"])
        st.download_button(
            label="Download Documentation",
            data=doc_sections["final_documentation"],
            file_name="PROJECT_DOCUMENTATION.md",
            mime="text/markdown"
        )

if __name__ == '__main__':
    run_app()
