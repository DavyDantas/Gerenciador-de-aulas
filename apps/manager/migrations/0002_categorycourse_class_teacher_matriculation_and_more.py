# Generated by Django 4.2.6 on 2023-10-25 01:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="categoryCourse",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("periods", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Class",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "timeTable",
                    models.CharField(
                        choices=[("Matutino", "Matutino"), ("Vespertino", "Vespertino"), ("Noturno", "Noturno")],
                        max_length=15,
                    ),
                ),
                ("period", models.IntegerField()),
                ("acronym", models.CharField(max_length=10)),
                (
                    "course",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="manager.categorycourse"),
                ),
            ],
        ),
        migrations.AddField(
            model_name="teacher",
            name="matriculation",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="teacher",
            name="imgProfile",
            field=models.ImageField(default="user-profile-icon.jpg", upload_to="UsersProfile/"),
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
        migrations.CreateModel(
            name="dayClasses",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("day", models.CharField(max_length=50)),
                ("classObj", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="manager.class")),
                (
                    "fifth",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="fifth",
                        to="manager.subject",
                    ),
                ),
                (
                    "first",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="first",
                        to="manager.subject",
                    ),
                ),
                (
                    "fourth",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="fourth",
                        to="manager.subject",
                    ),
                ),
                (
                    "second",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="second",
                        to="manager.subject",
                    ),
                ),
                (
                    "sixth",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="sixth",
                        to="manager.subject",
                    ),
                ),
                (
                    "third",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="third",
                        to="manager.subject",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="categorycourse",
            name="coordinator",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="manager.teacher"),
        ),
    ]
