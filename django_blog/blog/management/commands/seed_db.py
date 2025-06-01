from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from taggit.models import Tag
from blog.models import *
from blog.management.commands.seeding_tools import *
from blog.management.commands.group_models_permissions import mods_group_permissions, users_group_permissions


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
        admin_user.set_password('Admin123!')
        admin_user.save()
# create moderator
        moderator_user, created = User.objects.get_or_create(username='moderator', defaults=moderator_defaults)
        moderator_user.set_password('Mod123!')
        moderator_user.groups.add(mods_group)
        moderator_user.save()
# create user
        regular_user, created = User.objects.get_or_create(
            username='blog_user', defaults=user_defaults)
        regular_user.set_password('User123!')
        regular_user.save()
# create tags
        for tag in tags_list:
            Tag.objects.get_or_create(name=tag)
# create articles

# create comments & nested comments

# create article likes, dislikes. 

# create comment likes, dislikes. 


        self.stdout.write(self.style.SUCCESS('Seeding Completed Successfully...'))
