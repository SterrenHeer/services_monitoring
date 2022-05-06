from django.contrib import admin
from .models import Tenant, Worker


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'contact_details', 'apartment')
    search_fields = ('full_name',)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'contact_details', 'position')
    search_fields = ('full_name',)
