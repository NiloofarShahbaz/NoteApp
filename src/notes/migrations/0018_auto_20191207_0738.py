# Generated by Django 2.2.7 on 2019-12-07 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0017_auto_20191205_1803'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notesetting',
            old_name='is_archive',
            new_name='is_archived',
        ),
    ]
