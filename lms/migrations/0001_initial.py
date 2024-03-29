# Generated by Django 4.2.7 on 2024-02-07 13:28

from django.db import migrations, models
import lms.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Course')),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=lms.models.course_upload_to)),
            ],
            options={
                'verbose_name': 'course',
                'verbose_name_plural': 'courses',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Lesson')),
                ('description', models.TextField(blank=True, null=True)),
                ('preview', models.ImageField(blank=True, null=True, upload_to='images/lessons/')),
                ('video', models.FileField(blank=True, null=True, upload_to=lms.models.lesson_upload_to)),
            ],
            options={
                'verbose_name': 'lesson',
                'verbose_name_plural': 'lessons',
            },
        ),
    ]
