from django.views.generic import ListView
from .models import CleaningSchedule
from django.db.models import Q


class WorkWithCleaningSchedule(ListView):
    model = CleaningSchedule
    template_name = 'documentation/cleaning_schedule.html'

    def get_queryset(self):
        if self.request.user.groups.filter(name__in=['Master', 'Manager']).exists():
            return CleaningSchedule.objects.all().order_by('date')
        elif self.request.user.groups.filter(name='Tenant').exists():
            return CleaningSchedule.objects.filter(building_id=self.request.user.tenant.apartment.building).order_by('date')


class SearchByCleaningSchedule(ListView):
    template_name = 'documentation/cleaning_schedule.html'

    def get_queryset(self):
        search = self.request.GET.get("search")
        if self.request.user.groups.filter(name__in=['Master', 'Manager', 'Worker']).exists():
            return CleaningSchedule.objects.filter(Q(service__name__icontains=search) |
                                                   Q(date__icontains=search) |
                                                   Q(worker__full_name__icontains=search) |
                                                   Q(status__icontains=search) |
                                                   Q(start_time__icontains=search) |
                                                   Q(building__street__name__icontains=search)).order_by('date')
        if self.request.user.groups.filter(name='Tenant').exists():
            return CleaningSchedule.objects.filter(Q(service__name__icontains=search) |
                                                   Q(date__icontains=search) |
                                                   Q(worker__full_name__icontains=search) |
                                                   Q(status__icontains=search) |
                                                   Q(start_time__icontains=search))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["search"] = f"search={self.request.GET.get('search')}&"
        return context
