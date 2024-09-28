# *********************************************************
# Program: auth.py
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

import streamlit as st

# UI function to display the change password form
def change_password_ui(supabase: Client):
    st.subheader("Change Your Password")

    # Ask the user to input their current password and new password
    current_password = st.text_input("Current Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_new_password = st.text_input("Confirm New Password", type="password")

    # Change password button
    if st.button("Change Password"):
        if new_password == confirm_new_password:
            result = change_password(supabase, st.session_state['auth']['id'], current_password, new_password)
            if result == "success":
                st.success("Your password has been changed successfully.")
            elif result == "incorrect_password":
                st.error("Current password is incorrect.")
            else:
                st.error("An error occurred. Please try again.")
        else:
            st.error("New passwords do not match.")


# Logic function to validate the current password and update with the new password
def change_password(supabase: Client, user_id, current_password, new_password):
    try:
        # Fetch the current password from the database
        user = supabase.from_('users').select('password_hash').eq('id', user_id).single().execute()

        if user.data:
            # Verify the current password matches the stored one
            if current_password == user.data['password_hash']:  # Direct comparison, no hashing as requested
                # Update the password in the database
                supabase.from_('users').update({'password_hash': new_password}).eq('id', user_id).execute()
                return "success"
            else:
                return "incorrect_password"
        else:
            return "user_not_found"
    except Exception as e:
        print(f"Error changing password: {e}")
        return "error"

# Function to log in the user
def login_user(supabase: Client):
    st.subheader("Login")

    # Input fields for email and password
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # Login button
    if st.button("Login"):
        # Check for empty fields
        if not email or not password:
            st.error("Both email and password are required.")
        else:
            try:
                # Fetch user information from the database
                user = supabase.from_('users').select('*').eq('email', email).single().execute()

                # Check if the user exists in the database
                if user.data:
                    # Check if the password matches
                    if user.data['password_hash'] == password:  # Direct comparison as per the current setup
                        st.session_state['auth'] = {'id': user.data['id'], 'role': user.data['role'], 'email': user.data['email']}
                        st.success(f"Welcome, {user.data['email']}!")
                    else:
                        st.error("Incorrect password.")
                else:
                    st.error("User not found. Please check your email or sign up.")

            except Exception as e:
                st.error(f"An error occurred during login: {e}")

# Function to sign up a new user
def signup_user(supabase: Client):
    st.subheader("Create New Account")

    # Get email, password, and role from user
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["teacher", "student"])

    # Insert the new user into the database
    if st.button("Sign Up"):
        user = supabase.from_('users').insert({
            'email': email,
            'password_hash': password,
            'role': role
        }).execute()

        # Check if the user was successfully created and store the user in the session state
        if user.data:
            st.success("Account created for {}".format(email))
            st.session_state['auth'] = user.data
        else:
            st.error("Sign Up failed")
