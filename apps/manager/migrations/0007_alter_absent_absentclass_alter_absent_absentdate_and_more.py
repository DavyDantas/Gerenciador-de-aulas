# Generated by Django 4.2.6 on 2023-12-25 17:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("manager", "0006_alter_absent_absentclass"),
    ]

    operations = [
        migrations.AlterField(
            model_name="absent",
            name="absentClass",
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name="absent",
            name="absentDate",
            field=models.DateField(help_text="Insira uma data de ausência"),
        ),
        migrations.CreateModel(
            name="Manager",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "user",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
    ]
