from django.db import models
from django.conf import settings
from django.urls import reverse


class Tenant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, help_text="Введите ФИО")
    contact_details = models.CharField(max_length=200, help_text="Введите контактные данные")
    apartment = models.ForeignKey('documentation.Apartment', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('tenant_requests', args=[str(self.full_name)])
