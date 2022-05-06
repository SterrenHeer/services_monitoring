from django.db import models
from django.conf import settings
import datetime


class Street(models.Model):
    name = models.CharField("Название улицы", max_length=200)

    class Meta:
        verbose_name = 'улицу'
        verbose_name_plural = 'Улицы'

    def __str__(self):
        return self.name


class Building(models.Model):
    number = models.IntegerField("Жилец")
    street = models.ForeignKey('Street', on_delete=models.CASCADE, verbose_name="Улица")
    apartments_quantity = models.IntegerField("Количество квартир")

    class Meta:
        verbose_name = 'здание'
        verbose_name_plural = 'Здания'

    def __str__(self):
        return f"{self.street}, {self.number}"


class Apartment(models.Model):
    building = models.ForeignKey('Building', on_delete=models.CASCADE, verbose_name="Здание")
    apartment_number = models.IntegerField("Номер квартиры")
    area = models.IntegerField("Площадь помещения")
    tenants_quantity = models.IntegerField("Количество жильцов")

    class Meta:
        verbose_name = 'квартиру'
        verbose_name_plural = 'Квартиры'

    def __str__(self):
        return f"{self.building}, {self.apartment_number}"


class Equipment(models.Model):
    title = models.CharField("Наименование", max_length=200)

    class Meta:
        verbose_name = 'оборудование'
        verbose_name_plural = 'Оборудование'

    def __str__(self):
        return self.title


class Service(models.Model):
    name = models.CharField("Наименование", max_length=200)
    price = models.IntegerField("Стоимость")
    service_type = models.ForeignKey('ServiceType', on_delete=models.CASCADE, verbose_name="Тип услуги")
    equipment = models.ManyToManyField('Equipment', verbose_name="Оборудование")
    duration = models.TimeField("Время исполнения", default=datetime.time(1, 0))

    class Meta:
        verbose_name = 'услугу'
        verbose_name_plural = 'Услуги'

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
    title = models.CharField("Наименование", max_length=200)
    nature = models.CharField("Характер", max_length=20, choices=NATURE_CHOICES, default='Замечание')

    class Meta:
        verbose_name = 'тип услуги'
        verbose_name_plural = 'Типы услуг'

    def __str__(self):
        return self.title


class Position(models.Model):
    name = models.CharField("Наименование", max_length=200)
    service_type = models.ManyToManyField('ServiceType', verbose_name="Тип услуги")

    class Meta:
        verbose_name = 'должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.name


class CleaningSchedule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             null=True, verbose_name="Пользователь")
    building = models.ForeignKey('Building', on_delete=models.CASCADE, verbose_name="Здание")
    service = models.ForeignKey('Service', on_delete=models.CASCADE, verbose_name="Услуга")
    worker = models.ForeignKey('users.Worker', on_delete=models.SET_NULL,
                               null=True, blank=True, verbose_name="Работник")
    date = models.DateField("Дата проведения", default=datetime.date.today)
    status = models.CharField("Состояние", max_length=200, default="Запланирована")
    start_time = models.TimeField("Время начала", default=datetime.time(8, 0))

    class Meta:
        verbose_name = 'график уборки'
        verbose_name_plural = 'Графики уборки'

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


class AnnualPlan(models.Model):
    TYPE_CHOICES = (
        ('Благоустройство', 'Благоустройство'),
        ('Ремонт', 'Ремонт'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             null=True, verbose_name="Пользователь")
    building = models.ForeignKey('Building', on_delete=models.CASCADE, verbose_name="Здание")
    service = models.ForeignKey('Service', on_delete=models.CASCADE, verbose_name="Услуга")
    worker = models.ForeignKey('users.Worker', on_delete=models.SET_NULL,
                               null=True, blank=True, verbose_name="Работник")
    date = models.DateField("Дата проведения", default=datetime.date.today)
    status = models.CharField("Состояние", max_length=200, default="Запланирована")
    start_time = models.TimeField("Время начала", default=datetime.time(8, 0))
    type = models.CharField("Характер", max_length=200, choices=TYPE_CHOICES, default="Благоустройство")

    class Meta:
        verbose_name = 'годовой план'
        verbose_name_plural = 'Годовые планы'

    def __str__(self):
        return f"{self.service} ({self.building})"

    def get_current_date(self):
        return self.date <= datetime.date.today()

    def get_overdue(self):
        return self.date < datetime.date.today()
