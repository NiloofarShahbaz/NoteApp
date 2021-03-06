# Generated by Django 2.2.7 on 2019-12-02 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0008_auto_20191130_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoteContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('N', 'Is Not A Checklist'), ('T', 'Done'), ('F', 'Not Done')], default='N', max_length=1)),
                ('text', models.CharField(max_length=950)),
            ],
            options={
                'ordering': ('order', 'pk'),
            },
        ),
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ('order', 'pk')},
        ),
        migrations.RenameField(
            model_name='note',
            old_name='archive',
            new_name='is_archive',
        ),
        migrations.RenameField(
            model_name='note',
            old_name='new',
            new_name='is_pin',
        ),
        migrations.RemoveField(
            model_name='note',
            name='pin',
        ),
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.AddField(
            model_name='notecontent',
            name='note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.Note'),
        ),
    ]
