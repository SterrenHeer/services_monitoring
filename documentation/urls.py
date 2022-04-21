from django.urls import path
from . import views

urlpatterns = [
    path('document/cleaning/schedule/', views.WorkWithCleaningSchedule.as_view(), name='cleaning_schedule'),
    path('search/schedule/', views.SearchByCleaningSchedule.as_view(), name='search_schedule'),
]
