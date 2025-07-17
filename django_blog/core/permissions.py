from rest_framework import permissions
from rest_framework.permissions import BasePermission, DjangoModelPermissions
from django.contrib.auth import get_user_model
from blog.models import Article, Comment, ArticleLike, CommentLike, UserProfile

CustomUser = get_user_model()


class IsAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and (
                request.user.is_superuser or
                request.user.groups.filter(name='moderators').exists()
            )
        )

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return is_owner(request.user, obj)

class IsOwnerOrModelPermissions(DjangoModelPermissions):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            is_owner(request.user, obj) or
            request.user.is_superuser or
            request.user.has_perm(
                f'{obj._meta.app_label}.change_{obj._meta.model_name}')
        )

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            if request.user.groups.filter(name='moderators').exists():
                return request.method in permissions.SAFE_METHODS
        return request.method in permissions.SAFE_METHODS

class IsAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return is_owner(request.user, obj)

def is_owner(user, obj):
    if not user or not user.is_authenticated:
        return False

    if isinstance(obj, UserProfile):
        return obj.user == user

    if isinstance(obj, CustomUser):
        return obj == user

    if hasattr(obj, 'user'):
        return obj.user == user

    if hasattr(obj, 'author'):
        author = obj.author
        return getattr(author, 'user', None) == user

    return False
