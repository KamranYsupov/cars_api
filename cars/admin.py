from django.contrib import admin

from .models import Car, CarTranslatedName, Language


admin.site.register(CarTranslatedName)
admin.site.register(Language)


class CarTranslatedNameInline(admin.TabularInline):
    """Инлайн форма названия автомобиля."""
    model = CarTranslatedName
    extra = 1


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """Админ-панель для управления автомобилями"""
    inlines = (CarTranslatedNameInline,)


