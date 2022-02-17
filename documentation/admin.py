from django.contrib import admin
from .models import Street, Building, Apartment, Tenant, ServiceType, Service, Equipment

admin.site.register(Street)
admin.site.register(Building)
admin.site.register(Apartment)
admin.site.register(Tenant)
admin.site.register(ServiceType)
admin.site.register(Service)
admin.site.register(Equipment)
