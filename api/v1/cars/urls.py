from django.urls import path, include, re_path

from .views import CreateCarAPIView

app_name = 'api_v1_cars'

urlpatterns = [
    path('create/', CreateCarAPIView.as_view(), name='create_car'),
]
