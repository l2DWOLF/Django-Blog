from rest_framework import permissions
from rest_framework.permissions import BasePermission, DjangoModelPermissions
from django.contrib.auth import get_user_model
from blog.models import Article, Comment, ArticleLike, CommentLike, UserProfile

CustomUser = get_user_model()


class IsAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        # Admin check
        if request.user and request.user.is_authenticated and request.user.is_superuser:
            return True

        # Moderator group check
        return (
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name='moderators').exists()
        )


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read-only access
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if object has author attribute
        if hasattr(obj, 'author'):
            return obj.author.user == request.user
        return False


class IsOwnerOrModelPermissions(DjangoModelPermissions):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # UserProfile: allow user or admin
        if isinstance(obj, UserProfile):
            return obj.user == request.user or request.user.is_superuser

        # CustomUser: allow self or admin
        if isinstance(obj, CustomUser):
            return obj == request.user or request.user.is_superuser

        # Articles & Comments: allow owner, moderator, or admin
        if isinstance(obj, Article) or isinstance(obj, Comment):
            return (
                obj.author.user == request.user
                or request.user.is_superuser
                or request.user.is_staff
            )

        # Likes: readonly for moderators/admins
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
