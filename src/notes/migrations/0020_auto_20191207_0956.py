# Generated by Django 2.2.7 on 2019-12-07 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0019_auto_20191207_0947'),
    ]

    operations = [
        migrations.RenameField(
            model_name='settinglabel',
            old_name='settings',
            new_name='setting',
        ),
    ]