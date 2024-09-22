
# *********************************************************
# Program: result.py
# Course: SP1123 MINI IT PROJECT
# Class: TL11-13
# Year: 2023/2024 Trimester 3
# Name: NUR FARAH AMYLIA BINTI JAMIL
# ID: 1231101910
# Email: 1231101910@student.mmu.edu.my
# Phone: 0184656557
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
