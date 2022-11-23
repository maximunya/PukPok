# Generated by Django 4.1.2 on 2022-11-22 14:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PP', '0023_notification_edit_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='black_list',
            field=models.ManyToManyField(blank=True, related_name='black_list', to=settings.AUTH_USER_MODEL),
        ),
    ]
