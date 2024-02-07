from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    # lookup_field = 'username'  # Поле, которое будет использоваться для поиска пользователя (в данном случае, username)
    #
    # def get_queryset(self):
    #     return User.objects.filter(username=self.request.user.username)
