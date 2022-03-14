from django.urls import path
from . import views

urlpatterns = [
    path('tenant/', views.tenant_home_page, name='tenant_home_page'),
    path('master/', views.master_home_page, name='master_home_page'),
    path('account/create/', views.sign_up, name='signup'),
    path('account/login/', views.log_in, name='login'),
]
