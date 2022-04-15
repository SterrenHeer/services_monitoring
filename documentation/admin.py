from django.contrib import admin
from .models import Street, Building, Apartment, ServiceType, Service, Equipment, Position

admin.site.register(Street)
admin.site.register(Building)
admin.site.register(Apartment)
admin.site.register(ServiceType)
admin.site.register(Service)
admin.site.register(Equipment)
admin.site.register(Position)
