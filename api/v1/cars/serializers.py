from django.contrib.auth import get_user_model
from rest_framework import serializers

from cars.models import Car, Language, CarTranslatedName

User = get_user_model()


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('id', 'creation_year', 'time_add')


class CarCreateSerializer(serializers.ModelSerializer):
    car = CarSerializer()

    class Meta:
        model = CarTranslatedName
        fields = ('name', 'car', 'language')

    def create(self, validated_data):
        car_data = validated_data.pop('car')
        creation_year = car_data.get('creation_year')

        car = Car.objects.create(creation_year=creation_year)

        car_name = validated_data.get('name')
        language = validated_data.get('language')

        car_translated_name = CarTranslatedName.objects.create(
            name=car_name,
            car=car,
            language=language
        )

        return car_translated_name

