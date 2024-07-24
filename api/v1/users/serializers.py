from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.v1.cars.serializers import CarSerializer, LanguageSerializer
from .mixins import UserSerializerMixin
from cars.models import Car, CarTranslatedName, Language
from api.service import update_serializer_data

User = get_user_model()


class UserSerializer(UserSerializerMixin):
    language = LanguageSerializer(read_only=True)


class RetrieveUserSerializer(UserSerializerMixin):
    ...


class UserCarsSerializer(UserSerializerMixin):
    cars = serializers.SerializerMethodField()

    class Meta(UserSerializerMixin.Meta):
        fields = UserSerializerMixin.Meta.fields + ('cars',)

    @staticmethod
    def get_cars(obj):
        """
        Данный метод возвращает данные автомобилей пользователя
        """
        cars = obj.cars.all()
        cars_serializer = CarSerializer(data=cars, many=True)
        cars_serializer.is_valid()

        cars_names = (CarTranslatedName.objects
                      .select_related('car', 'language')
                      .filter(car__in=cars, language__code=obj.language.code)
                      .values('name', 'id')
                      )

        return update_serializer_data(
            'name',
            cars_names,
            cars_serializer.data,
            not_found_value=
            f'This car`s name '
            f'is not supported in {obj.username}`s language',
        )


class UserCreateSerializer(UserSerializerMixin):
    class Meta(UserSerializerMixin.Meta):
        fields = UserSerializerMixin.Meta.fields + ('password',)


class CarsSerializer(serializers.Serializer):
    cars = serializers.ListField(
        child=serializers.IntegerField()
    )
