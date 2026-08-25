"""
test_models.py - Tests for assignment-related models.

WHAT TO TEST:
    - Creating assignments, submissions, grades
    - unique_together on Submission (one submission per student per assignment)
    - Grade percentage calculation
    - Status transitions (submitted → graded → returned)
"""

from django.test import TestCase


class AssignmentModelTest(TestCase):
    pass


class SubmissionModelTest(TestCase):
    pass
