from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_page, name='home_page'),
    path('account/create/', views.sign_up, name='signup'),
    path('account/login/', views.log_in, name='login'),
    path('', views.log_in, name='login'),
    path('account/logout/', views.log_out, name='logout'),
    path('tenant/<int:pk>/update/', views.TenantUpdate.as_view(), name='tenant_update'),
]
