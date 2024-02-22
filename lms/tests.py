from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase, APIClient

from lms.models import Course, Lesson
from users.models import Subscription


class CourseTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create(email='user@example.com', password='password')
        self.client.force_authenticate(user=self.user)

    def test_create_course(self):
        """ Тестирование создания курса """
        data = {
            'name': 'Test Course',
            'description': 'description',
        }
        response = self.client.post(  # self.client - экземпляр класса APIClient
            '/courses/',
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response.json(),
            {'name': 'Test Course', 'description': 'description', 'image': None, 'number_of_lessons': 0,
             'lessons': [], 'author': 'user@example.com'}
        )

        self.assertTrue(Course.objects.all().exists())


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()   # имитирует запросы от клиента
        # Создание пользователя и его авторизация
        self.user = get_user_model().objects.create(email='user@example.com', password='password')
        self.client.force_authenticate(user=self.user)

        # Создание модератора
        self.moderator = get_user_model().objects.create(email='moderator@example.com', password='password')
        moderator_group = Group.objects.create(name='moderators')
        self.moderator.groups.add(moderator_group)

        # Создание тестового курса
        self.course = Course.objects.create(name='Test Course', description='Test Course Description', author=self.user)

        # Создание тестовых уроков
        self.lesson1 = Lesson.objects.create(name='Lesson 1', description='Description 1', course=self.course)
        self.lesson2 = Lesson.objects.create(name='Lesson 2', description='Description 2', course=self.course)

    def test_create_lesson(self):
        """Тестирование создания урока"""
        # Подготовка данных для создания урока
        lesson_data = {
            'name': 'Test Lesson',
            'description': 'Test Lesson Description',
            'course': self.course.id,  # Используем ID созданного курса
        }
        # Отправление POST-запроса на создание урока
        response = self.client.post(reverse('lms:lesson-list-create'), data=lesson_data)

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверка, что в ответе присутствует созданный урок
        self.assertEqual(response.data['name'], lesson_data['name'])
        self.assertEqual(response.data['description'], lesson_data['description'])
        self.assertEqual(response.data['course'], self.course.id)

    def test_moderator_cannot_create_lessons(self):
        """Тестирование, что модератор не может создать уроки"""

        # Подготовка данных для создания урока
        lesson_data = {
            'name': 'Test Lesson by Moderator',
            'description': 'Test Lesson Description by Moderator',
            'course': self.course.id,
        }
        # Переключение на модератора
        self.client.force_authenticate(user=self.moderator)

        # Отправление POST-запроса на создание урока модератором
        response = self.client.post(reverse('lms:lesson-list-create'), data=lesson_data)

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_lesson(self):
        """ Вывод списка уроков """

        response = self.client.get(reverse('lms:lesson-list-create'))

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка, что в ответе присутствуют ожидаемые данные
        self.assertEqual(len(response.data['results']),  2)

        # Проверка наличия ожидаемых уроков в списке
        lesson_names = [lesson['name'] for lesson in response.data['results']]
        self.assertIn('Lesson 1', lesson_names)
        self.assertIn('Lesson 2', lesson_names)

    def test_update_lesson(self):
        """Тестирование редактирования урока"""

        self.lesson = Lesson.objects.create(
            name='Test Lesson',
            description='Test Lesson Description',
            course=self.course,
        )

        lesson_data = {
            'name': 'New Lesson'
        }
        # Отправка PATCH-запроса на создание урока
        response = self.client.patch(reverse('lms:lesson-update', kwargs={'pk': self.lesson.pk}), data=lesson_data)

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка, что имя урока было обновлено
        self.assertEqual(response.data['name'], lesson_data['name'])

    def test_read_lesson(self):
        """Тестирование просмотра урока"""
        response = self.client.get(reverse('lms:lesson', kwargs={'pk': self.lesson2.id}))

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка, что возвращаемый JSON содержит ожидаемые данные
        self.assertEqual(response.data['name'], 'Lesson 2')
        self.assertEqual(response.data['description'], 'Description 2')

    def test_delete_lesson(self):
        """Тестирование удаления урока"""
        # Получение URL для удаления урока
        url = reverse('lms:lesson-delete', kwargs={'pk': self.lesson1.id})

        # Отправка DELETE-запроса на удаление урока
        response = self.client.delete(url)

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверка, что урок был удален
        with self.assertRaises(Lesson.DoesNotExist):
            Lesson.objects.get(id=self.lesson1.id)

    def test_moderator_cannot_delete_lessons(self):
        """Тестирование, что модератор не может удалять уроки"""

        # Переключение на модератора
        self.client.force_authenticate(user=self.moderator)

        # Отправка POST-запросаа на создание урока модератором
        response = self.client.delete(reverse('lms:lesson-delete', kwargs={'pk': self.lesson1.id}))

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_youtube_url_validation(self):
        """Тестирование валидации YouTube URL при создании урока"""
        # Действительный YouTube URL
        valid_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        # Недействительный YouTube URL
        invalid_url = "https://www.example.com/"

        # Создание урока с действительным YouTube URL
        lesson_data = {
            'name': 'Valid YouTube URL Lesson',
            'video': valid_url,
            'course': self.course.id,
        }
        valid_response = self.client.post(reverse('lms:lesson-list-create'), data=lesson_data)
        self.assertEqual(valid_response.status_code, status.HTTP_201_CREATED)

        # Создание урока с недействительным YouTube URL
        lesson_data = {
            'name': 'Valid YouTube URL Lesson',
            'video': invalid_url,
            'course': self.course.id,
        }
        invalid_response = self.client.post(reverse('lms:lesson-list-create'), data=lesson_data)
        self.assertEqual(invalid_response.status_code, status.HTTP_400_BAD_REQUEST)
