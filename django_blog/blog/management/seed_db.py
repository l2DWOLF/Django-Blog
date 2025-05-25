from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import *

class Command(BaseCommand):
    help = 'Seed the database with initial data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding The Database...'))
        pass
