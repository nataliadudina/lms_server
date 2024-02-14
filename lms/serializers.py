from rest_framework import serializers

from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField(read_only=True)

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
    class Meta:
        model = Lesson
        fields = (
            'name',
            'description',
        )


class CourseSerializer(serializers.ModelSerializer):
    number_of_lessons = serializers.SerializerMethodField()
    lessons = SimpleLessonSerializer(source='lesson', many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            'name',
            'description',
            'image',
            'number_of_lessons',
            'lessons',
        )

    def get_number_of_lessons(self, instance):
        return instance.lesson.count()
