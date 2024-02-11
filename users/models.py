from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    """
      Custom User model that extends Django's built-in AbstractUser model.
      """
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='users/', blank=True, null=True, verbose_name='Avatar')
    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name='Phone number')
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name='Country')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    date = models.DateTimeField(null=True, blank=True, verbose_name='Payment date')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='payments',
                               verbose_name='Paid course')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True, related_name='payments',
                               verbose_name='Paid lesson')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), null=True, blank=True,
                                 verbose_name='Payment amount')

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('transfer', 'Bank transfer'),
    ]
    method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name='Payment method')

    def __str__(self):
        course_or_lesson = self.course.name if self.course else self.lesson.name if self.lesson else "N/A"
        return f"{self.user} - {course_or_lesson} - {self.date} - {self.amount}"

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
