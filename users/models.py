from django.db import models
from django.conf import settings
from documentation.models import Service, Position


class Tenant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    full_name = models.CharField(max_length=200, help_text="Введите ФИО")
    contact_details = models.CharField(max_length=200, help_text="Введите контактные данные")
    apartment = models.ForeignKey('documentation.Apartment', on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class Worker(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    full_name = models.CharField(max_length=200, help_text="Введите ФИО")
    contact_details = models.CharField(max_length=200, help_text="Введите контактные данные")
    position = models.ForeignKey('documentation.Position', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.full_name} ({self.position})"

    def get_services(self):
        return Service.objects.filter(service_type__in=self.position.service_type.all())

    def get_positions(self):
        return Position.objects.exclude(name__icontains='Мастер')\
                               .filter(service_type__in=self.position.service_type.all()).distinct()
