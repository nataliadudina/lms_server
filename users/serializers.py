from rest_framework import serializers

from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    # выводит строку вместо id
    user = serializers.SlugRelatedField(slug_field="email", read_only=True)
    lesson = serializers.SlugRelatedField(slug_field="name", read_only=True)
    course = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Payment
        fields = ('user', 'date', 'amount', 'method', 'course', 'lesson')


class PaymentDetailsSerializer(serializers.ModelSerializer):

    pass


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
