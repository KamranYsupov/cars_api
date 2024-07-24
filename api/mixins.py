from django.shortcuts import redirect
from django.urls import reverse


class AuthenticateRedirectMixin:
    """
    Класс миксин выполняющий redirect на страницу войти

    РАБОТАЕТ ТОЛЬКО НА rest_framework.generics КЛАССАХ
    """
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super().post(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super().delete(request, *args, **kwargs)

