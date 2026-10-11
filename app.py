import pandas as pd
import streamlit as st
from database import add_student, get_students
from services import calculate_grade, calculate_statistics

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")
st.title("🎓 Student Performance Dashboard")

st.sidebar.header("➕ Student əlavə etmək")
with st.sidebar.form("add_student_form"):
    student_name = st.text_input("Student Name")
    student_score = st.number_input(
        "Score", min_value=0.0, max_value=100.0, step=1.0
    )
    submit_button = st.form_submit_button("Add Student")

    if submit_button:
        if student_name.strip():
            add_student(student_name.strip(), student_score)
            st.success(f"{student_name} əlavə edildi!")
            st.rerun()
        else:
            st.warning("Tələbə adını daxil edin.")

st.subheader("🔍 Student axtarışı")
search_query = st.text_input("Search Student")

students_data = get_students(search_query)

for student in students_data:
    student["Grade"] = calculate_grade(student["Score"])

stats = calculate_statistics(students_data)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students", stats["total_students"])
col2.metric("Average Score", stats["average_score"])
col3.metric("Highest Score", stats["highest_score"])
col4.metric("Lowest Score", stats["lowest_score"])

st.markdown("---")

st.subheader("📋 Student siyahısı")
if students_data:
    df = pd.DataFrame(students_data)[["Name", "Score", "Grade"]]
    st.dataframe(df, use_container_width=True)
else:
    st.info("Məlumat tapılmadı.")