from django.contrib import admin
from .models import Tenant, Worker

admin.site.register(Tenant)
admin.site.register(Worker)
