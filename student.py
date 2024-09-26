# *********************************************************
# Program: student.py
# Course: SP1123 MINI IT PROJECT
# Class: TL11-13
# Year: 2023/2024 Trimester 3
# Name: NUR FARAH AMYLIA BINTI JAMIL
# ID: 1231101910
# Email: 1231101910@student.mmu.edu.my
# Phone: 0184656557
# *********************************************************

import streamlit as st
from supabase import Client

# Dashboard function
def student_dashboard(supabase: Client):
    st.subheader("Student Dashboard")

    # Fetch subjects from Supabase
    subjects = supabase.table('subjects').select('*').execute()

    if subjects.data:
        # Create list of subject names for the dropdown
        subject_list = [subject['name'] for subject in subjects.data]
        selected_subject = st.selectbox("Select Subject", subject_list)

        if selected_subject:
            # Get the selected subject ID
            subject_id = next(subject['id'] for subject in subjects.data if subject['name'] == selected_subject)
            
            # Fetch related questions from Supabase
            questions = supabase.table('questions').select('*').eq('subject_id', subject_id).execute()

            if questions.data:
                score = 0

                # Display questions and options
                for question in questions.data:
                    st.write(question['question_text'])
                    options = [question['option_a'], question['option_b'], question['option_c'], question['option_d']]
                    selected_option = st.radio("Choose", options, key=question['id'])  # Use unique key for each question

                    # Check if the selected option is correct
                    if selected_option == question[f"option_{question['correct_option'].lower()}"]:
                        score += 1

                # Submit button to calculate score
                if st.button("Submit Quiz"):
                    supabase.table('results').insert({
                        'student_id': st.session_state.get('auth', {}).get('id', 0),  # Dummy student ID for now
                        'subject_id': subject_id,
                        'score': score
                    }).execute()
                    st.success(f"Your score is {score}/{len(questions.data)}")
            else:
                st.warning("No questions found for the selected subject.")
    else:
        st.warning("No subjects available.")
