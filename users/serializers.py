from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Payment, Subscription


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
    password = serializers.CharField(write_only=True, required=True)
    payments = PaymentSerializer(many=True, read_only=True)
    subscriptions = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = '__all__'

    def get_subscriptions(self, instance):
        # Получаем все подписки текущего пользователя
        subscriptions = Subscription.objects.filter(user=instance)

        subscription_list = []
        for subscription in subscriptions:
            subscription_info = {
                'course_name': subscription.course.name,
                'is_subscribed': True
            }
            subscription_list.append(subscription_info)
        return subscription_list

