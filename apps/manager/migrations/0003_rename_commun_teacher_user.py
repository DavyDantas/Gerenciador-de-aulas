# Generated by Django 4.2.6 on 2023-12-24 18:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0002_alter_absent_absentclass"),
    ]

    operations = [
        migrations.RenameField(
            model_name="teacher",
            old_name="commun",
            new_name="user",
        ),
    ]
