from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.permissions import BasePermission, DjangoModelPermissions
from blog.models import *


class IsAdminOrModerator(BasePermission):
    """
    Custom permission to grant access to Admin or Moderator group.
    """

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
    """
    Custom permission to allow owners to edit their own objects, but allow others to view.
    """

    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, 'author'):
            return obj.author.user == request.user
        return False


class IsOwnerOrModelPermissions(DjangoModelPermissions):
    """
    Custom permissions for models, allowing full access to the owner and admins.
    Moderators can view, and users can only access their own profile, article, and comment.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # Allow view-only access to authenticated users
            return True

        # Check for UserProfile
        if isinstance(obj, UserProfile):
            # Allow the owner to modify their profile, and allow admins to modify any profile
            return obj.user == request.user or request.user.is_superuser

        # Check for User (same rule as UserProfile, admins can view/delete)
        if isinstance(obj, User):
            return obj == request.user or request.user.is_superuser

        # Check for Articles and Comments
        if isinstance(obj, Article) or isinstance(obj, Comment):
            # Only owners or moderators can modify articles/comments
            return (
                obj.author.user == request.user
                or request.user.is_superuser
                or request.user.groups.filter(name='moderators').exists()
            )

        # For likes (ArticleLike & CommentLike), only allow viewing for Moderators & Admins
        if isinstance(obj, ArticleLike) or isinstance(obj, CommentLike):
            return request.method in permissions.SAFE_METHODS  # View-only for likes/dislikes

        return False

class IsAdminOrReadOnly(BasePermission):
    """
    Allow full CRUD access to admins, but restrict all others to read-only.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.is_superuser:  # Admins get full access
                return True
            # Moderators can view only
            if request.user.groups.filter(name='moderators').exists():
                return request.method in permissions.SAFE_METHODS
        # For non-logged-in users (view only)
        return request.method in permissions.SAFE_METHODS


class IsAdminOrOwner(BasePermission):
    """
    Allow full CRUD access to admins, but restrict owners to their own objects.
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:  # Admins get full access
            return True
        # Owners can access their own objects
        return request.user == view.get_object().user
