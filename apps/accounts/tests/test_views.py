"""
test_views.py - Tests for the accounts views.

VIEW TESTS check:
    - Does the URL return the right status code? (200 OK, 302 Redirect, 403 Forbidden)
    - Does the URL use the right template?
    - Does the view redirect unauthenticated users?
    - Does form submission create/update the right data?

Django's test client simulates a browser — it can make GET/POST requests
without running a real server.

EXAMPLE TESTS (uncomment and expand when ready):

    class LoginViewTest(TestCase):
        def test_login_page_loads(self):
            # self.client is a test browser that Django provides
            response = self.client.get("/accounts/login/")
            self.assertEqual(response.status_code, 200)

        def test_login_with_valid_credentials(self):
            User.objects.create_user(username="testuser", password="testpass123")
            response = self.client.post("/accounts/login/", {
                "username": "testuser",
                "password": "testpass123",
            })
            # After successful login, should redirect (302) to the dashboard
            self.assertEqual(response.status_code, 302)

    class DashboardRedirectTest(TestCase):
        def test_student_redirects_to_student_dashboard(self):
            user = User.objects.create_user(username="student1", password="pass123", role="student")
            self.client.login(username="student1", password="pass123")
            response = self.client.get("/accounts/dashboard/")
            self.assertRedirects(response, "/students/dashboard/")
"""

from django.test import TestCase


class AccountViewsTest(TestCase):
    pass
