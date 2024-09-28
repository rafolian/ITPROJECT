#TC1L

Architecture:
1. This project is based on python, utilizing streamlit as the main framework. It is also using supabase as the database.

2. The database contains five tables:
- users
- results
- questions
- subjects
- student_responses

3. Table users contains the following field:
- id 
- email
- password_hash
- role 
- created_at

4. Table results contains the following field:
- id 
- student_id
- subject_id
- score
- created_at

5. Table questions contains the following field:
- id
- subject_id
- question_text
- option_a
- option_b
- option_c
- option_d
- correct_option
- created_at

6. Table subjects contains the following field:
- id
- name
- teacher_id
- created_at

7. Table student_responses contains the following field:
- id 
- student_id
- question_id 
- chosen_option
- is_correct 
- answered_at


Development Journal:
1. At week 1, 2 and 3, we completed the overall architecture and selection of technology stacks(python, streamlit, supabase)

2. At week 4, we have created app.py and auth.py as an intial code. Further development is being planned.

3. At week 5, we have created student.py and teacher.py as an intial code. Further development is being planned.

4. At week 6, we continue to integrate the codes and reviewing the features.

5. At week 7, we are making the github repo public and publishing the app to the streamlit community cloud at https://itproject-mmu.streamlit.app.


Instruction to Run:

1. activate python environment with the libraries defined in requirements.txt

2. run the code "streamlit run app.py"