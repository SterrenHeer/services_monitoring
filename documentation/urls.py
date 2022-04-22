from django.urls import path
from . import views

urlpatterns = [
    path('document/cleaning/schedule/', views.CleaningScheduleListView.as_view(), name='cleaning_schedule'),
    path('search/schedule/', views.SearchByCleaningSchedule.as_view(), name='search_schedule'),
    path('schedule/item/create/', views.CreateScheduleItem.as_view(), name='schedule_item_create'),
]
