# Generated by Django 5.2.4 on 2025-07-17 09:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='location',
            field=models.TextField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(validators=[django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(10288)]),
        ),
    ]
