# *********************************************************
# Program: app.py
# Course: PSP0101 PROBLEM SOLVING AND PROGRAM DESIGN
# Class: TL11-13
# Year: 2023/2024 Trimester 3
# Name: AMIRAH NAILOFAR BINTI MUHAMAD HAFIDZ
# ID: 1231102231
# Email: 1231102231@student.mmu.edu.my
# Phone: 011-1001-8080
# *********************************************************

# import streamlit library
import streamlit as st

# import supabase library
from supabase import create_client, Client

# import login_user and signup_user functions from auth.py
from auth import login_user, signup_user
# from teacher import teacher_dashboard
# from student import student_dashboard

# Load Supabase credentials from secrets.toml
supabase_url = st.secrets["supabase"]["url"]
supabase_key = st.secrets["supabase"]["key"]

# Initialize Supabase client
supabase: Client = create_client(supabase_url, supabase_key)

# Main function to handle routing
def main():
    st.title("MCQ Quiz App")

    # Initialize auth in session state if it does not exist yet
    if 'auth' not in st.session_state:
        # set auth to None
        st.session_state['auth'] = None



    # Sidebar menu with dropdown list
    st.sidebar.title("Navigation Option 1")

    menu = ["Login", "Sign Up", "Teacher Dashboard", "Student Dashboard"]
    # selectbox to choose the menu
    choice = st.sidebar.selectbox("Menu", menu)



    # Sidebar menu with links
    st.sidebar.title("Navigation Option 2")
    
    if st.session_state['auth'] is None:
        if st.sidebar.button("Login", key="login_button"):
            login_user(supabase)
        if st.sidebar.button("Sign Up", key="signup_button"):
            signup_user(supabase)
    else:
        if st.session_state['auth']['role'] == 'teacher':
            if st.sidebar.button("Teacher Dashboard", key="teacher_dashboard_button"):
                teacher_dashboard(supabase)
        elif st.session_state['auth']['role'] == 'student':
            if st.sidebar.button("Student Dashboard", key="student_dashboard_button"):
                student_dashboard(supabase)

        if st.sidebar.button("Logout", key="logout_button"):
            st.session_state['auth'] = None
            st.sidebar.success("Successfully logged out.")



if __name__ == '__main__':
    main()