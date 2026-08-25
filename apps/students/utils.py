"""
utils.py - Utility functions for the Students app.

These are pure calculation functions — they don't touch the database or handle requests.
They take input data and return computed results.

USED IN: apps/students/views.py → gpa() view

GPA (Grade Point Average) CALCULATION:
    GPA = Sum(grade_point × credit_units) / Sum(credit_units)

    Example:
        Course A: Grade = A (5.0 points), 3 credit units → 5.0 × 3 = 15.0
        Course B: Grade = B (4.0 points), 2 credit units → 4.0 × 2 = 8.0
        Course C: Grade = C (3.0 points), 4 credit units → 3.0 × 4 = 12.0

        Total points = 15.0 + 8.0 + 12.0 = 35.0
        Total credits = 3 + 2 + 4 = 9
        GPA = 35.0 / 9 = 3.89

GRADING SCALE (Nigerian university system):
    70-100 = A (5.0)
    60-69  = B (4.0)
    50-59  = C (3.0)
    45-49  = D (2.0)
    40-44  = E (1.0)
    0-39   = F (0.0)
"""

from decimal import Decimal  # Decimal is more precise than float for financial/grade calculations


def calculate_gpa(grades):
    """
    Calculate GPA from a list of (grade_point, credit_units) tuples.
    Uses a 5.0 scale (common in Nigerian universities).

    Parameters:
        grades: list of tuples, e.g., [(Decimal("5.0"), 3), (Decimal("4.0"), 2)]
                Each tuple is (grade_point, credit_units)

    Returns:
        Decimal: the calculated GPA, rounded to 2 decimal places

    Example:
        grades = [(Decimal("5.0"), 3), (Decimal("4.0"), 2)]
        calculate_gpa(grades)  # Returns Decimal("4.60")
    """
    if not grades:
        return Decimal("0.00")  # No grades → GPA is 0

    # Calculate weighted sum: grade_point × credit_units for each course
    # Then sum them all up
    total_points = sum(gp * cu for gp, cu in grades)

    # Sum of all credit units
    total_credits = sum(cu for _, cu in grades)
    # The "_" means "I don't need this variable" — we only need credit units here

    if total_credits == 0:
        return Decimal("0.00")  # Avoid division by zero

    # Calculate GPA and round to 2 decimal places
    # Decimal("0.01") tells quantize() to round to 2 decimal places
    return Decimal(str(total_points / total_credits)).quantize(Decimal("0.01"))


# Mapping of letter grades to grade points (5.0 scale)
# Used to convert a letter grade to its numeric value for GPA calculation
GRADE_POINTS = {
    "A": Decimal("5.0"),
    "B": Decimal("4.0"),
    "C": Decimal("3.0"),
    "D": Decimal("2.0"),
    "E": Decimal("1.0"),
    "F": Decimal("0.0"),
}


def score_to_grade(score):
    """
    Convert a numeric score (0-100) to a letter grade.

    Parameters:
        score: int or float, the student's score (e.g., 75)

    Returns:
        str: the letter grade ("A", "B", "C", "D", "E", or "F")

    Example:
        score_to_grade(75)  # Returns "A"
        score_to_grade(55)  # Returns "C"
        score_to_grade(35)  # Returns "F"
    """
    if score >= 70:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C"
    elif score >= 45:
        return "D"
    elif score >= 40:
        return "E"
    return "F"
