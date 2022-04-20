from django.views.generic import ListView
from .models import CleaningSchedule


class WorkWithCleaningSchedule(ListView):
    model = CleaningSchedule
    template_name = 'documentation/cleaning_schedule.html'

