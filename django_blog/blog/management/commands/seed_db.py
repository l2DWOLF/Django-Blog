from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from taggit.models import Tag
from blog.models import *
from blog.management.commands.seeding_tools import *
from blog.management.commands.group_models_permissions import get_mods_group_permissions, get_users_group_permissions
from random import choice, randint, random
import json
from pathlib import Path



class Command(BaseCommand):
    help = 'Seed the database with initial data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding The Database...'))

        # Create groups and assign permissions
        mods_group, _ = Group.objects.get_or_create(name='moderators')
        mods_group.permissions.set(get_mods_group_permissions())

        users_group, _ = Group.objects.get_or_create(name='users')
        users_group.permissions.set(get_users_group_permissions())

        # Create main users
        admin_user, _ = CustomUser.objects.get_or_create(
            username='admin', defaults=admin_defaults)
        admin_user.set_password('AdminUser1234!')
        admin_user.save()

        moderator_user, _ = CustomUser.objects.get_or_create(
            username='moderator', defaults=moderator_defaults)
        moderator_user.set_password('ModUser1234!')
        moderator_user.groups.add(mods_group)
        moderator_user.save()

        regular_user, _ = CustomUser.objects.get_or_create(
            username='blog_user', defaults=user_defaults)
        regular_user.set_password('UserUser1234!')
        regular_user.groups.add(users_group)
        regular_user.save()

        # Create additional users
        for i in range(50):
            user, created = CustomUser.objects.get_or_create(
                username=f'user_{i}', defaults={
                    'email': f'user_{i}@user.com',
                })
            if created:
                user.set_password('TestUser123!')
                user.groups.add(users_group)
                user.save()

        # Create tags
        for tag in tags_list:
            Tag.objects.get_or_create(name=tag)

        # Create articles and nested comments

        article_seed_path = Path(__file__).resolve(
        ).parent.parent / "seed_data" / "article_seed_data.json"
        with open(article_seed_path, 'r', encoding='utf-8') as f:
            article_data = json.load(f)

        for i, article_info in enumerate(article_data):
            author_id = i + 1 if i < 2 else 2  # First two authored by id 1 & 2, rest by id 2
            authorProfile, _ = UserProfile.objects.get_or_create(id=author_id)

            article, _ = Article.objects.get_or_create(
                author=authorProfile,
                title=article_info['title'],
                defaults={
                    'content': article_info['content'],
                    'status': article_info.get('status', 'publish'),
                }
            )
            article.tags.set(article_info['tags'])  # Overwrites existing tags
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

                for reply_index in range(2, 6):
                    reply, _ = Comment.objects.get_or_create(
                        author=moderator_user.userprofile if reply_index % 2 == 0 else regular_user.userprofile,
                        article=article,
                        content=f"Reply {reply_index} to Comment {j + 1} on article {i + 1}",
                        reply_to=comment,
                        status='publish'
                    )

                    if reply_index == 2:
                        Comment.objects.get_or_create(
                            author=moderator_user.userprofile,
                            article=article,
                            content=f"Nested reply to Reply {reply_index} on Comment {j + 1} Article {i + 1}",
                            reply_to=reply,
                            status='publish'
                        )

        users = list(CustomUser.objects.select_related('userprofile'))
        articles = Article.objects.all()
        comments = Comment.objects.all()

        # Article Likes/Dislikes
        for article in articles:
            num_likes = randint(10, 40)
            num_dislikes = max(1, int(num_likes * randint(1, 5) / 100))

            total_voters = set()

            # Add likes
            while len(total_voters) < num_likes:
                user = choice(users)
                if user.id in total_voters:
                    continue
                total_voters.add(user.id)
                ArticleLike.objects.update_or_create(
                    user=user.userprofile,
                    article=article,
                    defaults={'status': 'like'}
                )

            # Add dislikes
            dislike_count = 0
            while dislike_count < num_dislikes:
                user = choice(users)
                if user.id in total_voters:
                    continue
                total_voters.add(user.id)
                ArticleLike.objects.update_or_create(
                    user=user.userprofile,
                    article=article,
                    defaults={'status': 'dislike'}
                )
                dislike_count += 1

        # Comment Likes/Dislikes
        for comment in comments:
            total_votes = randint(3, 10)
            voted_users = set()

            while len(voted_users) < total_votes and len(voted_users) < len(users):
                user = choice(users)
                if user.id in voted_users:
                    continue
                voted_users.add(user.id)

                status = 'dislike' if random() < 0.20 else 'like'

                CommentLike.objects.update_or_create(
                    user=user.userprofile,
                    comment=comment,
                    defaults={'status': status}
                )

        self.stdout.write(self.style.SUCCESS(
            'Seeding Completed Successfully.'))
