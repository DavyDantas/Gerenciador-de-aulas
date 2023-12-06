# Generated by Django 4.2.6 on 2023-10-23 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0007_alter_class_period"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dayclasses",
            name="fifth",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="fifth",
                to="manager.subject",
            ),
        ),
        migrations.AlterField(
            model_name="dayclasses",
            name="first",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="first",
                to="manager.subject",
            ),
        ),
        migrations.AlterField(
            model_name="dayclasses",
            name="fourth",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="fourth",
                to="manager.subject",
            ),
        ),
        migrations.AlterField(
            model_name="dayclasses",
            name="second",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="second",
                to="manager.subject",
            ),
        ),
        migrations.AlterField(
            model_name="dayclasses",
            name="sixth",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="sixth",
                to="manager.subject",
            ),
        ),
        migrations.AlterField(
            model_name="dayclasses",
            name="third",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="third",
                to="manager.subject",
            ),
        ),
    ]
