from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.paginators import CoursePaginator, LessonPaginator
from lms.serializers import CourseSerializer, LessonSerializer, LessonDetailSerializer
from lms.permissions import IsModerator, IsProductAuthor
from lms.tasks import send_notification


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator
    permission_classes_by_action = {
        'create': [IsAuthenticated, IsModerator],
        'update': [IsAuthenticated, IsProductAuthor | IsModerator],
        'partial_update': [IsAuthenticated, IsProductAuthor | IsModerator],
        'destroy': [IsAuthenticated, IsProductAuthor],
        'list': [IsAuthenticated]
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        course_updated = serializer.save(author=self.request.user)
        if course_updated:
            send_notification.delay(course_updated.pk)


class LessonApiList(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonPaginator
    permission_classes = [IsAuthenticated, IsModerator]


class LessonDetailApiView(generics.RetrieveAPIView):
    serializer_class = LessonDetailSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonUpdateApiView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsProductAuthor | IsModerator]


class LessonDestroyApiView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsProductAuthor]
