"""
test_models.py - Tests for the accounts models.

HOW TESTING WORKS:
    - Each test class inherits from Django's TestCase
    - Each method starting with "test_" is a test case
    - Run tests: python manage.py test apps.accounts
    - Or with pytest: pytest apps/accounts/tests/

WHAT TO TEST:
    - Model creation (can we create a user?)
    - Model properties (does is_student return True for students?)
    - Model methods (does __str__ return the right string?)
    - Model validation (does the role field reject invalid values?)

EXAMPLE TESTS (uncomment and expand when ready):

    class UserModelTest(TestCase):
        def setUp(self):
            # setUp() runs BEFORE each test method — creates test data
            self.student = User.objects.create_user(
                username="teststudent",
                password="testpass123",
                role="student",
                first_name="John",
                last_name="Doe",
            )

        def test_user_creation(self):
            self.assertEqual(self.student.username, "teststudent")
            self.assertEqual(self.student.role, "student")

        def test_is_student_property(self):
            self.assertTrue(self.student.is_student)
            self.assertFalse(self.student.is_lecturer)

        def test_str_representation(self):
            self.assertEqual(str(self.student), "John Doe (student)")
"""

from django.test import TestCase
from apps.accounts.models import User


class UserModelTest(TestCase):
    pass
