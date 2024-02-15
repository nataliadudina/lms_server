from django.urls import path
from rest_framework.routers import DefaultRouter
from lms.apps import LmsConfig
from lms.views import CourseViewSet, LessonApiList, LessonDetailApiView, LessonUpdateApiView, LessonDestroyApiView

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
                  path('courses/lessons/', LessonApiList.as_view(), name='lesson-list-create'),
                  path('courses/lessons/<int:pk>/', LessonDetailApiView.as_view(), name='lesson'),
                  path('courses/lessons/<int:pk>/edit/', LessonUpdateApiView.as_view(), name='lesson-update'),
                  path('courses/lessons/<int:pk>/delete/', LessonDestroyApiView.as_view(), name='lesson-delete')
              ] + router.urls
