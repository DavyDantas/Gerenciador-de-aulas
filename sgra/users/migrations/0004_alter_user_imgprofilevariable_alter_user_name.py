# Generated by Django 4.2.6 on 2023-12-24 21:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_user_telephone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="imgProfileVariable",
            field=models.ImageField(blank=True, default="user-profile-icon.jpg", upload_to="UsersProfile/"),
        ),
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(max_length=255, verbose_name="Name of User"),
        ),
    ]
