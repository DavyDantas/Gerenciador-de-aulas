# Generated by Django 4.2.6 on 2023-10-22 19:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0003_teacher_matriculation_alter_teacher_name_subject"),
    ]

    operations = [
        migrations.AlterField(
            model_name="teacher",
            name="matriculation",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="name",
            field=models.CharField(max_length=200),
        ),
    ]
