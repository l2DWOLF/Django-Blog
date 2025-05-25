from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework import status 
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import Throttled


def blog_except_handler(exc, context):
    response = exception_handler(exc, context)
    
    if isinstance(exc, Http404):
        return Response({"Error":"Resource Not Found."}, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, ValueError):
        return Response({"Error":"Invalid Input."}, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, PermissionDenied):
        return Response({"Error":"Permission Denied."}, status=status.HTTP_403_FORBIDDEN)
    
    if isinstance(exc, Throttled):
        return Response({"Error": "Request was Throttled, too many requests."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    
    return response