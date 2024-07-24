import bcrypt

from django.conf import settings

salt = bytes(settings.SECRET_KEY.encode('utf-8'))


def hash_password(password: str):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password.decode('utf-8').split('.')[-1]


def check_password(input_password, hashed_password):
    return str(hash_password(input_password)) == hashed_password
