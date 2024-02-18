from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Просмотр списка всех платежей"""
    # SlugRelatedField выводит строку вместо id
    user = serializers.SlugRelatedField(slug_field="email", read_only=True)
    lesson = serializers.SlugRelatedField(slug_field="name", read_only=True)
    course = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Payment
        fields = ('user', 'date', 'amount', 'method', 'course', 'lesson')


class UserSerializer(serializers.ModelSerializer):
    """Просмотр публичного профиля пользователя"""

    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'email', 'avatar', 'phone', 'country']


class UserProfileSerializer(serializers.ModelSerializer):
    """Просмотр полного профиля пользователя"""
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = '__all__'
