from config import (
    GRADE_A_THRESHOLD,
    GRADE_B_THRESHOLD,
    GRADE_C_THRESHOLD,
    GRADE_D_THRESHOLD,
)


def calculate_grade(score: float) -> str:
    if score >= GRADE_A_THRESHOLD:
        return "A"
    elif score >= GRADE_B_THRESHOLD:
        return "B"
    elif score >= GRADE_C_THRESHOLD:
        return "C"
    elif score >= GRADE_D_THRESHOLD:
        return "D"
    return "F"


def calculate_statistics(students: list) -> dict:
    if not students:
        return {
            "total_students": 0,
            "average_score": 0.0,
            "highest_score": 0,
            "lowest_score": 0,
        }

    scores = [s["Score"] for s in students]
    total_students = len(scores)
    average_score = sum(scores) / total_students

    return {
        "total_students": total_students,
        "average_score": round(average_score, 1),
        "highest_score": max(scores),
        "lowest_score": min(scores),
    }