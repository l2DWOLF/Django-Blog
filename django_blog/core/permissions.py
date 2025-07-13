from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.permissions import BasePermission, DjangoModelPermissions
from blog.models import *


class IsAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        # Admin check
        is_admin = (
            request.user and
            request.user.is_authenticated and
            request.user.is_superuser
        )
        if is_admin:
            return True

        # Moderator check
        in_mod_group = (
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name='moderators').exists()
        )
        return in_mod_group


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, 'author'):
            return obj.author.user == request.user
        return False


class IsOwnerOrModelPermissions(DjangoModelPermissions):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check for UserProfile
        if isinstance(obj, UserProfile):
            return obj.user == request.user or request.user.is_superuser

        # Check for User (same rule as UserProfile, admins can view/delete)
        if isinstance(obj, User):
            return obj == request.user or request.user.is_superuser

        # Only owners or moderators can modify articles/comments
        if isinstance(obj, Article) or isinstance(obj, Comment):
            return (
                obj.author.user == request.user
                or request.user.is_superuser
                or request.user.is_staff
            )

        
        # For likes (ArticleLike & CommentLike), only allow viewing for Moderators & Admins
        if isinstance(obj, ArticleLike) or isinstance(obj, CommentLike):
            return request.method in permissions.SAFE_METHODS
        return False

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.is_superuser:
                return True

            if request.user.groups.filter(name='moderators').exists():
                return request.method in permissions.SAFE_METHODS
        return request.method in permissions.SAFE_METHODS

class IsAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser: 
            return True
        return request.user == view.get_object().user
