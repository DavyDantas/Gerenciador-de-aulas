# Generated by Django 4.2.6 on 2023-10-25 10:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0002_categorycourse_class_teacher_matriculation_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="teacher",
            name="telefone",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
