from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .apps import UsersConfig
from .views import UserViewSet, PaymentListView, UserPaymentsView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
                  # path('users/profiles/', PaymentListView.as_view(), name='profiles'),
                  path('users/payments/', PaymentListView.as_view(), name='payments-history'),
                  path('users/<int:pk>/payments/', UserPaymentsView.as_view(), name='user-payments'),  # ?
                  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ] + router.urls
