from django.urls import path
from . import views

urlpatterns = [
    path('cleaning/schedule/', views.CleaningScheduleListView.as_view(), name='cleaning_schedule'),
    path('improvement/plan/', views.ImprovementPlanListView.as_view(), name='improvement_plan'),
    path('improvement/item/create/', views.CreateImprovementItem.as_view(), name='improvement_item_create'),
    path('improvement/item/<int:pk>/update/', views.UpdateImprovementItem.as_view(), name='improvement_item_update'),
    path('improvement/item/<int:pk>/delete/', views.DeleteImprovementItem.as_view(), name='improvement_item_delete'),
    path('schedule/search/', views.SearchByCleaningSchedule.as_view(), name='search_schedule'),
    path('schedule/item/create/', views.CreateScheduleItem.as_view(), name='schedule_item_create'),
    path('schedule/item/<int:pk>/update/', views.UpdateScheduleItem.as_view(), name='schedule_item_update'),
    path('schedule/item/<int:pk>/delete/', views.DeleteScheduleItem.as_view(), name='schedule_item_delete'),
    path("schedule/item/<int:pk>/status/", views.ChangeStatus.as_view(), name="change_item_status"),
]
