from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from blog.models import Article, ArticleLike, Comment, CommentLike, UserProfile

CustomUser = get_user_model()


def get_permission(codename, model):
    content_type = ContentType.objects.get_for_model(model)
    permission, created = Permission.objects.get_or_create(
        codename=codename,
        content_type=content_type,
        defaults={
            'name': f"Can {codename.replace('_', ' ')} {model._meta.verbose_name}"}
    )
    return permission


def get_mods_group_permissions():
    return [
        get_permission('view_customuser', CustomUser),
        get_permission('add_customuser', CustomUser),
        get_permission('change_customuser', CustomUser),
        get_permission('delete_customuser', CustomUser),

        get_permission('view_userprofile', UserProfile),
        get_permission('add_userprofile', UserProfile),
        get_permission('change_userprofile', UserProfile),
        get_permission('delete_userprofile', UserProfile),

        get_permission('view_article', Article),
        get_permission('add_article', Article),
        get_permission('change_article', Article),
        get_permission('delete_article', Article),

        get_permission('view_comment', Comment),
        get_permission('add_comment', Comment),
        get_permission('change_comment', Comment),
        get_permission('delete_comment', Comment),

        get_permission('view_articlelike', ArticleLike),
        get_permission('add_articlelike', ArticleLike),
        get_permission('change_articlelike', ArticleLike),
        get_permission('delete_articlelike', ArticleLike),

        get_permission('view_commentlike', CommentLike),
        get_permission('add_commentlike', CommentLike),
        get_permission('change_commentlike', CommentLike),
        get_permission('delete_commentlike', CommentLike),
    ]



def get_users_group_permissions():
    return [
        get_permission('view_user', CustomUser),
        get_permission('add_user', CustomUser),
        get_permission('change_user', CustomUser),
        get_permission('delete_user', CustomUser),

        get_permission('view_userprofile', UserProfile),
        get_permission('add_userprofile', UserProfile),
        get_permission('change_userprofile', UserProfile),
        get_permission('delete_userprofile', UserProfile),

        get_permission('view_article', Article),

        get_permission('view_comment', Comment),
        get_permission('add_comment', Comment),
        get_permission('change_comment', Comment),
        get_permission('delete_comment', Comment),

        get_permission('view_articlelike', ArticleLike),
        get_permission('add_articlelike', ArticleLike),
        get_permission('change_articlelike', ArticleLike),
        get_permission('delete_articlelike', ArticleLike),

        get_permission('view_commentlike', CommentLike),
        get_permission('add_commentlike', CommentLike),
        get_permission('change_commentlike', CommentLike),
        get_permission('delete_commentlike', CommentLike),
    ]
