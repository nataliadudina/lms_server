from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .apps import UsersConfig
from .views import PaymentListView, UserApiList, UserDetailApiList, \
    UserUpdateApiList, UserDestroyApiView, UserRegistrationAPIView, SubscriptionAPIView, CreatePaymentView, \
    PaymentStatusView

app_name = UsersConfig.name

urlpatterns = [
    path('users/', UserApiList.as_view(), name='user-get'),
    path('register/', UserRegistrationAPIView.as_view(), name='user-post'),
    path('users/<int:pk>/profile/', UserDetailApiList.as_view(), name='profile'),
    path('users/<int:pk>/edit/', UserUpdateApiList.as_view(), name='profile-put-patch'),
    path('users/<int:pk>/delete/', UserDestroyApiView.as_view(), name='user-destroy'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # payments
    path('users/payments/', PaymentListView.as_view(), name='payments-history'),
    path('new_payment/', CreatePaymentView.as_view(), name='payment'),    # method POST
    path('payment-status/', PaymentStatusView.as_view(), name='payment_status'),

    # subscriptions
    path('users/subscriptions/', SubscriptionAPIView.as_view(), name='subscriptions'),  # method POST
]
