from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('requests.urls')),
    path('', include('documentation.urls')),
]

admin.site.site_header = "Административная панель ЖЭУ"
admin.site.site_title  =  "Административная панель ЖЭУ"
admin.site.index_title  =  "Административная панель ЖЭУ"
