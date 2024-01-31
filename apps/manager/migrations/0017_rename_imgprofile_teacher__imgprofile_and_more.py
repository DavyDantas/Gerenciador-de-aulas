# Generated by Django 4.2.6 on 2023-11-15 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0016_rename_day_dayclasses_dayweek'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='imgProfile',
            new_name='_imgProfile',
        ),
        migrations.AlterField(
            model_name='class',
            name='acronym',
            field=models.CharField(error_messages={'unique': 'Já existe uma turma com está abreviação'}, max_length=10, unique=True),
        ),
    ]