from rest_framework.generics import CreateAPIView

from .serializers import CarCreateSerializer
from api.mixins import AuthenticateRedirectMixin
from cars.models import Car


class CreateCarAPIView(CreateAPIView):
    queryset = Car.objects.prefetch_related('renters')
    serializer_class = CarCreateSerializer
