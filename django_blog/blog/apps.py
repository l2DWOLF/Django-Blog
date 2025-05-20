from django.apps import AppConfig
from django.dispatch import receiver
from django.db.models.signals import post_save


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    @receiver(post_save, sender='auth.User')
    def perform_new_user_group_profile(sender, instance, created, **kwargs):
        from django.contrib.auth.models import Group, User
        from rest_framework.authtoken.models import Token
        from blog.models import UserProfile

        if not created:
            return
        group, _ = Group.objects.get_or_create(name='users')
        instance.groups.add(group)
        instance.save()
        UserProfile.objects.get_or_create(user=instance, bio=f"{instance.username}'s bio coming soon...")
        Token.objects.get_or_create(user=instance)
        print(f'User {instance.username} added to {group.name} group') 
