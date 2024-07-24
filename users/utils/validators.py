from string import digits, ascii_uppercase

from django.core.exceptions import ValidationError


def password_validator(password: str):
    if not any(char.isdigit() for char in password):
        raise ValidationError('Пароль должен содержать хотя бы 1 цифру')
    if not any(char.isupper() for char in password):
        raise ValidationError('Пароль должен содержать хотя бы 1 заглавную букву')
