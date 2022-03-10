from django.urls import path
from . import views

urlpatterns = [
    path('', views.tenant_home_page, name='tenant_home_page'),
    path('account/create/', views.sign_up, name='signup'),
]
