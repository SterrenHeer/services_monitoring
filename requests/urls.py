from django.urls import path
from . import views

urlpatterns = [
    path('requests/', views.TenantRequestsListView.as_view(), name='tenant_requests'),
    path('details/<int:pk>', views.RequestDetailView.as_view(), name='request_details'),
]
