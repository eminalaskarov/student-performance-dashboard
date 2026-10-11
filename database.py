import pyodbc
from config import DB_DRIVER, DB_NAME, DB_SERVER


def create_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={DB_DRIVER};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        return conn
    except Exception as e:
        print(f"Database error: {e}")
        return None


def add_student(name: str, score: float):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO Students (Name, Score) VALUES (?, ?)"
        cursor.execute(query, (name, score))
        conn.commit()
        conn.close()


def get_students(search_term: str = ""):
    conn = create_connection()
    students = []
    if conn:
        cursor = conn.cursor()
        if search_term:
            query = "SELECT Id, Name, Score FROM Students WHERE Name LIKE ?"
            cursor.execute(query, (f"%{search_term}%",))
        else:
            query = "SELECT Id, Name, Score FROM Students"
            cursor.execute(query)

        rows = cursor.fetchall()
        for row in rows:
            students.append({"Id": row[0], "Name": row[1], "Score": row[2]})
        conn.close()
    return students


def get_student(student_id: int):
    conn = create_connection()
    student = None
    if conn:
        cursor = conn.cursor()
        query = "EXEC GetStudentResult @StudentId = ?"
        cursor.execute(query, (student_id,))
        row = cursor.fetchone()
        if row:
            student = {"Id": row[0], "Name": row[1], "Score": row[2]}
        conn.close()
    return student