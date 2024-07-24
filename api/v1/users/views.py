from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from api.pagination import ObjectsListPagination
from api.permissions import IsOwnOrReadOnly
from api.mixins import AuthenticateRedirectMixin
from cars.tasks import send_car_mail
from .serializers import (
    UserSerializer,
    UserCarsSerializer,
    UserCreateSerializer, RetrieveUserSerializer, CarsSerializer
)

User = get_user_model()


class UsersListAPIView(AuthenticateRedirectMixin, ListAPIView):
    queryset = User.objects.select_related('language')
    serializer_class = UserSerializer
    pagination_class = ObjectsListPagination


class RetrieveUpdateDestroyUserAPIView(
    AuthenticateRedirectMixin,
    RetrieveUpdateDestroyAPIView
):
    queryset = User.objects.select_related('language')
    serializer_class = RetrieveUserSerializer
    permission_classes = (IsOwnOrReadOnly,)


class UserCarsAPIView(
    AuthenticateRedirectMixin,
    RetrieveAPIView,
):
    queryset = User.objects.select_related('language')
    serializer_class = UserCarsSerializer


@api_view(['PUT'])
def add_car_to_user_api_view(request, pk):
    if request.user.pk != pk and not request.user.is_staff:
        return Response({
            "detail": "You do not have permission to perform this action."
        }, status=status.HTTP_403_FORBIDDEN,)

    user = request.user
    if request.user.is_staff:  # В случае если машины добавляет админ
        user = User.objects.get(pk=pk)

    serializer = CarsSerializer(data=request.data)
    if serializer.is_valid():
        cars = serializer.validated_data['cars']
        for car in cars:
            user.cars.add(car)
            send_car_mail.delay(
                user.email, car, language_code=user.language.code
            )

        return Response({
            'status': 'ok',
            'cars': cars,
        },
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserAPIView(CreateAPIView):
    queryset = User.objects.select_related('language')
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(
                username=serializer.data.get('username'),
                email=serializer.data.get('email'),
                password=serializer.data.get('password'),
                language_id=serializer.data.get('language'),
            )
            serializer_data = serializer.data.copy()
            serializer_data.pop('password')
            return Response(serializer_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
