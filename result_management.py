import streamlit as st
import pandas as pd

# Create a sample dataset for demonstration purposes
data = {
    "Student ID": [1, 2, 3, 4, 5],
    "Name": ["John", "Alice", "Bob", "Eve", "Charlie"],
    "Score": [80, 90, 70, 85, 95]
}
df = pd.DataFrame(data)

# Create a Streamlit app
st.title("Result Management System")
st.write("Welcome to the Result Management System!")

# Display the dataset
st.write("### Student Results")
st.write(df)

# Create a form to input student ID and score
st.write("### Update Student Score")
form = st.form("update_score")
student_id = form.text_input("Student ID")
score = form.number_input("Score")
submit = form.form_submit_button("Update Score")

# Update the dataset when the form is submitted
if submit:
    df.loc[df["Student ID"] == int(student_id), "Score"] = score
    st.write("Score updated successfully!")

# Create a dropdown to select a student and display their score
st.write("### View Student Score")
student_id_dropdown = st.selectbox("Select Student ID", df["Student ID"])
student_score = df.loc[df["Student ID"] == student_id_dropdown, "Score"].values[0]
st.write(f"Score for Student ID {student_id_dropdown}: {student_score}")

# Create a button to download the dataset as a CSV file
st.write("### Download Results")
download_button = st.button("Download Results")
if download_button:
    df.to_csv("results.csv", index=False)
    st.write("Results downloaded successfully!")