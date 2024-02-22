from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

from lms.models import Course
from users.models import Subscription


class SubscriptionTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()  # имитирует запросы от клиента
        # Создание пользователя и его авторизация
        self.user = get_user_model().objects.create(email='user@example.com', password='password')
        self.client.force_authenticate(user=self.user)

        # Создание тестового курса
        self.course = Course.objects.create(name='Test Course', description='Test Course Description', author=self.user)

        # Получение URL для подписки на курс
        self.url = reverse('users:subscriptions', kwargs={'pk': self.user.id})

    def test_subscribe_and_unsubscribe(self):
        # Подписка на курс
        response = self.client.post(self.url, {'course_id': self.course.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         f'You have been successfully subscribed to {self.course.name} updates.')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # Отписка от курса
        response = self.client.post(self.url, {'course_id': self.course.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         f'You have successfully unsubscribed from {self.course.name} updates.')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
