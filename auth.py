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
from supabase import Client

# Function to log out the user
def login_user(supabase: Client):
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = supabase.from_('users').select('*').eq('email', email).single().execute()
        if user.data:
            if user.data['password_hash'] == password:
                st.session_state['auth'] = user.data
                st.success("Logged In as {}".format(email))
            else:
                st.error("Incorrect Password")
        else:
            st.error("User not found")

# Function to sign up a new user
def signup_user(supabase: Client):
    st.subheader("Create New Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["teacher", "student"])

    if st.button("Sign Up"):
        user = supabase.from_('users').insert({
            'email': email,
            'password_hash': password,
            'role': role
        }).execute()

        if user.data:
            st.success("Account created for {}".format(email))
            st.session_state['auth'] = user.data
        else:
            st.error("Sign Up failed")
