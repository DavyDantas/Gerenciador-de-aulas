# Generated by Django 4.2.6 on 2023-10-28 18:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0004_teacher_numberabsents"),
    ]

    operations = [
        migrations.AlterField(
            model_name="class",
            name="timeTable",
            field=models.CharField(max_length=15),
        ),
    ]
