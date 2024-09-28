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

# Import login_user and signup_user functions from auth.py
from auth import login_user, signup_user, change_password_ui

# Import teacher_dashboard function from teacher.py
from teacher import teacher_dashboard

# Import student function from student.py
from student import student_dashboard

# Load Supabase credentials from secrets.toml
supabase_url = st.secrets["supabase"]["url"]
supabase_key = st.secrets["supabase"]["key"]

# Initialize Supabase client
supabase: Client = create_client(supabase_url, supabase_key)

# Function to log out the user
def logout():
    st.session_state['auth'] = None
    st.sidebar.success("You have been logged out.")

# Function to display FAQ content
def faq():
    st.subheader("Frequently Asked Questions")
    st.write("""
    **Q1: What is this Application?**
             
    A1: This is a simple MCQ Quiz Application that allows teachers to create quizzes and students to take them online.

    **Q2: How can this be used in education?**
             
    A2: Teachers can create quizzes for students to study and test their knowledge. Students can take the quizzes to practice and improve their understanding.

    **Q3: How do I view my results?**
             
    A3: After logging in, click on the 'Result' option in the sidebar to view your results for the quizzes you have taken.
             
    **Q4: How do I register?**
             
    A4: Click on the 'Sign Up' option in the sidebar to create a new account. You can choose to sign up as a teacher or student.

    **Q5: How do I log in?**
             
    A5: Click on the 'Login' option in the sidebar to log in to your account. Enter your email and password to access your account.
    """)

# Function to add header
def add_header():
    header = """
    <style>
    .header {
        position: fixed;
        top: 40px;
        left: 0;
        width: 100%;
        background-color: #98DED9;
        color: white;
        text-align: center;
        padding: 10px;
        z-index: 1000;
    }
    body {
        padding-top: 300px; /* Adjust this value based on the height of your header */
    }
    </style>
    <div class="header">
        <h1>Welcome to the QuizLab Application</h1>
    </div>
    """
    st.markdown(header, unsafe_allow_html=True)

# Function to add footer
def add_footer():
    footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: #555;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        <p>QuizLab &copy; 2024 | MULTIMEDIA UNIVERSITY MINI IT PROJECT</p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)

# Main function to handle routing and display the app
def main():

    # Add header
    add_header()

    st.title("")
    
    # Initialize session state for authentication
    if 'auth' not in st.session_state:
        st.session_state['auth'] = None

    # Sidebar menu with all options
    menu = ["Login", "Sign Up", "FAQ", "Teacher Dashboard", "Student Dashboard", "Change Password"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Display logout button and user info if user is logged in
    if st.session_state['auth'] is not None:
        st.sidebar.write(f"Logged in as: {st.session_state['auth']['email']}")
        st.sidebar.button("Logout", on_click=logout)

    # Routing based on user selection
    if choice == "Login":
        if st.session_state['auth'] is None:
            login_user(supabase)
        else:
            st.success(f"You are already logged in as {st.session_state['auth']['email']}.")
    elif choice == "Sign Up":
        if st.session_state['auth'] is None:
            signup_user(supabase)
        else:
            st.success(f"You are already logged in as {st.session_state['auth']['email']}.")
    elif choice == "FAQ":
        faq()
    elif choice == "Teacher Dashboard":
        if st.session_state['auth'] is not None and st.session_state['auth']['role'] == 'teacher':
            teacher_dashboard(supabase)
        else:
            st.warning("You must be logged in as a teacher to access this section.")
    elif choice == "Student Dashboard":
        if st.session_state['auth'] is not None and st.session_state['auth']['role'] == 'student':
            student_dashboard(supabase)
        else:
            st.warning("You must be logged in as a student to access this section.")
    elif choice == "Change Password":
        if st.session_state['auth'] is not None:
            change_password_ui(supabase)
        else:
            st.warning("You must be logged in to change your password.")
            
    # Add footer
    add_footer()

# Run the main function when the script is executed
if __name__ == '__main__':
    main()