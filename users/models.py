from django.db import models
from django.conf import settings


class Tenant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    full_name = models.CharField(max_length=200, help_text="Введите ФИО")
    contact_details = models.CharField(max_length=200, help_text="Введите контактные данные")
    apartment = models.ForeignKey('documentation.Apartment', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.full_name
