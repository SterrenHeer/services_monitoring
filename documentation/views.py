from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import CleaningSchedule, Service, AnnualPlan
from django.db.models import Q
import datetime
from django.http import HttpResponse
import xlwt
from weasyprint import HTML
from django.template.loader import render_to_string
import tempfile
from django import forms


class CleaningScheduleListView(ListView):
    model = CleaningSchedule
    template_name = 'documentation/cleaning_schedule.html'

    def get_queryset(self):
        if self.request.user.groups.filter(name__in=['Master', 'Manager']).exists():
            return CleaningSchedule.objects.all().order_by('building', 'date')
        elif self.request.user.groups.filter(name='Tenant').exists():
            return CleaningSchedule.objects.filter(building_id=self.request.user.tenant.apartment.building)\
                                   .order_by('date')
        elif self.request.user.groups.filter(name='Worker').exists():
            return CleaningSchedule.objects.filter(worker=self.request.user.worker).order_by('building', 'date')


class AnnualPlanListView(ListView):
    model = AnnualPlan
    template_name = 'documentation/annual_plan.html'

    def get_queryset(self):
        if self.request.user.groups.filter(name__in=['Master', 'Manager']).exists():
            return AnnualPlan.objects.filter(type=self.kwargs['type']).order_by('building', 'date')
        elif self.request.user.groups.filter(name='Tenant').exists():
            return AnnualPlan.objects.filter(building_id=self.request.user.tenant.apartment.building,
                                             type=self.kwargs['type']).order_by('date')
        elif self.request.user.groups.filter(name='Worker').exists():
            return AnnualPlan.objects.filter(worker=self.request.user.worker,
                                             type=self.kwargs['type']).order_by('building', 'date')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["type"] = self.kwargs['type']
        return context


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


class SearchByAnnualPlan(ListView):
    template_name = 'documentation/annual_plan.html'

    def get_queryset(self):
        search = self.request.GET.get("search")
        return AnnualPlan.objects.filter(Q(service__name__icontains=search) |
                                         Q(date__icontains=search) |
                                         Q(worker__full_name__icontains=search) |
                                         Q(status__icontains=search) |
                                         Q(building__street__name__icontains=search)).order_by('date')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["search"] = f"search={self.request.GET.get('search')}&"
        context["type"] = self.kwargs['type']
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_types = self.request.user.worker.position.service_type.all()
        context['form'].fields['service'].queryset = Service.objects.filter(service_type__in=service_types)
        context['form'].fields['date'].widget = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        context['form'].fields['start_time'].widget = forms.TimeInput(attrs={'type': 'time'})
        return context

    def get_initial(self):
        initial = super(CreateScheduleItem, self).get_initial()
        initial['building'] = self.request.GET.get("building")
        return initial

    def get_success_url(self):
        return reverse_lazy('cleaning_schedule')


