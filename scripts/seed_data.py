"""
seed_data.py - Populate the database with sample data for development.

WHAT IS SEEDING?
    Seeding fills your database with fake/sample data so you can:
    - Test your views and templates with realistic data
    - Demo the app to your team without manually creating records
    - Have a consistent starting point for development

HOW TO RUN:
    python manage.py shell < scripts/seed_data.py

    OR import and run manually in the Django shell:
    python manage.py shell
    >>> exec(open("scripts/seed_data.py").read())

TODO: Implement seed data creation:
    - Create sample departments (Computer Science, Mathematics, etc.)
    - Create an academic session and semesters
    - Create sample courses
    - Create sample users (students, lecturers, admin)
    - Create sample enrollments
    - Create sample assignments and submissions

EXAMPLE:
    from apps.accounts.models import User
    from apps.courses.models import Department, AcademicSession, Semester, Course, Enrollment

    # Create departments
    cs = Department.objects.create(name="Computer Science", code="CSC")
    mth = Department.objects.create(name="Mathematics", code="MTH")

    # Create admin
    admin = User.objects.create_superuser(
        username="admin", password="admin123", email="admin@lms.com", role="admin"
    )

    # Create lecturers
    lecturer1 = User.objects.create_user(
        username="dr_smith", password="pass123", email="smith@lms.com",
        role="lecturer", first_name="John", last_name="Smith"
    )

    # Create students
    student1 = User.objects.create_user(
        username="student001", password="pass123", email="student1@lms.com",
        role="student", first_name="Jane", last_name="Doe"
    )

    print("Seed data created successfully!")
"""
