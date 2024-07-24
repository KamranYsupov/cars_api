from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from ..serializers import CarSerializer, CarCreateSerializer
from cars.models import Language, Car, CarTranslatedName


class CarAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.english = Language.objects.create(
            name='English',
            code='en'
        )
        self.russian = Language.objects.create(
            name='Русский',
            code='ru'
        )
        self.car_data = {
            'name': 'English name',
            'car': {
                'creation_year': 2024
            },
            'language': self.english.id
        }

    def test_create_car_api_view(self):
        """Проверка эндпоинта CreateCarAPIView"""
        response = self.client.post(
            reverse('api_v1_cars:create_car'),
            data=self.car_data,
            format='json'
        )

        car_exists = Car.objects.all().exists()

        serializer = CarCreateSerializer(data=self.car_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(serializer.is_valid())
        self.assertTrue(car_exists)
