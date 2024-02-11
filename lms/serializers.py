from rest_framework import serializers

from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = (
            'name',
            'description',
            'preview',
            'video',
        )


class CourseSerializer(serializers.ModelSerializer):
    number_of_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson', many=True)

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
