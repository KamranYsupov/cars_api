from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from api.v1.users.serializers import (
    UserSerializer,
    RetrieveUserSerializer,
    CarsSerializer,
    UserCreateSerializer
)
from cars.models import Language, Car, CarTranslatedName

User = get_user_model()


class UserAPITestCase(APITestCase):
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
        self.super_user = User.objects.create_user(
            username='admin',
            email='superuser@admin.com',
            password='12345678A',
            is_superuser=True,
            is_staff=True,
            language=self.english,
        )
        self.user_data = {
            'username': 'username',
            'email': 'email@example.com',
            'password': '12345678A',
            'language': self.english,
        }

    def test_register_view(self):
        """Проверка эндпоинта RegisterUserAPIView"""
        self.user_data['language'] = self.user_data['language'].id
        response = self.client.post(reverse('api_v1_users:register_user'), data=self.user_data)
        user_exist = User.objects.filter(email=self.user_data.get('email')).exists()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user_exist)

    def test_invalid_users_list_view(self):
        """Проверка AuthenticateRedirectMixin"""
        response = self.client.get(reverse('api_v1_users:users_list'))

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIsInstance(response, HttpResponseRedirect)

    def test_valid_users_list_view(self):
        """Проверка эндпоинта UsersListAPIView"""
        test_user = User.objects.create_user(**self.user_data)
        test_user.save()

        token = Token.objects.create(user=test_user)

        self.client.force_authenticate(user=test_user, token=token)
        response = self.client.get(reverse('api_v1_users:users_list'))

        serializer_data = UserSerializer(test_user).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_data, response.data['results'])

    def test_retrieve_user_api_view(self):
        """Проверка get запроса RetrieveUpdateDestroyUserAPIView"""
        test_user = User.objects.create_user(**self.user_data)
        test_user.save()

        token = Token.objects.create(user=test_user)
        self.client.force_authenticate(user=self.super_user, token=token)

        response = self.client.get(reverse('api_v1_users:retrieve_user', kwargs={'pk': test_user.pk}))
        serializer_data = RetrieveUserSerializer(test_user).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_update_user_api_view(self):
        """Проверка put запроса RetrieveUpdateDestroyUserAPIView"""
        user = User.objects.create_user(**self.user_data)
        user.save()

        token = Token.objects.create(user=user)
        self.client.force_authenticate(user=user, token=token)

        update_data = {
            'username': 'updated_username',
            'email': 'updated_email@example.com',
        }

        put_response = self.client.put(
            reverse('api_v1_users:retrieve_user', kwargs={'pk': user.pk}),
            data=update_data
        )

        get_response = self.client.get(
            reverse('api_v1_users:retrieve_user', kwargs={'pk': user.pk}),
        )

        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data['username'], put_response.data['username'])
        self.assertEqual(get_response.data['email'], put_response.data['email'])

    def test_delete_user_api_view(self):
        """Проверка delete запроса RetrieveUpdateDestroyUserAPIView"""
        test_user = User.objects.create_user(**self.user_data)
        test_user.save()

        token = Token.objects.create(user=self.super_user)
        self.client.force_authenticate(user=self.super_user, token=token)

        delete_response = self.client.delete(
            reverse('api_v1_users:retrieve_user', kwargs={'pk': test_user.pk}),
        )

        get_response = self.client.get(
            reverse('api_v1_users:retrieve_user', kwargs={'pk': test_user.pk}),
        )

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cars_api_view(self):
        """Проверка эндпоинта UserCarsAPIView и add_car_to_user_api_view"""
        test_user = User.objects.create_user(**self.user_data)
        test_user.save()

        token = Token.objects.create(user=test_user)
        self.client.force_authenticate(user=test_user, token=token)

        car_1 = Car.objects.create(creation_year=2024)

        car_translated_name_1 = CarTranslatedName.objects.create(
            name='Название на русском',
            car=car_1,
            language=self.russian
        )

        car_2 = Car.objects.create(creation_year=2023)

        car_translated_name_2 = CarTranslatedName.objects.create(
            name='Name in English',
            car=car_2,
            language=self.english
        )

        add_cars_data = {'cars': [car_1.id, car_2.id]}

        add_cars_response = self.client.put(
            reverse('api_v1_users:add_cars', kwargs={'pk': test_user.pk}),
            data=add_cars_data
        )

        get_user_cars_response = self.client.get(
            reverse('api_v1_users:user_cars', kwargs={'pk': test_user.pk})
        )

        self.assertEqual(add_cars_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_user_cars_response.status_code, status.HTTP_200_OK)

        self.assertIn(car_1, test_user.cars.all())
        self.assertIn(car_2, test_user.cars.all())

        self.assertEqual(add_cars_response.data['cars'], add_cars_data['cars'])
        self.assertEqual(
            get_user_cars_response.data['cars'][0]['name'],
            'This car`s name is not supported in username` language'
        )
        self.assertEqual(
            get_user_cars_response.data['cars'][1]['name'],
            car_translated_name_2.name
        )
