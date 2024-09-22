
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
