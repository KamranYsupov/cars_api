from django.urls import path, include, re_path

from .views import (
    UsersListAPIView,
    RetrieveUpdateDestroyUserAPIView,
    UserCarsAPIView,
    RegisterUserAPIView,
    add_car_to_user_api_view,
)

app_name = 'api_v1_users'

urlpatterns = [
    path('', UsersListAPIView.as_view(), name='users_list'),
    path('<int:pk>/', RetrieveUpdateDestroyUserAPIView.as_view(), name='retrieve_user'),
    path('<int:pk>/cars/', UserCarsAPIView.as_view(), name='user_cars'),
    path('<int:pk>/add_cars/', add_car_to_user_api_view, name='add_cars'),
    path('register/', RegisterUserAPIView.as_view(), name='register_user'),
]
