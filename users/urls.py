from django.urls import path
from rest_framework.routers import DefaultRouter

from .apps import UsersConfig
from .views import UserViewSet, PaymentListView, UserPaymentsView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('users/payments/', PaymentListView.as_view(), name='payments-history'),
    path('users/<int:pk>/payments/', UserPaymentsView.as_view(), name='user-payments'),
] + router.urls
