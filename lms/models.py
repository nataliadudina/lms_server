from rest_framework import serializers
from django.db import models


def course_upload_to(instance, filename):
    course_name = instance.name  # Получаем название курса
    course_name = course_name.replace(' ', '_').lower()  # Преобразуем название курса в lowercase и заменяем пробелы на подчеркивания
    return f'courses/{course_name}/{filename}'


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Course')
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=course_upload_to, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'course'
        verbose_name_plural = 'courses'


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = (
            'name',
            'description',
            'image',
        )


def lesson_upload_to(instance, filename):
    course_name = instance.course.name  # Получаем название курса
    course_name = course_name.replace(' ', '_').lower()  # Преобразуем название курса в lowercase и заменяем пробелы на подчеркивания
    return f'courses/{course_name}/lessons/{filename}'


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='Lesson')
    description = models.TextField(null=True, blank=True)
    preview = models.ImageField(upload_to='images/lessons/', null=True, blank=True)
    video = models.FileField(upload_to=lesson_upload_to, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'lesson'
        verbose_name_plural = 'lessons'


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = (
            'name',
            'description',
            'preview',
            'video',
        )