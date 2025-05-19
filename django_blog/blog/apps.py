from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    @receiver(post_save, sender='auth.User')
    def perform_add_user_to_users_group(sender, instance, created, **kwargs):
        from django.contrib.auth.models import Group, User

        if not created:
            return
        group, _ = Group.objects.get_or_create(name='users')
        instance.groups.add(group)
        instance.save()
        print(f'User {instance.username} added to {group.name} group') 
