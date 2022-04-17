from django.urls import path
from . import views

urlpatterns = [
    path('account/create/', views.sign_up, name='signup'),
    path('account/login/', views.log_in, name='login'),
    path('', views.log_in, name='login'),
    path('account/logout/', views.log_out, name='logout'),
    path('tenant/<int:pk>/update/', views.TenantUpdate.as_view(), name='tenant_update'),
    path('workers/', views.WorkersListView.as_view(), name='all_workers'),
]
