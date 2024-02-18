from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from users.models import Payment
from lms.permissions import IsOwnerOrReadOnly, IsModerator
from users.serializers import UserSerializer, PaymentSerializer, UserProfileSerializer


class UserApiList(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated]


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        password = self.request.data.get('password')
        if password:
            user.set_password(password)
            user.save()


class UserDetailApiList(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        user = self.get_object()

        if user == self.request.user:
            return UserProfileSerializer    # просмотр собственного профиля
        else:
            return UserSerializer    # просмотр чужого профиля


class UserUpdateApiList(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        user = serializer.save()
        password = self.request.data.get('password')
        if password:
            user.set_password(password)
            user.save()


class UserDestroyApiView(generics.DestroyAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # Бэкенд для обработки фильтра
    filterset_fields = ('course', 'lesson', 'method')  # Набор полей для фильтрации
    ordering_fields = ('date',)
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated | IsModerator]

    def get_queryset(self):
        # Показывает только платежи пользователя
        if not self.request.user.groups.filter(name='moderators').exists():
            return Payment.objects.filter(user=self.request.user)
        # Для модератора показывает все
        return Payment.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if not queryset.exists():
            return Response({'message': 'No payments to display.'}, status=200)
        return Response(serializer.data)
