"""
test_models.py - Tests for course-related models.

WHAT TO TEST:
    - Creating departments, sessions, semesters, courses, enrollments
    - String representations (__str__)
    - Unique constraints (no duplicate course codes, no duplicate enrollments)
    - Properties (enrolled_count, is_full)
    - Cascade deletes (deleting a department deletes its courses)

EXAMPLE:
    class CourseModelTest(TestCase):
        def setUp(self):
            self.department = Department.objects.create(name="Computer Science", code="CSC")
            self.session = AcademicSession.objects.create(
                name="2025/2026", start_date="2025-09-01", end_date="2026-07-31"
            )
            self.semester = Semester.objects.create(
                session=self.session, name="first",
                start_date="2025-09-01", end_date="2026-01-31"
            )
            self.course = Course.objects.create(
                code="CSC201", title="Intro to Python",
                department=self.department, semester=self.semester
            )

        def test_enrolled_count_starts_at_zero(self):
            self.assertEqual(self.course.enrolled_count, 0)
"""

from django.test import TestCase


class CourseModelTest(TestCase):
    pass


class EnrollmentModelTest(TestCase):
    pass
