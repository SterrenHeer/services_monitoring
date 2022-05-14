import datetime
from django.contrib import admin
from .models import Request, RequestComment, Comment
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
import tempfile
from .views import form_rows_to_excel
import xlwt
from django.db.models import Sum, Max, Min


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('service', 'submission_date', 'completion_date', 'status',
                    'start_time', 'end_time', 'answer', 'tenant', 'worker')
    actions = ['export_pdf', 'export_excel']

    @admin.action(description='Экспортировать данные в Excel')
    def export_excel(self, request, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Akt ot ' + str(datetime.date.today()) + '.xls'
        work_book = xlwt.Workbook(encoding='utf-8')
        sheet = work_book.add_sheet('Акт выполненных работ')
        row_number = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        labels = ['Услуга', 'Стоимость', 'Заказчик', 'Исполнитель', 'Дата подачи', 'Дата выполнения']
        for column_number in range(len(labels)):
            sheet.write(row_number, column_number, labels[column_number], font_style)
        rows = queryset.filter(status='Выполнена')\
                       .values_list('service__name', 'service__price', 'tenant__full_name',
                                    'worker__full_name', 'submission_date', 'completion_date')
        form_rows_to_excel(rows, sheet, row_number)
        work_book.save(response)
        return response

    @admin.action(description='Экспортировать данные в PDF')
    def export_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename=Akt ot ' + str(datetime.date.today()) + '.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        requests = queryset.filter(status='Выполнена').order_by('worker', 'submission_date')
        previous_date = queryset.aggregate(Min('completion_date'))['completion_date__min']
        current_date = queryset.aggregate(Max('completion_date'))['completion_date__max']
        total_requests = requests.aggregate(Sum('service__price'))['service__price__sum']
        html_string = render_to_string('requests/pdf_output.html', {'requests': requests,
                                                                    'total_requests': total_requests,
                                                                    'previous_date': previous_date,
                                                                    'current_date': current_date})
        html = HTML(string=html_string)
        result = html.write_pdf()
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output.seek(0)
            response.write(output.read())
        return response


@admin.register(RequestComment)
class RequestCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'status', 'submission_date', 'request', 'answer')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'status', 'submission_date', 'completion_date', 'service', 'tenant', 'answer')
    actions = ['export_pdf', 'export_excel']

    @admin.action(description='Экспортировать данные в Excel')
    def export_excel(self, request, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Akt ot ' + str(datetime.date.today()) + '.xls'
        work_book = xlwt.Workbook(encoding='utf-8')
        sheet = work_book.add_sheet('Акт выполненных работ')
        row_number = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        labels = ['Услуга', 'Стоимость', 'Заказчик', 'Исполнитель', 'Дата подачи', 'Дата выполнения']
        for column_number in range(len(labels)):
            sheet.write(row_number, column_number, labels[column_number], font_style)
        rows = queryset.filter(status='Выполнена') \
            .values_list('service__name', 'service__price', 'tenant__full_name',
                         'worker__full_name', 'submission_date', 'completion_date')
        form_rows_to_excel(rows, sheet, row_number)
        work_book.save(response)
        return response

    @admin.action(description='Экспортировать данные в PDF')
    def export_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename=Akt ot ' + str(datetime.date.today()) + '.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        comments = queryset.filter(status='Выполнена').order_by('worker', 'submission_date')
        previous_date = queryset.aggregate(Min('completion_date'))['completion_date__min']
        current_date = queryset.aggregate(Max('completion_date'))['completion_date__max']
        total_comments = comments.aggregate(Sum('service__price'))['service__price__sum']
        html_string = render_to_string('requests/pdf_output.html', {'comments': comments,
                                                                    'total_comments': total_comments,
                                                                    'previous_date': previous_date,
                                                                    'current_date': current_date})
        html = HTML(string=html_string)
        result = html.write_pdf()
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output.seek(0)
            response.write(output.read())
        return response
