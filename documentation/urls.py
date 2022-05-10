from django.urls import path
from . import views

urlpatterns = [
    path('cleaning/schedule/', views.CleaningScheduleListView.as_view(), name='cleaning_schedule'),
    path('annual/plan/<str:type>/', views.AnnualPlanListView.as_view(), name='annual_plan'),
    path('annual/plan/<str:type>/search/', views.SearchByAnnualPlan.as_view(), name='search_plan'),
    path('plan/item/<str:type>/create/', views.CreatePlanItem.as_view(), name='plan_item_create'),
    path('plan/item/<str:type>/<int:pk>/update/', views.UpdatePlanItem.as_view(), name='plan_item_update'),
    path('plan/item/<str:type>/<int:pk>/delete/', views.DeletePlanItem.as_view(), name='plan_item_delete'),
    path('plan/export/', views.plan_export, name='plan_export'),
    path('schedule/search/', views.SearchByCleaningSchedule.as_view(), name='search_schedule'),
    path('schedule/item/create/', views.CreateScheduleItem.as_view(), name='schedule_item_create'),
    path('schedule/item/<int:pk>/update/', views.UpdateScheduleItem.as_view(), name='schedule_item_update'),
    path('schedule/item/<int:pk>/delete/', views.DeleteScheduleItem.as_view(), name='schedule_item_delete'),
    path('schedule/export/', views.schedule_export, name='schedule_export'),
    path("change/item/<int:pk>/status/", views.ChangeStatus.as_view(), name="change_item_status"),
]
