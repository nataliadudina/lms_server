# Lms Server

SPA веб-приложение Lms Server - LMS-система, в которой каждый желающий может размещать свои полезные материалы или курсы.
Информация доступна только авторизованным пользователям. Редактировать уроки и курсы может только автор и модератор сервиса.
Авторизованные пользователи имеют возможность оплатить понравившийся курс или отдельный урок, а также оформить подписку - 
им будет приходить уведомление на почту об обновлениях выбранного курса.

### Технологии

- **Django**
- **Python**
- **PostgreSQL**
- **Django REST Framework**
- **Django REST Framework SimpleJWT**
- **Django CORS Headers**
- **drf-yasg**
- **Celery**
- **Redis**
- **django-celery-beat**


###  Предварительная установка

+ Установленный Docker
+ Установленный Docker Compose


###  Установка и использование

+ Клонируйте репозиторий: git@github.com:nataliadudina/lms_server.git
+ Перейдите в каталог проекта: cd lms_server
+ Создайте файл .env в корневой директории проекта и добавьте в него необходимые переменные окружения. Пример содержимого файла `.env` есть в файле `.env.sample`
+ Соберите и запустите контейнеры: docker-compose up --build
+ После успешного запуска контейнеров приложение будет доступно по адресу http://localhost:8000.
+ Чтобы остановить и удалить контейнеры, выполните: docker-compose down

---

### Структура проекта

    Проект "Lms Server" состоит из двух приложений:
    1) lms: модели Course, Lesson
    2) users: модель User, Payment, Subscription
---

### Дополнительная информация

    Django: Веб-фреймворк, используемый для создания веб-приложения.
    PostgreSQL: Система управления базами данных, используемая для хранения данных приложения.
    Redis: Используется как брокер сообщений для Celery.
    Celery: Фреймворк для асинхронной обработки задач.
    Poetry: Инструмент для управления зависимостями Python.
