import datetime
from django.contrib import admin
from .models import Street, Building, Apartment, ServiceType, Service, Equipment, Position, CleaningSchedule, AnnualPlan
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
import tempfile
from .views import form_rows_to_excel
import xlwt


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('number', 'street', 'apartments_quantity')
    list_filter = (('street', admin.RelatedOnlyFieldListFilter),)


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('building', 'apartment_number', 'area', 'tenants_quantity')
    list_filter = (('building', admin.RelatedOnlyFieldListFilter),)


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'nature')
    list_filter = ('nature',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'equipment_titles', 'service_type')
    list_filter = (('service_type', admin.RelatedOnlyFieldListFilter),)
    search_fields = ('name',)
    filter_horizontal = ('equipment',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_types_titles')
    search_fields = ('name', 'service_type__title')
    filter_horizontal = ('service_type',)


@admin.register(CleaningSchedule)
class CleaningScheduleAdmin(admin.ModelAdmin):
    list_display = ('building', 'date', 'service', 'status', 'start_time', 'worker')
    list_filter = (('service__service_type', admin.RelatedOnlyFieldListFilter),
                   ('building', admin.RelatedOnlyFieldListFilter), 'date', 'status')
    search_fields = ('service__name', 'worker__full_name')
    actions = ['export_pdf', 'export_excel']

    @admin.action(description='Экспортировать данные в Excel')
    def export_excel(self, request, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Grafik uborki ot ' + str(datetime.date.today()) + '.xls'
        work_book = xlwt.Workbook(encoding='utf-8')
        sheet = work_book.add_sheet('График уборки')
        row_number = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        labels = ['Улица', 'Дом', 'Услуга', 'Дата', 'Начало в', 'Работник']
        for column_number in range(len(labels)):
            sheet.write(row_number, column_number, labels[column_number], font_style)
        rows = queryset.values_list('building__street__name', 'building__number', 'service__name',
                                    'date', 'start_time', 'worker__full_name').order_by('building', 'date')
        form_rows_to_excel(rows, sheet, row_number)
        work_book.save(response)
        return response

    @admin.action(description='Экспортировать данные в PDF')
    def export_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename=Grafik uborki ot ' + str(
            datetime.date.today()) + '.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        html_string = render_to_string('requests/pdf_output.html', {'schedule': queryset})
        html = HTML(string=html_string)
        result = html.write_pdf()
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output.seek(0)
            response.write(output.read())
        return response


@admin.register(AnnualPlan)
class AnnualPlanAdmin(admin.ModelAdmin):
    list_display = ('building', 'service', 'date', 'status', 'type', 'worker')
    list_filter = ('type', ('service__service_type', admin.RelatedOnlyFieldListFilter), 'date',
                   'status', ('building', admin.RelatedOnlyFieldListFilter))
    search_fields = ('service__name', 'worker__full_name')
    actions = ['approve', 'export_pdf', 'export_excel']

    @admin.action(description='Утвердить к выполнению')
    def approve(self, request, queryset):
        queryset.filter(status='Запланирована').update(status='Утверждена')

    @admin.action(description='Экспортировать данные в Excel')
    def export_excel(self, request, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Plan rabot ot ' + str(datetime.date.today()) + '.xls'
        work_book = xlwt.Workbook(encoding='utf-8')
        sheet = work_book.add_sheet('План работ')
        row_number = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        labels = ['Улица', 'Дом', 'Услуга', 'Дата', 'Работник']
        for column_number in range(len(labels)):
            sheet.write(row_number, column_number, labels[column_number], font_style)
        rows = queryset.values_list('building__street__name', 'building__number', 'service__name',
                                    'date', 'worker__full_name').order_by('building', 'date')
        form_rows_to_excel(rows, sheet, row_number)
        work_book.save(response)
        return response

    @admin.action(description='Экспортировать данные в PDF')
    def export_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename=Plan rabot ot ' + str(
            datetime.date.today()) + '.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        plan = queryset.order_by('building', 'date')
        html_string = render_to_string('requests/pdf_output.html', {'plan': plan})
        html = HTML(string=html_string)
        result = html.write_pdf()
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output.seek(0)
            response.write(output.read())
        return response
