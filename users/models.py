import unicodedata
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractUser

from cars.models import Language
from .utils.hashers import hash_password, check_password
from .utils.validators import password_validator
from django.core.validators import EmailValidator
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")

        user = self.model(email=email, password=password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class CustomAbstractBaseUser(models.Model):
    """Кастомноя базовая модель абстрактного пользователя"""
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    password = models.CharField(
        'Пароль',
        max_length=60,
        validators=[password_validator]
    )
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        self.password = hash_password(raw_password)
        self._password = raw_password

    def check_password(self, password):
        return check_password(password, self.password)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_password(self.password)
        super(CustomAbstractBaseUser, self).save(*args, **kwargs)

    def get_username(self):
        return getattr(self, self.USERNAME_FIELD)

    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return "email"

    @classmethod
    def normalize_username(cls, username):
        return (
            unicodedata.normalize("NFKC", username)
            if isinstance(username, str)
            else username
        )


class CustomAbstractUser(CustomAbstractBaseUser, PermissionsMixin):
    """Кастомноя модель абстрактного пользователя"""
    objects = UserManager()
    REQUIRED_FIELDS = ('password',)

    email = models.EmailField(
        'E-mail',
        unique=True,
        db_index=True,
        validators=[EmailValidator(message='Некорректный E-mail')]
    )


class User(CustomAbstractUser):
    username = models.CharField('Имя', max_length=70)
    language = models.ForeignKey(
        Language,
        related_name='users',
        on_delete=models.PROTECT,
        null=True,
        default=None,
    )

