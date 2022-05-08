from django.urls import path
from . import views

urlpatterns = [
    path('allrequests/<str:status>/', views.AllRequestsListView.as_view(), name='all_requests'),
    path('allcomments/<str:status>/', views.CommentListView.as_view(), name='comments'),
    path('cleaning/comments/<str:status>/', views.CleaningCommentListView.as_view(), name='cleaning_comments'),
    path('search/requests/<str:status>/', views.SearchByRequests.as_view(), name='search_requests'),
    path('request/export/excel', views.request_export_to_excel, name='request_export_to_excel'),
    path('request/export/pdf', views.request_export_to_pdf, name='request_export_to_pdf'),
    path('allrequestcomments/<str:status>/', views.RequestCommentsListView.as_view(), name='request_comments'),
    path('details/<int:pk>/', views.RequestDetailView.as_view(), name='request_details'),
    path("request/comment/<int:pk>/", views.WorkWithRequestComment.as_view(), name="work_with_request_comment"),
    path("request/<int:pk>/<str:status>/appointment/", views.WorkerAppointment.as_view(), name="worker_appointment"),
    path("request/<int:pk>/<str:status>/status/", views.ChangeStatus.as_view(), name="change_status"),
    path('request/create/', views.CreateRequest.as_view(), name='request_create'),
    path('request/create/manager/', views.ManagerRequestCreate.as_view(), name='manager_request_create'),
    path('request/<int:pk>/update/', views.UpdateRequest.as_view(), name='request_update'),
    path('request/<int:pk>/update/manager/', views.ManagerUpdateRequest.as_view(), name='manager_request_update'),
    path('request/<int:pk>/<str:status>/delete/', views.DeleteRequest.as_view(), name='request_delete'),
    path('request/comment/<int:pk>/delete/', views.DeleteRequestComment.as_view(), name='request_comment_delete'),
    path('comment/create/', views.CreateComment.as_view(), name='comment_create'),
    path('comment/<int:pk>/<str:status>/delete/', views.DeleteComment.as_view(), name='comment_delete'),
]
