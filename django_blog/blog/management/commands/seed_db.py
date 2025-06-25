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

        # Create groups and assign permissions
        mods_group, _ = Group.objects.get_or_create(name='moderators')
        mods_group.permissions.add(*mods_group_permissions)

        users_group, _ = Group.objects.get_or_create(name='users')
        users_group.permissions.add(*users_group_permissions)

        # Create users
        admin_user, _ = User.objects.get_or_create(
            username='admin', defaults=admin_defaults)
        admin_user.set_password('AdminUser1234!')
        admin_user.save()

        moderator_user, _ = User.objects.get_or_create(
            username='moderator', defaults=moderator_defaults)
        moderator_user.set_password('ModUser1234!')
        moderator_user.groups.add(mods_group)
        moderator_user.save()

        regular_user, _ = User.objects.get_or_create(
            username='blog_user', defaults=user_defaults)
        regular_user.set_password('UserUser1234!')
        regular_user.groups.add(users_group)
        regular_user.save()

        # Create tags
        for tag in tags_list:
            Tag.objects.get_or_create(name=tag)

        # Create articles and nested comments
        for i in range(4):
            author_id = i + 1 if i < 2 else 2
            authorProfile, _ = UserProfile.objects.get_or_create(id=author_id)

            article, _ = Article.objects.get_or_create(
                author=authorProfile,
                title=article_data[i]['title'],
                content=article_data[i]['content'],
                status=status_list[i]
            )
            article.tags.add(*article_tags[i])
            article.save()

            for j in range(3):
                userProfile = regular_user if j % 2 == 0 else moderator_user

                # top-level comment
                comment, _ = Comment.objects.get_or_create(
                    author=userProfile.userprofile,
                    article=article,
                    content=f"Comment {j + 1} on article {i + 1}",
                    status='publish'
                )
                comment.save()

                # Create 2-5 replies for each comment
                for reply_index in range(2, 6):
                    reply, _ = Comment.objects.get_or_create(
                        author=moderator_user.userprofile if reply_index % 2 == 0 else regular_user.userprofile,
                        article=article,
                        content=f"Reply {reply_index} to Comment {j + 1} on article {i + 1}",
                        reply_to=comment,
                        status='publish'
                    )
                    reply.save()

                    if reply_index == 2:
                        nested_reply, _ = Comment.objects.get_or_create(
                            author=moderator_user.userprofile,
                            article=article,
                            content=f"Nested reply to Reply {reply_index} on Comment {j + 1} Article {i + 1}",
                            reply_to=reply,
                            status='publish'
                        )
                        nested_reply.save()

        # Article & Comment Likes
        users = UserProfile.objects.all()
        for user in users:
            for article in Article.objects.all():
                if not ArticleLike.objects.filter(user=user, article=article).exists():
                    ArticleLike.objects.create(
                        user=user,
                        article=article,
                        status=choice(['like', 'dislike'])
                    )
            for comment in Comment.objects.all():
                if not CommentLike.objects.filter(user=user, comment=comment).exists():
                    CommentLike.objects.create(
                        user=user,
                        comment=comment,
                        status=choice(['like', 'dislike'])
                    )

        self.stdout.write(self.style.SUCCESS(
            'Seeding Completed Successfully.'))