from django.urls import path
from . import views

urlpatterns = [
    path('<str:pk>/requests/', views.TenantRequestsListView.as_view(), name='tenant_requests'),
    path('allrequests/', views.AllRequestsListView.as_view(), name='all_requests'),
    path('complaints/new/', views.RequestComplaintsListView.as_view(), name='new_request_complaints'),
    path('details/<int:pk>', views.RequestDetailView.as_view(), name='request_details'),
    path("request/comment/<int:pk>/", views.CreateRequestComment.as_view(), name="request_comment_create"),
    path('request/create/', views.CreateRequest.as_view(), name='request_create'),
    path('request/create/manager', views.ManagerRequestCreate.as_view(), name='manager_request_create'),
    path('request/<int:pk>/update/', views.UpdateRequest.as_view(), name='request_update'),
    path('request/<int:pk>/update/manager', views.ManagerUpdateRequest.as_view(), name='manager_request_update'),
    path('request/<int:pk>/delete/', views.DeleteRequest.as_view(), name='request_delete'),
]
