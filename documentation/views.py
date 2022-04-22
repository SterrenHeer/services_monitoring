from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import CleaningSchedule
from django.db.models import Q
import datetime


class CleaningScheduleListView(ListView):
    model = CleaningSchedule
    template_name = 'documentation/cleaning_schedule.html'

    def get_queryset(self):
        if self.request.user.groups.filter(name__in=['Master', 'Manager']).exists():
            return CleaningSchedule.objects.all().order_by('building', 'date')
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


class CreateScheduleItem(CreateView):
    model = CleaningSchedule
    template_name = 'documentation/create_schedule_item.html'
    fields = ['building', 'service', 'worker', 'date', 'start_time']

    def form_valid(self, form):
        if form.cleaned_data['date'] < datetime.date.today():
            form.add_error('date', 'Введите правильную дату.')
        elif form.cleaned_data['date'] == datetime.date.today() and form.cleaned_data['start_time'] <= datetime.datetime.now().time():
            form.add_error('start_time', 'Введите правильное время.')
        if form.errors:
            return self.form_invalid(form)

        form.instance.user = self.request.user
        return super(CreateScheduleItem, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('cleaning_schedule')
