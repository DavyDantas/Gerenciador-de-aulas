# Generated by Django 4.2.6 on 2023-10-22 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0002_categorycourse_alter_teacher_imgprofile_class"),
    ]

    operations = [
        migrations.AddField(
            model_name="teacher",
            name="matriculation",
            field=models.IntegerField(default=110, verbose_name="Matricula"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="teacher",
            name="name",
            field=models.CharField(max_length=200, verbose_name="Nome"),
        ),
        migrations.CreateModel(
            name="Subject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("acronym", models.CharField(max_length=10)),
                ("teacher", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="manager.teacher")),
            ],
        ),
    ]
