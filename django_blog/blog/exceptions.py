import logging
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.db.models.deletion import ProtectedError
from rest_framework import status 
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import (
    Throttled, ValidationError, AuthenticationFailed,
    NotAuthenticated, ParseError, NotFound, MethodNotAllowed,
    UnsupportedMediaType, NotAcceptable, PermissionDenied as DRFPermissionDenied)
from core.exceptionUtils import format_isinstance


logger = logging.getLogger(__name__)

def blog_except_handler(exc, context):
    response = exception_handler(exc, context)
    
    for exc_type, message, status_code in [
        (Http404, "Resource Not Found.", status.HTTP_404_NOT_FOUND),
        (ValueError, f"{str(exc)} - Invalid Input.", status.HTTP_400_BAD_REQUEST),
       # (AttributeError, f"{str(exc)} - Attribute Error Occurred.", status.HTTP_400_BAD_REQUEST),
        (PermissionDenied, "Permission Denied.", status.HTTP_403_FORBIDDEN),
        (DRFPermissionDenied, str(exc), status.HTTP_403_FORBIDDEN),
        (Throttled, "Throttled Request, too many requests - Please try again soon..",
            status.HTTP_429_TOO_MANY_REQUESTS),
        (ParseError, "Malformed request.", status.HTTP_400_BAD_REQUEST),
        (NotFound, "Endpoint Not Found.", status.HTTP_404_NOT_FOUND),
        (MethodNotAllowed, "Method not allowed.",
            status.HTTP_405_METHOD_NOT_ALLOWED),
        (UnsupportedMediaType, "Unsupported media type.",
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE),
        (NotAcceptable, "Not acceptable.", status.HTTP_406_NOT_ACCEPTABLE),
        (AuthenticationFailed, str(exc), status.HTTP_401_UNAUTHORIZED),
        (NotAuthenticated, str(exc), status.HTTP_401_UNAUTHORIZED),
    ]:
        formatted = format_isinstance(exc, exc_type, message, status_code)
        if formatted:
            return formatted
    
    if isinstance(exc, ValidationError) or isinstance(exc, ValueError) and response is not None:
        formatted_errors = []
        if isinstance(response.data, dict):
            for key, value in response.data.items():
                if isinstance(value, list):
                    formatted_errors.extend(value)
                else:
                    formatted_errors.append(str(value))
        elif isinstance(response.data, list):
            formatted_errors.extend(response.data)
        else:
            formatted_errors.append(str(response.data))

        logger.warning(f"ValidationError caught: {formatted_errors}")
        return Response({"backend_error": formatted_errors}, status=response.status_code)

    if isinstance(exc, ProtectedError):
        logger.warning(f"ProtectedError caught: Attempt to delete a model with active depenencies.")
        return Response(
            {"backend_error": ["Cannot delete this model because it has dependencies. You can edit the comment/reply instead."]},
            status=status.HTTP_400_BAD_REQUEST)
    
# Catch All Exceptions # 
    if response is None:
        logger.exception(f"Unhandled exception in {context.get('view')} | "
                        f"Method: {context.get('request').method} | "
                        f"Path: {context.get('request').path}",
                        exc_info=exc)
        return Response(
            {"backend_error": ["An unexpected error occured, please try again later.."]},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 

    if response and isinstance(response.data, dict) and "backend_error" not in response.data:
        logger.warning(f"Unhandled DRF response: {response.data}")
        return Response(
            {"backend_error": [
                "FALLBACK: Unknown error occurred (not caught by backend)"]},
            status=response.status_code
        )
    return response