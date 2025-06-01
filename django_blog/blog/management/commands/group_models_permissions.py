from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from blog.models import Article, ArticleLike, Comment, CommentLike

view_article_permission = Permission.objects.get(
    codename='view_article',
    content_type=ContentType.objects.get_for_model(Article)
)
add_article_permission = Permission.objects.get(
    codename='add_article',
    content_type=ContentType.objects.get_for_model(Article)
)
change_article_permission = Permission.objects.get(
    codename='change_article',
    content_type=ContentType.objects.get_for_model(Article)
)
delete_article_permission = Permission.objects.get(
    codename='delete_article',
    content_type=ContentType.objects.get_for_model(Article)
)

view_comment_permission = Permission.objects.get(
    codename='view_comment',
    content_type=ContentType.objects.get_for_model(Comment)
)
add_comment_permission = Permission.objects.get(
    codename='add_comment',
    content_type=ContentType.objects.get_for_model(Comment)
)
change_comment_permission = Permission.objects.get(
    codename='change_comment',
    content_type=ContentType.objects.get_for_model(Comment)
)
delete_comment_permission = Permission.objects.get(
    codename='delete_comment',
    content_type=ContentType.objects.get_for_model(Comment)
)

view_articlelike_permission = Permission.objects.get(
    codename='view_articlelike',
    content_type=ContentType.objects.get_for_model(ArticleLike)
)
add_articlelike_permission = Permission.objects.get(
    codename='add_articlelike',
    content_type=ContentType.objects.get_for_model(ArticleLike)
)
change_articlelike_permission = Permission.objects.get(
    codename='change_articlelike',
    content_type=ContentType.objects.get_for_model(ArticleLike)
)
delete_articlelike_permission = Permission.objects.get(
    codename='delete_articlelike',
    content_type=ContentType.objects.get_for_model(ArticleLike)
)

view_commentlike_permission = Permission.objects.get(
    codename='view_commentlike',
    content_type=ContentType.objects.get_for_model(CommentLike)
)
add_commentlike_permission = Permission.objects.get(
    codename='add_commentlike',
    content_type=ContentType.objects.get_for_model(CommentLike)
)
change_commentlike_permission = Permission.objects.get(
    codename='change_commentlike',
    content_type=ContentType.objects.get_for_model(CommentLike)
)
delete_commentlike_permission = Permission.objects.get(
    codename='delete_commentlike',
    content_type=ContentType.objects.get_for_model(CommentLike)
)



mods_group_permissions = [
    view_article_permission,
    add_article_permission,
    change_article_permission,
    delete_article_permission,

    view_comment_permission,
    add_comment_permission,
    change_comment_permission,
    delete_comment_permission,

    view_articlelike_permission,
    add_articlelike_permission,
    change_articlelike_permission,
    delete_articlelike_permission,

    view_commentlike_permission,
    add_commentlike_permission,
    change_commentlike_permission,
    delete_commentlike_permission,
]

users_group_permissions = [
    view_article_permission,

    view_comment_permission,
    add_comment_permission,
    change_comment_permission,
    delete_comment_permission,

    view_articlelike_permission,
    add_articlelike_permission,
    change_articlelike_permission,
    delete_articlelike_permission,

    view_commentlike_permission,
    add_commentlike_permission,
    change_commentlike_permission,
    delete_commentlike_permission,
]