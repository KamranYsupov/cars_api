from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from cars.models import Car, CarTranslatedName
from core.celery import app


@app.task
def send_car_mail(email, car_id: Car.id, language_code: str) -> None:
    try:
        car_name = (CarTranslatedName.objects
                    .get(car_id=car_id, language__code=language_code)).name
    except ObjectDoesNotExist:
        car_name = (CarTranslatedName.objects
                    .get(car_id=car_id, language__code='en')).name

    return send_mail(
        settings.EMAIL_SUBJECT,
        f'You have rented {car_name}!\n'  # Поменять на вызов функции translate, которая будет 
        f'Have a nice trip!',                      # переводить текст письма на язык пользователя
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
