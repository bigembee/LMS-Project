"""
utils.py - Shared utility functions for the Core app.

These are reusable helper functions used across multiple apps.
They handle file validation (size and type checking) for user uploads.

USED IN:
    - Assignment submission forms (validate student uploads)
    - Profile picture uploads (validate image files)
    - Course material uploads (validate document files)

HOW TO USE IN MODELS:
    from apps.core.utils import validate_file_size, validate_file_extension

    class Submission(models.Model):
        file = models.FileField(
            upload_to="submissions/",
            validators=[validate_file_size, validate_file_extension],
            # Django will call these validators when the form is submitted
            # If validation fails, the form shows an error and the file is rejected
        )

HOW TO USE IN VIEWS:
    def submit_assignment(request):
        uploaded_file = request.FILES["file"]
        try:
            validate_file_size(uploaded_file, max_size_mb=10)
            validate_file_extension(uploaded_file, allowed_extensions=[".pdf", ".docx"])
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect("assignments:submit", pk=pk)
"""

import os  # For file path operations (extracting file extensions)
from django.core.exceptions import ValidationError  # Django's validation error


def validate_file_size(file, max_size_mb=10):
    """
    Check that an uploaded file doesn't exceed the maximum size.

    Parameters:
        file: the uploaded file object (from request.FILES)
        max_size_mb: maximum allowed size in megabytes (default: 10MB)

    Raises:
        ValidationError: if the file is too large

    HOW IT WORKS:
        file.size returns the file size in BYTES
        1 MB = 1024 * 1024 bytes = 1,048,576 bytes
        So 10 MB = 10 * 1024 * 1024 = 10,485,760 bytes
    """
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"File size must not exceed {max_size_mb}MB.")


def validate_file_extension(file, allowed_extensions=None):
    """
    Check that an uploaded file has an allowed file extension.

    Parameters:
        file: the uploaded file object
        allowed_extensions: list of allowed extensions (e.g., [".pdf", ".docx"])
                          If None, uses a default list of common file types.

    Raises:
        ValidationError: if the file extension is not in the allowed list

    HOW IT WORKS:
        os.path.splitext("report.pdf") returns ("report", ".pdf")
        We take the extension part [1] and check if it's in the allowed list
    """
    if allowed_extensions is None:
        # Default allowed file types — covers common document and image formats
        allowed_extensions = [".pdf", ".doc", ".docx", ".txt", ".zip", ".png", ".jpg"]

    # os.path.splitext() splits "filename.pdf" into ("filename", ".pdf")
    # [1] gets the extension part: ".pdf"
    # .lower() makes it case-insensitive (".PDF" becomes ".pdf")
    ext = os.path.splitext(file.name)[1].lower()

    if ext not in allowed_extensions:
        raise ValidationError(f"File type '{ext}' is not allowed. Allowed: {', '.join(allowed_extensions)}")
