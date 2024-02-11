from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LessonApiList(generics.ListCreateAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        course_id = self.kwargs['pk']
        course = get_object_or_404(Course, pk=course_id)
        queryset = Lesson.objects.filter(course=course)
        return queryset


# class LessonCreateApiView(generics.CreateAPIView):
#     serializer_class = LessonSerializer
#
#
# class LessonListApiView(generics.ListAPIView):
#     serializer_class = LessonSerializer
#     queryset = Lesson.objects.all()


class LessonDetailApiView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateApiView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyApiView(generics.DestroyAPIView):
    serializer_class = LessonSerializer

