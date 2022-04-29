from django.urls import path
from . import views

urlpatterns = [
    path('document/cleaning/schedule/', views.CleaningScheduleListView.as_view(), name='cleaning_schedule'),
    path('search/schedule/', views.SearchByCleaningSchedule.as_view(), name='search_schedule'),
    path('schedule/item/create/', views.CreateScheduleItem.as_view(), name='schedule_item_create'),
    path('schedule/item/<int:pk>/update/', views.UpdateScheduleItem.as_view(), name='schedule_item_update'),
    path('schedule/item/<int:pk>/delete/', views.DeleteScheduleItem.as_view(), name='schedule_item_delete'),
    path("schedule/item/<int:pk>/status/", views.ChangeStatus.as_view(), name="change_item_status"),
]
