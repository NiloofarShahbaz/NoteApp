# Generated by Django 2.2.7 on 2019-12-03 15:47

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0014_auto_20191203_1358'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='noteconfig',
            unique_together={('user', 'note')},
        ),
    ]
