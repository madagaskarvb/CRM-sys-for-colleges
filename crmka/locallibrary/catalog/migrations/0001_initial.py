# Generated by Django 5.1.5 on 2025-02-04 13:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EducationalMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('file', models.FileField(blank=True, null=True, upload_to='materials/', verbose_name='Файл')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Учебный материал',
                'verbose_name_plural': 'Учебные материалы',
                'db_table': 'educational_materials',
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название факультета')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание факультета')),
            ],
            options={
                'verbose_name': 'Факультет',
                'verbose_name_plural': 'Факультеты',
                'db_table': 'faculties',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя студента')),
                ('login', models.CharField(max_length=150, unique=True, verbose_name='Логин')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('status', models.CharField(default='Активный', max_length=150, verbose_name='Статус')),
                ('password', models.CharField(max_length=150, verbose_name='Пароль')),
                ('faculty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.faculty', verbose_name='Факультет')),
            ],
            options={
                'verbose_name': 'Студент',
                'verbose_name_plural': 'Студенты',
                'db_table': 'students',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя преподавателя')),
                ('login', models.CharField(max_length=150, unique=True, verbose_name='Логин')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('status', models.CharField(default='Активный', max_length=150, verbose_name='Статус')),
                ('password', models.CharField(max_length=150, verbose_name='Пароль')),
                ('subject', models.CharField(blank=True, max_length=150, null=True, verbose_name='Предмет')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Биография')),
                ('faculty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.faculty', verbose_name='Факультет')),
            ],
            options={
                'verbose_name': 'Преподаватель',
                'verbose_name_plural': 'Преподаватели',
                'db_table': 'teachers',
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Оценка')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата выставления оценки')),
                ('material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.educationalmaterial', verbose_name='Учебный материал')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.student', verbose_name='Студент')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.teacher', verbose_name='Преподаватель')),
            ],
            options={
                'verbose_name': 'Оценка',
                'verbose_name_plural': 'Оценки',
                'db_table': 'grades',
            },
        ),
        migrations.AddField(
            model_name='educationalmaterial',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.teacher', verbose_name='Преподаватель'),
        ),
    ]
