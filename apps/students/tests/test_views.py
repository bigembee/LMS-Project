"""
test_views.py - Tests for student views.

WHAT TO TEST:
    - Dashboard loads for students (status 200)
    - Dashboard redirects non-students (status 403 or 302)
    - Course registration works
    - GPA calculation is correct

EXAMPLE:
    class StudentDashboardTest(TestCase):
        def setUp(self):
            self.student = User.objects.create_user(
                username="student1", password="pass123", role="student"
            )
            self.lecturer = User.objects.create_user(
                username="lecturer1", password="pass123", role="lecturer"
            )

        def test_student_can_access_dashboard(self):
            self.client.login(username="student1", password="pass123")
            response = self.client.get("/students/dashboard/")
            self.assertEqual(response.status_code, 200)

        def test_lecturer_cannot_access_student_dashboard(self):
            self.client.login(username="lecturer1", password="pass123")
            response = self.client.get("/students/dashboard/")
            self.assertEqual(response.status_code, 403)  # Forbidden
"""

from django.test import TestCase


class StudentDashboardTest(TestCase):
    pass
