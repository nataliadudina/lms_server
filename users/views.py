from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        password = self.request.data.get('password')
        if password:
            user.set_password(password)
            user.save()

    def perform_update(self, serializer):
        user = serializer.save()
        password = self.request.data.get('password')
        if password:
            user.set_password(password)
            user.save()


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # Бэкенд для обработки фильтра
    filterset_fields = ('course', 'lesson', 'method')  # Набор полей для фильтрации
    ordering_fields = ('date',)
    queryset = Payment.objects.all()
    # permission_classes = [IsAuthenticated]
    # lookup_field = 'username'  # Поле, которое будет использоваться для поиска пользователя
    #
    # def get_queryset(self):
    #     return User.objects.filter(username=self.request.user.username)


class UserPaymentsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
