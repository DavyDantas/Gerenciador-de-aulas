# Generated by Django 4.2.6 on 2023-12-24 18:24

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="absent",
            name="absentClass",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[("1", "1º"), ("2", "2º"), ("3", "3º"), ("4", "4º"), ("5", "5º"), ("6", "6º")],
                    max_length=15,
                ),
                size=None,
            ),
        ),
    ]
