from django.urls import path
from . import views

urlpatterns = [
    path('allrequests/', views.AllRequestsListView.as_view(), name='all_requests'),
    path('search/', views.Search.as_view(), name='search'),
    path('export/excel', views.export_to_excel, name='export_to_excel'),
    path('export/pdf', views.export_to_pdf, name='export_to_pdf'),
    path('complaints/new/', views.RequestComplaintsListView.as_view(), name='request_comments'),
    path('details/<int:pk>', views.RequestDetailView.as_view(), name='request_details'),
    path("request/comment/<int:pk>/", views.WorkWithRequestComment.as_view(), name="request_comment_create"),
    path("request/<int:pk>/appointment/", views.WorkerAppointment.as_view(), name="worker_appointment"),
    path('request/create/', views.CreateRequest.as_view(), name='request_create'),
    path('request/create/manager', views.ManagerRequestCreate.as_view(), name='manager_request_create'),
    path('request/<int:pk>/update/', views.UpdateRequest.as_view(), name='request_update'),
    path('request/<int:pk>/update/manager', views.ManagerUpdateRequest.as_view(), name='manager_request_update'),
    path('request/<int:pk>/delete/', views.DeleteRequest.as_view(), name='request_delete'),
    path('request/comment/<int:pk>/delete/', views.DeleteRequestComment.as_view(), name='request_comment_delete'),
]
