from django.db import models
from django.conf import settings
import datetime


class Street(models.Model):
    name = models.CharField(max_length=200, help_text="Введите название улицы")

    def __str__(self):
        return self.name


class Building(models.Model):
    number = models.IntegerField()
    street = models.ForeignKey('Street', on_delete=models.CASCADE)
    apartments_quantity = models.IntegerField()

    def __str__(self):
        return f"{self.street}, {self.number}"


class Apartment(models.Model):
    building = models.ForeignKey('Building', on_delete=models.CASCADE)
    apartment_number = models.IntegerField()
    area = models.IntegerField()
    tenants_quantity = models.IntegerField()

    def __str__(self):
        return f"{self.building}, {self.apartment_number}"


class Equipment(models.Model):
    title = models.CharField(max_length=200, help_text="Введите наименование оборудования")

    def __str__(self):
        return self.title


class Service(models.Model):
    name = models.CharField(max_length=200, help_text="Введите название услуги")
    price = models.IntegerField()
    service_type = models.ForeignKey('ServiceType', on_delete=models.CASCADE)
    equipment = models.ManyToManyField('Equipment')
    duration = models.TimeField(default=datetime.time(1, 0))

    def __str__(self):
        return self.name


class ServiceType(models.Model):
    NATURE_CHOICES = (
        ('Заявка', 'Заявка'),
        ('Замечание', 'Замечание'),
        ('Уборка', 'Уборка'),
        ('Ремонт', 'Ремонт'),
        ('Благоустройство', 'Благоустройство'),
    )
    title = models.CharField(max_length=200, help_text="Введите тип услуги")
    nature = models.CharField(max_length=20, choices=NATURE_CHOICES, default='Замечание')

    def __str__(self):
        return self.title


class Position(models.Model):
    name = models.CharField(max_length=200, help_text="Введите название должности")
    service_type = models.ManyToManyField('ServiceType')

    def __str__(self):
        return self.name


class CleaningSchedule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    building = models.ForeignKey('Building', on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    worker = models.ForeignKey('users.Worker', on_delete=models.SET_NULL, null=True)
    date = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=200, default="Запланирована")
    start_time = models.TimeField(default=datetime.time(8, 0))

    def __str__(self):
        return f"{self.service} ({self.building})"

    def get_end_time(self):
        hour = self.start_time.hour + self.service.duration.hour
        minute = self.start_time.minute + self.service.duration.minute
        if minute >= 60:
            minute %= 60
            hour += 1
        return datetime.time(hour, minute)

    def get_current_date(self):
        return self.date <= datetime.date.today()

    def get_overdue(self):
        return self.date < datetime.date.today()
