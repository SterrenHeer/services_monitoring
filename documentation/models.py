from django.db import models


class Street(models.Model):
    name = models.CharField(max_length=200, help_text="Введите название улицы")

    def __str__(self):
        return self.name


class Building(models.Model):
    number = models.IntegerField()
    street = models.ForeignKey('Street', on_delete=models.SET_NULL, null=True)
    apartments_quantity = models.IntegerField()

    def __str__(self):
        return f"{self.street}, {self.number}"


class Apartment(models.Model):
    building = models.ForeignKey('Building', on_delete=models.SET_NULL, null=True)
    apartment_number = models.IntegerField()
    area = models.IntegerField()
    tenants_quantity = models.IntegerField()

    def __str__(self):
        return f"{self.building}, {self.apartment_number}"


class Equipment(models.Model):
    title = models.CharField(max_length=200, help_text="Введите наименование оборудования")
    cost = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.title


class Service(models.Model):
    name = models.CharField(max_length=200, help_text="Введите название услуги")
    price = models.IntegerField()
    service_type = models.ForeignKey('ServiceType', on_delete=models.SET_NULL, null=True)
    equipment = models.ManyToManyField('Equipment')

    def __str__(self):
        return self.name


class ServiceType(models.Model):
    title = models.CharField(max_length=200, help_text="Введите тип услуги")

    def __str__(self):
        return self.title

