from rest_framework.exceptions import ValidationError


def validate_video_url(value):
    """
    Функция валидации URL-адреса видео.
    Проверяет, что URL-адрес ведет только на youtube.com.
    """
    if 'youtube.com' not in value or '/watch?v=' not in value:
        raise ValidationError("Only YouTube video links are allowed.")
