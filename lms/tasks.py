from celery import shared_task
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from lms.models import Course
from users.models import Subscription, User


@shared_task
def send_notification(course_id):
    """Отправка уведомлений об обновлении курса подписчикам"""
    # Получаем курс по ID
    course = Course.objects.get(pk=course_id)
    # Получаем список подписчиков
    subscribers = Subscription.objects.filter(course=course)
    # Получаем список адресов электронной почты подписчиков
    subscribers_list = [subscriber.user.email for subscriber in subscribers]

    for subscriber in subscribers_list:
        try:
            message = f'We are thrilled to announce an update to {course.name}. Check it now!'
            subject = 'Course Update - Unlock New Levels of Learning!'
            print(
                f"Sending email to {subscriber}:\nSubject: {subject}\nMessage: {message}")
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscriber]
            )
        except Exception as e:
            print(f"Failed to send email to {subscriber}: {e}")


def check_user_last_login():
    """Блокирование пользователей, которые не заходили на сайт больше месяца"""
    now = timezone.now()
    month_ago = now - relativedelta(months=1)

    User.objects.filter(is_active=True, last_login__lte=month_ago).update(is_active=False)
