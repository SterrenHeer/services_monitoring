from django.urls import path
from . import views

urlpatterns = [
    path('<str:pk>/requests/', views.TenantRequestsListView.as_view(), name='tenant_requests'),
    path('allrequests/', views.AllRequestsListView.as_view(), name='all_requests'),
    path('details/<int:pk>', views.RequestDetailView.as_view(), name='request_details'),
    path('request/create/', views.RequestCreate.as_view(), name='request_create'),
    path('request/<int:pk>/update/', views.RequestUpdate.as_view(), name='request_update'),
    path('request/<int:pk>/delete/', views.RequestDelete.as_view(), name='request_delete'),
]
