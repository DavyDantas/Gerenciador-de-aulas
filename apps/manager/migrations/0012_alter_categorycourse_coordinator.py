# Generated by Django 4.2.6 on 2023-11-05 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0011_alter_categorycourse_coordinator_alter_class_acronym_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="categorycourse",
            name="coordinator",
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to="manager.teacher"),
        ),
    ]
