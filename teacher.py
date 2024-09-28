# *********************************************************
# Program: teacher.py
# Course: SP1123 MINI IT PROJECT
# Class: TL11-13
# Year: 2023/2024 Trimester 3
# Name: XX NAMA??
# ID: XX
# Email: XX
# Phone: XX
# *********************************************************

import streamlit as st
from supabase import Client

# Function to display teacher dashboard with options to create new subject and add questions
def teacher_dashboard(supabase: Client):
    st.subheader("Teacher Dashboard")

    # Step 1: Create New Subject 
    if 'subject_created' not in st.session_state:
        st.session_state['subject_created'] = False

    subject_name = st.text_input("Enter Subject Name")

    if st.button("Create New Subject"):
        if subject_name:

            # Insert new subject into the database with the teacher's ID 
            supabase.from_('subjects').insert({
                'name': subject_name,
                'teacher_id': st.session_state['auth']['id']
            }).execute()

            # Set subject_created to True to proceed to the next step
            st.session_state['subject_created'] = True
            st.success(f"Subject '{subject_name}' created.")
        else:
            st.error("Please enter a subject name.")

    # Step 2: Add 5 MCQ questions (if subject is created)
    if st.session_state['subject_created']:
        st.subheader(f"Add 5 Questions to {subject_name}")
        
        # Collect 5 questions
        questions = []
        for i in range(5):

            # Display question input fields 
            st.write(f"### Question {i+1}")
            question_text = st.text_area(f"Enter question {i+1}")
            option_a = st.text_input(f"Option A for Question {i+1}")
            option_b = st.text_input(f"Option B for Question {i+1}")
            option_c = st.text_input(f"Option C for Question {i+1}")
            option_d = st.text_input(f"Option D for Question {i+1}")
            correct_option = st.selectbox(f"Correct Option for Question {i+1}", ['A', 'B', 'C', 'D'])

            # Append question details to the questions list
            questions.append({
                'question_text': question_text,
                'option_a': option_a,
                'option_b': option_b,
                'option_c': option_c,
                'option_d': option_d,
                'correct_option': correct_option
            })

        # Save questions to the database 
        if st.button("Save Questions"):

            # Get the subject ID for the selected subject 
            subject_id = supabase.from_('subjects').select('id').eq('name', subject_name).single().execute()

            # Insert questions into the database with the subject ID
            if subject_id.data:
                for q in questions:
                    supabase.from_('questions').insert({
                        'subject_id': subject_id.data['id'],
                        'question_text': q['question_text'],
                        'option_a': q['option_a'],
                        'option_b': q['option_b'],
                        'option_c': q['option_c'],
                        'option_d': q['option_d'],
                        'correct_option': q['correct_option']
                    }).execute()
                    
                # Reset subject_created to False and display success message 
                st.success(f"All 5 questions added to {subject_name}.")
                st.session_state['subject_created'] = False  # Reset for the next session
            else:
                st.error("Subject ID not found in the database.")

    # Step 3: View Student Results for a Subject
    st.subheader("View Student Results")
    
    # Fetch all subjects created by the teacher
    subjects = supabase.from_('subjects').select('id, name').eq('teacher_id', st.session_state['auth']['id']).execute()
    
    if subjects.data:
        subject_names = {subject['name']: subject['id'] for subject in subjects.data}
        selected_subject_name = st.selectbox("Select Subject to View Results", list(subject_names.keys()))
        selected_subject_id = subject_names[selected_subject_name]
        
        # Fetch the results of students for the selected subject
        results = supabase.from_('results').select('student_id, score, created_at').eq('subject_id', selected_subject_id).execute()

        if results.data:
            for result in results.data:
                # Fetch student email or name from the users table
                student_info = supabase.from_('users').select('email').eq('id', result['student_id']).single().execute()

                # Display student result information
                if student_info.data:
                    st.write(f"*Student*: {student_info.data['email']}")
                    st.write(f"*Score*: {result['score']}")
                    st.write(f"*Date Taken*: {result['created_at'].split('T')[0]}")
                    st.write("---")
        else:
            st.write("No students have taken this quiz yet.")
    else:
        st.write("No subjects available to view results.")