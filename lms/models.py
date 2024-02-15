from django.db import models


def course_upload_to(instance, filename):
    course_name = instance.name
    course_name = course_name.replace(' ', '_').lower()
    return f'courses/{course_name}/{filename}'


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Course')
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=course_upload_to, null=True, blank=True)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'course'
        verbose_name_plural = 'courses'


def lesson_upload_to(instance, filename):
    course_name = instance.course.name.replace(' ', '_').lower()
    lesson_number = instance.id
    return f'courses/{course_name}/lessons/{lesson_number}/{filename}'


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='Lesson')
    description = models.TextField(null=True, blank=True)
    preview = models.ImageField(upload_to=lesson_upload_to, null=True, blank=True)
    video = models.URLField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lesson')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'lesson'
        verbose_name_plural = 'lessons'

