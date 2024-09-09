# *********************************************************
# Program: app.py
# Course: SP1123 MINI IT PROJECT
# Class: TL11-13
# Year: 2023/2024 Trimester 3
# Name: AMIRAH NAILOFAR BINTI MUHAMAD HAFIDZ
# ID: 1231102231
# Email: 1231102231@student.mmu.edu.my
# Phone: 011-1001-8080
# *********************************************************

# Import required libraries
import streamlit as st
from supabase import create_client, Client
from auth import login_user, signup_user
# from teacher import teacher_dashboard
# from student import student_dashboard

# Load Supabase credentials from secrets.toml
supabase_url = st.secrets["supabase"]["url"]
supabase_key = st.secrets["supabase"]["key"]

# Initialize Supabase client
supabase: Client = create_client(supabase_url, supabase_key)

# Function to log out the user
def logout():
    st.session_state['auth'] = None
    st.sidebar.success("You have been logged out.")

# Main function to handle routing
def main():
    st.title("MCQ Quiz App")

    # Sidebar menu
    menu = ["Login", "Sign Up", "Teacher Dashboard", "Student Dashboard"]
    
    # Display logout button if user is logged in
    if st.session_state.get('auth') is not None:
        st.sidebar.button("Logout", on_click=logout)
    
    choice = st.sidebar.selectbox("Menu", menu)

    if 'auth' not in st.session_state or st.session_state['auth'] is None:
        if choice == "Login":
            login_user(supabase)
        elif choice == "Sign Up":
            signup_user(supabase)
    else:
        role = st.session_state['auth']['role']
        if choice == "Teacher Dashboard" and role == 'teacher':
            teacher_dashboard(supabase)
        elif choice == "Student Dashboard" and role == 'student':
            student_dashboard(supabase)
        else:
            st.warning("You do not have access to this section.")

if __name__ == '__main__':
    main()