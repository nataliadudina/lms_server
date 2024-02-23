from rest_framework import serializers, request

from lms.models import Course, Lesson
from lms.validators import validate_video_url


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и отображения уроков"""
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    video = serializers.URLField(required=False, validators=[validate_video_url])

    class Meta:
        model = Lesson
        fields = (
            'id',
            'name',
            'description',
            'preview',
            'video',
            'course'
        )


class SimpleLessonSerializer(serializers.ModelSerializer):
    """Выводит краткую информацию об уроке"""
    class Meta:
        model = Lesson
        fields = (
            'name',
            'description',
        )


class LessonDetailSerializer(serializers.ModelSerializer):
    """Выводит полную информацию об уроке"""
    course = serializers.StringRelatedField()

    class Meta:
        model = Lesson
        fields = (
            'id',
            'name',
            'description',
            'preview',
            'video',
            'course'
        )


class CourseSerializer(serializers.ModelSerializer):
    """Выводит информацию о курсе, количество и список уроков с краткой информацией"""
    number_of_lessons = serializers.SerializerMethodField()
    lessons = SimpleLessonSerializer(source='lesson', many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.email')
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'name',
            'description',
            'image',
            'number_of_lessons',
            'lessons',
            'author',
            'subscription'
        )

    def get_number_of_lessons(self, instance):
        return instance.lesson.count()

    def create(self, validated_data):
        # При создании нового курса устанавливает текущего пользователя в качестве автора
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

    def get_subscription(self, instance):
        user = self.context['request'].user   # Получает текущего пользователя
        is_subscribed = instance.subscribers.filter(user=user).exists()    # Проверяет, подписан ли пользователь на курс
        return is_subscribed
