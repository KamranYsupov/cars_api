from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core.settings import AUTH_USER_MODEL


class Car(models.Model):
    """Модель автомобиля"""
    time_add = models.DateTimeField(
        'Время добавления',
        auto_now_add=True,
    )
    creation_year = models.PositiveBigIntegerField(
        'Год создания',
        validators=[],
    )
    renters = models.ManyToManyField(
        AUTH_USER_MODEL,
        related_name='cars',
        blank=True,
    )

    def __str__(self):
        try:
            translated_car_name = self.translated_names.get(language__code='en').name

        except ObjectDoesNotExist:
            translated_car_name = self.translated_names.first().name

        return translated_car_name


class Language(models.Model):
    """Модель языка"""
    code = models.CharField('Код', max_length=5)
    name = models.CharField('Название', max_length=70)

    def __str__(self):
        return f'{self.name} ({self.code})'


class CarTranslatedName(models.Model):
    """Модель названия машины на определенном языке"""
    name = models.CharField('Название', max_length=150)
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='translated_names',
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name='cars_names',
    )

    def __str__(self):
        return self.name



