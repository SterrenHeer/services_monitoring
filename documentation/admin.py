from django.contrib import admin
from .models import Street, Building, Apartment, ServiceType, Service, Equipment, Position, CleaningSchedule, AnnualPlan


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('number', 'street', 'apartments_quantity')
    list_filter = ('street',)


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('building', 'apartment_number', 'area', 'tenants_quantity')
    list_filter = ('building',)


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'nature')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'service_type', 'duration', 'equipment_titles')
    list_filter = ('service_type',)
    search_fields = ('name',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_types_titles')


@admin.register(CleaningSchedule)
class CleaningScheduleAdmin(admin.ModelAdmin):
    list_display = ('building', 'date', 'service', 'status', 'start_time', 'worker')
    list_filter = ('building', 'date', 'status')
    search_fields = ('service', 'worker')


@admin.register(AnnualPlan)
class AnnualPlanAdmin(admin.ModelAdmin):
    list_display = ('building', 'service', 'date', 'status', 'worker')
    list_filter = ('building', 'date', 'status')
    search_fields = ('service', 'worker')




