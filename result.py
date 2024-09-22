<<<<<<< HEAD
# *********************************************************
# Program: student.py
# Course: SP1123 MINI IT PROJECT
# Class: TL11-13
# Year: 2023/2024 Trimester 3
# Name: NUR
# ID: XX
# Email: XX
# Phone: XX
# *********************************************************

import streamlit as st
import pandas as pd
from supabase import Client

# Dashboard function
def result_management_dashboard(supabase: Client):
    st.subheader("Result Management Dashboard")

    # Fetch students from Supabase
    students = supabase.table('students').select('*').execute()

    if students.data:
        # Create list of student IDs for the dropdown
        student_list = [student['Student ID'] for student in students.data]
        selected_student = st.selectbox("Select Student ID", student_list)

        if selected_student:
            # Get the selected student's score
            student_score = supabase.table('students').select('Score').eq('Student ID', selected_student).execute().data[0]['Score']

            # Display the student's score
            st.write(f"Score for Student ID {selected_student}: {student_score}")

            # Create a form to update the student's score
            st.write("### Update Student Score")
            form = st.form("update_score")
            new_score = form.number_input("New Score")
            submit = form.form_submit_button("Update Score")

            # Update the student's score when the form is submitted
            if submit:
                supabase.table('students').update({'Score': new_score}).eq('Student ID', selected_student).execute()
                st.success("Score updated successfully!")

            # Create a button to download the student's results as a CSV file
            st.write("### Download Results")
            download_button = st.button("Download Results")
            if download_button:
                data = supabase.table('students').select('*').execute().data
                df = pd.DataFrame(data)
                df.to_csv("results.csv", index=False)
                st.success("Results downloaded successfully!")
    else:
        st.warning("No students available.")
=======
# *********************************************************
# Program: student.py
# Course: SP1123 MINI IT PROJECT
# Class: TL11-13
# Year: 2023/2024 Trimester 3
# Name: XX
# ID: XX
# Email: XX
# Phone: XX
# *********************************************************

import streamlit as st
import pandas as pd
from supabase import create_client, Client

# Initialize Supabase client
url = "https://dkbiurasbinrawvrtdtz.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRrYml1cmFzYmlucmF3dnJ0ZHR6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjQ1ODMxMTYsImV4cCI6MjA0MDE1OTExNn0.Bjg8I4PUMNHBfZumqQy_vOB5r1jZMRqBgXfchjrRQVg"

supabase = create_client(url, key)

def student_dashboard(supabase: Client):
    st.subheader("Student Dashboard")

    subjects = supabase.from_('subjects').select('*').execute()

    subject_list = [subject['name'] for subject in subjects.data]
    selected_subject = st.selectbox("Select Subject", subject_list)

    if selected_subject:
        subject_id = next(subject['id'] for subject in subjects.data if subject['name'] == selected_subject)
        questions = supabase.from_('questions').select('*').eq('subject_id', subject_id).execute()

        score = 0

        for question in questions.data:
            st.write(question['question_text'])
            options = [question['option_a'], question['option_b'], question['option_c'], question['option_d']]
            selected_option = st.radio("Choose", options)

            if selected_option == question[f"option_{question['correct_option'].lower()}"]:
                score += 1

        if st.button("Submit Quiz"):
            supabase.from_('results').insert({
                'student_id': st.session_state['auth']['id'],
                'subject_id': subject_id,
                'score': score
            }).execute()
            st.success(f"Your score is {score}/{len(questions.data)}")
>>>>>>> b6a26196a944a4eccff569058760f4dcd8cb69ae