class CreatePlanItem(CreateView):
    model = AnnualPlan
    template_name = 'documentation/create_plan_item.html'
    fields = ['building', 'service', 'date']

    def form_valid(self, form):
        if form.cleaned_data['date'] < datetime.date.today():
            form.add_error('date', 'Введите правильную дату.')
            return self.form_invalid(form)
        form.instance.user = self.request.user
        form.instance.type = self.kwargs['type']
        return super(CreatePlanItem, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['service'].queryset = Service.objects.filter(service_type__nature=self.kwargs['type'])
        context['form'].fields['date'].widget = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        return context

    def get_initial(self):
        initial = super(CreatePlanItem, self).get_initial()
        initial['building'] = self.request.GET.get("building")
        return initial

    def get_success_url(self):
        return reverse_lazy('annual_plan', kwargs={'type': self.kwargs['type']})


class UpdateScheduleItem(UpdateView):
    model = CleaningSchedule
    template_name = 'documentation/update_planned_work.html'
    fields = ['building', 'service', 'worker', 'date', 'start_time']

    def form_valid(self, form):
        if form.cleaned_data['date'] < datetime.date.today():
            form.add_error('date', 'Введите правильную дату.')
        elif form.cleaned_data['date'] == datetime.date.today() and form.cleaned_data['start_time'] <= datetime.datetime.now().time():
            form.add_error('start_time', 'Введите правильное время.')
        if form.errors:
            return self.form_invalid(form)
        return super(UpdateScheduleItem, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_types = self.request.user.worker.position.service_type.all()
        context['form'].fields['service'].queryset = Service.objects.filter(service_type__in=service_types)
        context['form'].fields['date'].widget = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        context['form'].fields['start_time'].widget = forms.TimeInput(attrs={'type': 'time'})
        return context

    def get_success_url(self):
        return reverse_lazy('cleaning_schedule')


class UpdatePlanItem(UpdateView):
    model = AnnualPlan
    template_name = 'documentation/update_planned_work.html'
    fields = ['building', 'service', 'worker', 'date']

    def form_valid(self, form):
        if form.cleaned_data['date'] < datetime.date.today():
            form.add_error('date', 'Введите правильную дату.')
            return self.form_invalid(form)
        return super(UpdatePlanItem, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['service'].queryset = Service.objects.filter(service_type__nature=self.kwargs['type'])
        context['form'].fields['date'].widget = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        return context

    def get_success_url(self):
        return reverse_lazy('annual_plan', kwargs={'type': self.kwargs['type']})


class ChangeStatus(View):
    def post(self, request, pk):
        if self.request.POST.get("type"):
            item = AnnualPlan.objects.get(id=pk)
        else:
            item = CleaningSchedule.objects.get(id=pk)
        if self.request.POST.get("completed"):
            if item.get_current_date():
                item.status = self.request.POST.get("completed")
        else:
            if item.status == 'Отменена' or item.status == 'Отложена':
                item.status = 'Запланирована'
            else:
                item.status = self.request.POST.get("cancelled")
        item.save(update_fields=['status'])
        if self.request.POST.get("type"):
            return redirect(reverse_lazy('annual_plan', kwargs={'type': self.request.POST.get("type")}))
        return redirect(reverse_lazy('cleaning_schedule'))


class DeleteScheduleItem(DeleteView):
    model = CleaningSchedule

    def get_success_url(self):
        return reverse_lazy('cleaning_schedule')


class DeletePlanItem(DeleteView):
    model = AnnualPlan

    def get_success_url(self):
        return reverse_lazy('annual_plan', kwargs={'type': self.kwargs['type']})


def schedule_export(request):
    previous_date = datetime.datetime.strptime(request.GET.get('previous'), "%Y-%m-%d").date()
    current_date = datetime.datetime.strptime(request.GET.get('current'), "%Y-%m-%d").date()
    if request.GET.get("excel"):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Grafik uborki.xls'
        work_book = xlwt.Workbook(encoding='utf-8')
        sheet = work_book.add_sheet('График уборки')
        row_number = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        labels = ['Улица', 'Дом', 'Услуга', 'Дата', 'Начало в', 'Работник']
        for column_number in range(len(labels)):
            sheet.write(row_number, column_number, labels[column_number], font_style)
        rows = CleaningSchedule.objects.filter(date__gte=previous_date, date__lte=current_date)\
                                       .values_list('building__street__name', 'building__number',
                                                    'service__name', 'date', 'start_time', 'worker__full_name')\
                                       .order_by('building', 'date')
        form_rows_to_excel(rows, sheet, row_number)
        work_book.save(response)
        return response
    else:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename=Grafik uborki.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        schedule = CleaningSchedule.objects.filter(date__gte=previous_date, date__lte=current_date)\
                                           .order_by('building', 'date')
        html_string = render_to_string('requests/pdf_output.html', {'schedule': schedule})
        html = HTML(string=html_string)
        result = html.write_pdf()
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output.seek(0)
            response.write(output.read())
        return response


def plan_export(request):
    previous_date = datetime.datetime.strptime(request.GET.get('previous'), "%Y-%m-%d").date()
    current_date = datetime.datetime.strptime(request.GET.get('current'), "%Y-%m-%d").date()
    if request.GET.get("excel"):
        response = HttpResponse(content_type='application/ms-excel')
        if request.GET.get('type') == 'Благоустройство':
            response['Content-Disposition'] = 'attachment; filename=Plan blagoustroystva.xls'
        else:
            response['Content-Disposition'] = 'attachment; filename=Plan remonta.xls'
        work_book = xlwt.Workbook(encoding='utf-8')
        if request.GET.get('type') == 'Благоустройство':
            sheet = work_book.add_sheet('План благоустройства')
        else:
            sheet = work_book.add_sheet('План ремонтных работ')
        row_number = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        labels = ['Улица', 'Дом', 'Услуга', 'Дата', 'Работник']
        for column_number in range(len(labels)):
            sheet.write(row_number, column_number, labels[column_number], font_style)
        rows = AnnualPlan.objects.filter(date__gte=previous_date, date__lte=current_date,
                                         type=request.GET.get('type'))\
                                 .values_list('building__street__name', 'building__number',
                                              'service__name', 'date', 'worker__full_name')\
                                 .order_by('building', 'date')
        form_rows_to_excel(rows, sheet, row_number)
        work_book.save(response)
        return response
    else:
        response = HttpResponse(content_type='application/pdf')
        if request.GET.get('type') == 'Благоустройство':
            response['Content-Disposition'] = 'inline; attachment; filename=Plan blagoustroystva.pdf'
        else:
            response['Content-Disposition'] = 'inline; attachment; filename=Plan remonta.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        plan = AnnualPlan.objects.filter(date__gte=previous_date, date__lte=current_date,
                                         type=request.GET.get('type')).order_by('building', 'date')
        html_string = render_to_string('requests/pdf_output.html', {'plan': plan, 'type': request.GET.get('type')})
        html = HTML(string=html_string)
        result = html.write_pdf()
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output.seek(0)
            response.write(output.read())
        return response


def form_rows_to_excel(rows, sheet, row_number):
    font_style = xlwt.XFStyle()
    for row in rows:
        row_number += 1
        for column_number in range(len(row)):
            width = sheet.col(column_number).width
            if (len(str(row[column_number])) * 265) > width:
                sheet.col(column_number).width = (len(str(row[column_number])) * 265)
            sheet.write(row_number, column_number, str(row[column_number]), font_style)
    return row_number
