import stripe
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course
from lms.paginators import PaymentsPaginator
from lms.services import create_stripe_product, create_stripe_price, create_stripe_checkout_session, \
    retrieve_stripe_checkout_session
from users.models import Payment, Subscription
from lms.permissions import IsOwnerOrReadOnly, IsModerator
from users.serializers import UserSerializer, PaymentSerializer, UserProfileSerializer


class UserApiList(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated]


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer
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
        if self.kwargs.get('pk') == self.request.user.pk:
            return UserProfileSerializer  # просмотр собственного профиля
        else:
            return UserSerializer  # просмотр чужого профиля

    def get_object(self):
        return super().get_object()


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
    # swagger_schema = None
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # Бэкенд для обработки фильтра
    filterset_fields = ('course', 'lesson', 'method')  # Набор полей для фильтрации
    ordering_fields = ('date',)
    queryset = Payment.objects.all()
    pagination_class = PaymentsPaginator
    permission_classes = [IsAuthenticated | IsModerator]

    def get_queryset(self):
        # Показывает только платежи пользователя
        if not self.request.user.groups.filter(name='moderators').exists():
            return Payment.objects.filter(user=self.request.user)
        # Для модератора показывает все
        return Payment.objects.all()

    @swagger_auto_schema(
        operation_description="List all payments",
        responses={
            200: PaymentSerializer(many=True),
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Forbidden',
        }
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        if not paginated_queryset:
            return Response({'message': 'No payments to display.'}, status=200)
        return paginator.get_paginated_response(serializer.data)


class CreatePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        user_email = request.user.email

        # Получает курс
        course = get_object_or_404(Course, id=course_id)

        # Создает продукт и цену в Stripe
        product = create_stripe_product(course)
        price = create_stripe_price(product, course.price)

        # Создает сессию оплаты
        session = create_stripe_checkout_session(price.id, user_email)

        # Создает платеж в системе
        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            method='transfer',
            session_id=session.id
        )

        # Сохраняет ссылку на оплату
        payment.session_id = session.id
        payment.save()

        # Возвращает ссылку на оплату
        return Response({'payment_url': session.url}, status=status.HTTP_201_CREATED)


class PaymentStatusView(View):
    """
        Представление для обработки статуса платежа после успешной оплаты через Stripe.
        Ожидает параметр 'session_id' в GET-запросе, использует его для получения информации о сессии оплаты из Stripe
        и обновления статуса платежа в базе данных.
        """
    def get(self, request, *args, **kwargs):
        # Получаем ID сессии из параметров запроса
        session_id = request.GET.get('session_id')
        if not session_id:
            # Возвращаем ошибку, если session_id не предоставлен
            return JsonResponse({'error': 'Session ID is required'}, status=400)

        try:
            # Получаем информацию о сессии оплаты из Stripe
            session = retrieve_stripe_checkout_session(session_id)
            payment_status = session.payment_status

            # Находим платеж в базе данных по stripe_session_id
            payment = get_object_or_404(Payment, session_id=session_id)
            if payment:
                # Сохраняем статус платежа в базе данных
                payment.status = payment_status
                print(f"Payment status from Stripe: {payment_status}")
                payment.save()

            # Возвращаем статус платежа в ответе
            return JsonResponse({'payment_status': payment_status}, status=200)
        except stripe.error.StripeError as e:
            # Возвращаем ошибку, если произошла ошибка при взаимодействии с Stripe API
            return JsonResponse({'error': str(e)}, status=400)


class SubscriptionAPIView(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = f'You have successfully unsubscribed from {course_item.name} updates.'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = f'You have been successfully subscribed to {course_item.name} updates.'
        # Возвращаем ответ в API
        return Response({"message": message})
