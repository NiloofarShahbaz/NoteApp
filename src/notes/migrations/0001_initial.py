# Generated by Django 2.2.7 on 2019-11-11 18:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=150)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=950, null=True)),
                ('archive', models.BooleanField(default=False)),
                ('pin', models.BooleanField(default=False)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('new', models.BooleanField(default=False)),
                ('color', models.CharField(choices=[('W', 'White'), ('R', 'Red'), ('B', 'Blue'), ('G', 'Green'), ('Y', 'Yellow'), ('P', 'Pink'), ('V', 'Violet')], default='W', max_length=1)),
                ('label', models.ManyToManyField(blank=True, to='notes.Label')),
            ],
        ),
        migrations.CreateModel(
            name='Trash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delete_time', models.DateTimeField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_and_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('repeat', models.CharField(choices=[('N', 'Does Not Repeat'), ('D', 'Daily'), ('W', 'Weekly'), ('M', 'Monthly'), ('Y', 'Yearly')], default='N', max_length=1)),
                ('note', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='notes.Note')),
            ],
        ),
        migrations.AddField(
            model_name='note',
            name='trash',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='notes.Trash'),
        ),
        migrations.AddField(
            model_name='note',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('N', 'Is Not A Checklist'), ('T', 'Done'), ('F', 'Not Done')], default='N', max_length=1)),
                ('text', models.CharField(max_length=950)),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.Note')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='note_images')),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.Note')),
            ],
        ),
    ]