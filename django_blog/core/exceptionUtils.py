from rest_framework.response import Response

def format_isinstance(exc, exc_type, message, status_code):
    if isinstance(exc, exc_type):
        return Response({"backend_error": [message]}, status=status_code)