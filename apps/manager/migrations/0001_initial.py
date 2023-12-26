# Generated by Django 4.2.6 on 2023-12-26 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Absent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeTable', models.CharField(choices=[('Matutino', 'Matutino'), ('Vespertino', 'Vespertino'), ('Noturno', 'Noturno')], max_length=15)),
                ('absentClass', models.CharField(blank=True, max_length=15)),
                ('absentDate', models.DateField(help_text='Insira uma data de ausência')),
            ],
        ),
        migrations.CreateModel(
            name='categoryCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('periods', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeTable', models.CharField(choices=[('Matutino', 'Matutino'), ('Vespertino', 'Vespertino'), ('Noturno', 'Noturno')], max_length=15)),
                ('period', models.IntegerField()),
                ('acronym', models.CharField(error_messages={'unique': 'Já existe uma turma com está abreviação'}, max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='dayClasses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeTable', models.CharField(max_length=15)),
                ('dayWeek', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('acronym', models.CharField(error_messages={'unique': 'Já existe uma disciplina com está abreviação'}, max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numberAbsents', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
    ]
