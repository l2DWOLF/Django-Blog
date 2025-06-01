from django.db import migrations
from django.core.management import call_command

class Migration(migrations.Migration):

    def run_seed(app, schema_editor):
        call_command('seed_db')


    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(run_seed)
    ]
