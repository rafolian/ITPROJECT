import streamlit as st
from supabase import Client
# 
def teacher_dashboard(supabase: Client):
    st.subheader("Teacher Dashboard")

    # Step 1: Create New Subject
    if 'subject_created' not in st.session_state:
        st.session_state['subject_created'] = False

    subject_name = st.text_input("Enter Subject Name")
    
    if st.button("Create New Subject"):
        if subject_name:
            supabase.from_('subjects').insert({
                'name': subject_name,
                'teacher_id': st.session_state['auth']['id']
            }).execute()
            st.session_state['subject_created'] = True
            st.success(f"Subject '{subject_name}' created.")
        else:
            st.error("Please enter a subject name.")