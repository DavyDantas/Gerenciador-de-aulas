# Generated by Django 4.2.6 on 2023-11-16 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0022_rename_imgprofilev_teacher_imgprofilevariable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='manager.teacher'),
        ),
    ]
