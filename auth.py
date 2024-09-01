# *********************************************************
# Program: auth.py
# Course: PSP0101 PROBLEM SOLVING AND PROGRAM DESIGN
# Class: TL11-13
# Year: 2023/2024 Trimester 3
# Name: AMIRAH NAILOFAR BINTI MUHAMAD HAFIDZ
# ID: 1231102231
# Email: 1231102231@student.mmu.edu.my
# Phone: 011-1001-8080
# *********************************************************

import streamlit as st
from supabase import Client

# Functions: login_user(supabase: Client): Prompts the user to enter their email and password to log in. If the login is successful, the user is stored in the session state.
def login_user(supabase: Client):
    
    # render subheader with Login prompt
    st.subheader("Login")

    # text input
    email = st.text_input("Email")

    # masked text input
    password = st.text_input("Password", type="password")


# Functions: signup_user(supabase: Client): Prompts the user to enter their email, password, and role to create a new account. If the account creation is successful, the user is stored in the session state.
def signup_user(supabase: Client):

    # render subheader with Create New Account prompt
    st.subheader("Create New Account")

    # text input
    email = st.text_input("Email")

    # masked text input
    password = st.text_input("Password", type="password")

    role = st.selectbox("Role", ["teacher", "student"])