import streamlit as st
import pandas as pd
import hashlib

# Create a sample student data DataFrame
students_df = pd.DataFrame({
    "Student ID": [1, 2, 3],
    "Name": ["John Doe", "Jane Doe", "Bob Smith"],
    "Email": ["johndoe@example.com", "janedoe@example.com", "bobsmith@example.com"],
    "Password": ["password1", "password2", "password3"]
})

# Hash passwords for storage
hashed_passwords = [hashlib.sha256(password.encode()).hexdigest() for password in students_df["Password"]]
students_df["Password"] = hashed_passwords

# Login and Register
st.title("Student Dashboard")
st.sidebar.title("Navigation")

with st.form("login_form"):
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.form_submit_button("Login")

with st.form("register_form"):
    st.header("Register")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    new_email = st.text_input("Email")
    register_button = st.form_submit_button("Register")

# Check login credentials
if login_button:
    username = username.strip()
    password = hashlib.sha256(password.encode()).hexdigest()
    if username in students_df["Email"].values and password in students_df["Password"].values:
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
    else:
        st.error("Invalid username or password")

# Check register credentials
if register_button:
    new_username = new_username.strip()
    new_password = hashlib.sha256(new_password.encode()).hexdigest()
    new_email = new_email.strip()
    if new_username not in students_df["Email"].values:
        students_df = students_df.append({"Student ID": len(students_df) + 1, "Name": "", "Email": new_email, "Password": new_password}, ignore_index=True)
        st.success("Account created successfully")
    else:
        st.error("Username already exists")

# Display student data if logged in
if st.session_state.get("logged_in"):
    st.sidebar.title("Student Data")
    student_data = students_df[students_df["Email"] == st.session_state["username"]]
    st.table(student_data)

    # Navigation menu
    navigation_options = ["Dashboard", "Assignments", "Quizzes", "Profile"]
    selected_option = st.sidebar.selectbox("Navigation", navigation_options)

    if selected_option == "Dashboard":
        # Display dashboard content
        st.header("Dashboard")
        st.write("Welcome to your dashboard!")
    elif selected_option == "Assignments":
        # Display assignments content
        st.header("Assignments")
        st.write("Assignments will be displayed here")
    elif selected_option == "Quizzes":
        # Display quizzes content
        st.header("Quizzes")
        st.write("Quizzes will be displayed here")
    elif selected_option == "Profile":
        # Display profile content
        st.header("Profile")
        st.write("Profile information will be displayed here")