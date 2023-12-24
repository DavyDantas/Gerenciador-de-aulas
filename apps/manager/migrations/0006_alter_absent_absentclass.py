# Generated by Django 4.2.6 on 2023-12-24 21:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0005_alter_absent_absentclass"),
    ]

    operations = [
        migrations.AlterField(
            model_name="absent",
            name="absentClass",
            field=models.CharField(
                choices=[("1", "1º"), ("2", "2º"), ("3", "3º"), ("4", "4º"), ("5", "5º"), ("6", "6º")], max_length=15
            ),
        ),
    ]