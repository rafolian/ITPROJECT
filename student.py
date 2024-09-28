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

def student_dashboard(supabase: Client):
    st.subheader("Student Dashboard")

    # Fetch all subjects from the database
    subjects = supabase.from_('subjects').select('id, name').execute()

    if subjects.data:
        subject_names = {subject['name']: subject['id'] for subject in subjects.data}
        selected_subject_name = st.selectbox("Select Subject to Take Quiz", list(subject_names.keys()))
        selected_subject_id = subject_names[selected_subject_name]

        # Fetch all questions for the selected subject
        questions = supabase.from_('questions').select('*').eq('subject_id', selected_subject_id).execute()

        if questions.data:
            st.write(f"Taking Quiz for {selected_subject_name}")
            student_answers = []
            correct_answers = []
            question_ids = []

            # Display each question and answer options
            for question in questions.data:
                st.write(f"### {question['question_text']}")
                student_answer = st.radio(f"Choose your answer for Question {questions.data.index(question) + 1}", 
                                          [question['option_a'], question['option_b'], question['option_c'], question['option_d']])
                student_answers.append(student_answer)
                correct_answers.append(question[f"option_{question['correct_option'].lower()}"])  # Store correct answers
                question_ids.append(question['id'])

            if st.button("Submit Quiz"):
                # Score calculation
                score = 0
                wrong_questions = []

                for i, student_answer in enumerate(student_answers):
                    if student_answer == correct_answers[i]:
                        score += 1
                    else:
                        wrong_questions.append({
                            'question_text': questions.data[i]['question_text'],
                            'student_answer': student_answers[i],
                            'correct_answer': correct_answers[i]
                        })

                # Insert student response and score into the database
                supabase.from_('results').insert({
                    'student_id': st.session_state['auth']['id'],
                    'subject_id': selected_subject_id,
                    'score': score
                }).execute()

                st.success(f"Your score is {score}/{len(questions.data)}")

                # Display feedback on wrong questions
                if wrong_questions:
                    st.error("You answered the following questions incorrectly:")
                    for wrong in wrong_questions:
                        st.write(f"*Question*: {wrong['question_text']}")
                        st.write(f"*Your Answer*: {wrong['student_answer']}")
                        st.write(f"*Correct Answer*: {wrong['correct_answer']}")
                        st.write("---")
                else:
                    st.success("Great job! You answered all questions correctly!")
        else:
            st.write(f"No questions found for {selected_subject_name}.")
    else:
        st.write("No subjects available.")

    # New Section: Show Subjects Student Has Taken
    st.subheader("Subjects You Have Taken")

    # Fetch all the subjects the student has already taken from the 'results' table
    taken_subjects = supabase.from_('results').select('subject_id, score').eq('student_id', st.session_state['auth']['id']).execute()

    if taken_subjects.data:
        for entry in taken_subjects.data:
            # Get subject name for each entry
            subject_info = supabase.from_('subjects').select('name').eq('id', entry['subject_id']).single().execute()
            if subject_info.data:
                # Handle missing 'created_at' field
                date_taken = entry.get('created_at', 'N/A')  # Default to 'N/A' if 'created_at' is not present
                
                # If 'created_at' is present, format it
                if date_taken != 'N/A':
                    date_taken = date_taken.split("T")[0]  # Extract only the date (YYYY-MM-DD)
                
                # Display the subject name, score, and date taken
                st.write(f"*Subject*: {subject_info.data['name']}")
                st.write(f"*Score*: {entry['score']}")
                st.write(f"Date Taken: {date_taken}")
                st.write("---")
    else:
        st.write("You have not taken any subjects yet.")
