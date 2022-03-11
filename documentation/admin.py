from django.contrib import admin
from .models import Street, Building, Apartment, ServiceType, Service, Equipment
from users.models import Tenant

admin.site.register(Street)
admin.site.register(Building)
admin.site.register(Apartment)
admin.site.register(Tenant)
admin.site.register(ServiceType)
admin.site.register(Service)
admin.site.register(Equipment)
