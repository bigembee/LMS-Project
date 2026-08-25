"""
middleware.py - Custom middleware for the Core app.

WHAT IS MIDDLEWARE?
    Middleware is code that runs on EVERY request and response.
    It sits between the web server and your views, like layers of an onion.

    REQUEST:  Browser → Middleware 1 → Middleware 2 → ... → View
    RESPONSE: View → ... → Middleware 2 → Middleware 1 → Browser

HOW MIDDLEWARE WORKS:
    1. __init__() is called ONCE when the server starts
    2. __call__() is called on EVERY request

    Inside __call__():
        - Code BEFORE get_response(request) runs during the REQUEST phase
        - get_response(request) calls the next middleware or the view
        - Code AFTER get_response(request) runs during the RESPONSE phase

TO ACTIVATE THIS MIDDLEWARE:
    Add it to MIDDLEWARE list in settings.py:
    MIDDLEWARE = [
        ...
        "apps.core.middleware.AuditLogMiddleware",
    ]
"""

from .models import AuditLog


class AuditLogMiddleware:
    """
    Middleware to log user actions for an audit trail.

    This is a SKELETON — implement the logging logic based on your needs.

    POSSIBLE IMPLEMENTATION:
        - Log all POST/PUT/DELETE requests (data-changing operations)
        - Skip GET requests (just reading data, not worth logging)
        - Record the URL, method, user, and IP address

    EXAMPLE:
        def __call__(self, request):
            response = self.get_response(request)

            # Only log data-changing requests, and only for logged-in users
            if request.method in ["POST", "PUT", "PATCH", "DELETE"] and request.user.is_authenticated:
                AuditLog.objects.create(
                    user=request.user,
                    action=request.method,
                    model_name=request.path,
                    details=f"{request.method} {request.path}",
                    ip_address=request.META.get("REMOTE_ADDR"),
                )

            return response
    """

    def __init__(self, get_response):
        """
        Called once when the server starts.

        get_response is a callable that takes a request and returns a response.
        It represents the next middleware in the chain, or the view itself.
        We store it so we can call it later in __call__().
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Called on EVERY request.

        1. (Optional) Do something with the request BEFORE it reaches the view
        2. Pass the request to the next middleware/view
        3. (Optional) Do something with the response BEFORE it goes back to the browser
        """
        # --- PRE-VIEW PROCESSING (runs before the view) ---
        # You could log the incoming request here

        # Pass the request to the next middleware or view, and get the response
        response = self.get_response(request)

        # --- POST-VIEW PROCESSING (runs after the view) ---
        # You could log the response status code here

        return response
