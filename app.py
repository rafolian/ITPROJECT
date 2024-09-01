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

# Main function to handle routing
def main():
    st.title("MCQ Quiz App")

    if 'auth' not in st.session_state:
        st.session_state['auth'] = None

    # Sidebar menu
    menu = ["Login", "Sign Up", "Teacher Dashboard", "Student Dashboard"]
    choice = st.sidebar.selectbox("Menu", menu)

if __name__ == '__main__':
    main()