from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from taggit.models import Tag
from blog.models import *
from blog.management.commands.seeding_tools import *
from blog.management.commands.group_models_permissions import mods_group_permissions, users_group_permissions
from random import choice

class Command(BaseCommand):
    help = 'Seed the database with initial data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding The Database...'))
# create moderators group + permissions
        mods_group, _ = Group.objects.get_or_create(name='moderators')
        mods_group.permissions.add(*mods_group_permissions)
# create users group + permissions
        users_group, _ = Group.objects.get_or_create(name='users')
        users_group.permissions.add(*users_group_permissions)
# create admin superuser
        admin_user, created = User.objects.get_or_create(username='admin', defaults=admin_defaults)
        admin_user.set_password('AdminUser1234!')
        admin_user.save()
# create moderator
        moderator_user, created = User.objects.get_or_create(username='moderator', defaults=moderator_defaults)
        moderator_user.set_password('ModUser1234!')
        moderator_user.groups.add(mods_group)
        moderator_user.save()
# create user
        regular_user, created = User.objects.get_or_create(
            username='blog_user', defaults=user_defaults)
        regular_user.set_password('UserUser1234!')
        regular_user.save()
# create tags
        for tag in tags_list:
            Tag.objects.get_or_create(name=tag)
# create articles
        for i in range(4):
            author_id = i + 1
            if author_id > 2:
                author_id = 2

            authorProfile, _ = UserProfile.objects.get_or_create(id=author_id)
            article, _ = Article.objects.get_or_create(
                author=authorProfile,
                title=article_data[i]['title'],
                content=article_data[i]['content'],
                status=status_list[i-1]
            )
            article.tags.add(*article_tags[i-1])
            article.save()

            # Create comments for the current article
            for j in range(3):
                userProfile = regular_user if j % 2 == 0 else moderator_user

                comment, _ = Comment.objects.get_or_create(
                    author=userProfile.userprofile,
                    article=article,
                    content=f"Comment {j + 1} on article {i + 1}",
                    status='publish'
                )
                comment.save()

                if j > 0:
                    parent_comment, _ = Comment.objects.get_or_create(
                        article=article, content=f"Comment {j} on article {i + 1}")
                    nested_comment, _ = Comment.objects.get_or_create(
                        author=regular_user.userprofile,
                        article=article,
                        content=f"Reply to Comment {j} on article {i + 1}",
                        reply_to=parent_comment,
                        status='publish'
                    )
                    nested_comment.save()

# create article & comment likes, dislikes.
        users = UserProfile.objects.all()
        for user in users:
            articles = Article.objects.all()
            for article in articles:
                like_status = choice(['like', 'dislike'])
                if not ArticleLike.objects.filter(user=user, article=article).exists():
                    ArticleLike.objects.create(
                        user=user,
                        article=article,
                        status=like_status
                    )

            comments = Comment.objects.all()
            for comment in comments:
                like_status = choice(['like', 'dislike'])  # 
                if not CommentLike.objects.filter(user=user, comment=comment).exists():
                    CommentLike.objects.create(
                        user=user,
                        comment=comment,
                        status=like_status
                    )


        self.stdout.write(self.style.SUCCESS('Seeding Completed Successfully...'))