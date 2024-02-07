from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from lms.apps import LmsConfig
from lms.views import CourseViewSet, LessonCreateApiView, LessonListApiView, LessonDetailApiView, LessonUpdateApiView, \
    LessonDestroyApiView

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
                  path('lessons/create/', LessonCreateApiView.as_view(), name='create-lesson'),
                  path('lessons/', LessonListApiView.as_view(), name='lessons-list'),
                  path('lessons/<int:pk>/', LessonDetailApiView.as_view(), name='lesson'),
                  path('lessons/<int:pk>/edit/', LessonUpdateApiView.as_view(), name='update-lesson'),
                  path('lessons/<int:pk>/delete/', LessonDestroyApiView.as_view(), name='delete-lesson')
              ] + router.urls
