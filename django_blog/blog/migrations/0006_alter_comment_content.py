# Generated by Django 5.2.4 on 2025-07-28 23:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_comment_reply_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(validators=[django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(1028)]),
        ),
    ]
