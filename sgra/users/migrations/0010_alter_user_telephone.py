# Generated by Django 4.2.6 on 2023-12-28 01:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0009_alter_user_telephone_alter_user_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="telephone",
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
