# Generated by Django 2.2.7 on 2019-11-30 10:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0006_auto_20191130_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='collaborators',
            field=models.ManyToManyField(blank=True, null=True, related_name='collaborating_notes', to=settings.AUTH_USER_MODEL),
        ),
    ]
