import sqlite3
import pyodbc
from config import DB_DRIVER, DB_NAME, DB_SERVER


def get_sqlite_connection():
    conn = sqlite3.connect("university.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Students (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Score REAL NOT NULL
        )
    """
    )
    cursor.execute("SELECT COUNT(*) FROM Students")
    if cursor.fetchone()[0] == 0:
        sample_students = [
            ("Ali", 85),
            ("Leyla", 72),
            ("Murad", 48),
            ("Aysel", 91),
            ("Kamran", 63),
        ]
        cursor.executemany(
            "INSERT INTO Students (Name, Score) VALUES (?, ?)", sample_students
        )
    conn.commit()
    return conn


def create_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={DB_DRIVER};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;",
            timeout=2,
        )
        return ("odbc", conn)
    except Exception:
        return ("sqlite", get_sqlite_connection())


def add_student(name: str, score: float):
    db_type, conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO Students (Name, Score) VALUES (?, ?)"
        cursor.execute(query, (name, score))
        conn.commit()
        conn.close()


def get_students(search_term: str = ""):
    db_type, conn = create_connection()
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
    db_type, conn = create_connection()
    student = None
    if conn:
        cursor = conn.cursor()
        if db_type == "odbc":
            query = "EXEC GetStudentResult @StudentId = ?"
            cursor.execute(query, (student_id,))
        else:
            query = "SELECT Id, Name, Score FROM Students WHERE Id = ?"
            cursor.execute(query, (student_id,))

        row = cursor.fetchone()
        if row:
            student = {"Id": row[0], "Name": row[1], "Score": row[2]}
        conn.close()
    return student