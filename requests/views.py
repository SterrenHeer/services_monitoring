from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Request, RequestComment, Comment
from documentation.models import Service
from users.models import Tenant
from django.views.generic.base import View
from .forms import RequestCommentForm, RequestForm, CommentForm
from django.db.models import Q
from django.http import HttpResponse
import xlwt
import datetime
from weasyprint import HTML
from django.template.loader import render_to_string
import tempfile


class RequestCommentsListView(ListView):
    model = RequestComment
    template_name = 'requests/request_comments_list.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            if not self.request.GET.get('status'):
                return RequestComment.objects.exclude(Q(status='Ответ') |
                                                      Q(status='На рассотрении') |
                                                      Q(status='Отзыв')).order_by('submission_date')
            return RequestComment.objects.filter(status=self.request.GET.get('status')).order_by('-submission_date')
        elif self.request.user.groups.filter(name='Tenant').exists():
            if not self.request.GET.get('status'):
                return RequestComment.objects.exclude(Q(status='Ответ') |
                                                      Q(status='Отзыв')).filter(user=self.request.user)\
                                             .order_by('-submission_date')
            else:
                if self.request.GET.get('status') == 'Ответ':
                    user_comments = RequestComment.objects.filter(user=self.request.user).values('id')
                    return RequestComment.objects.filter(initial_id__in=user_comments).order_by('-submission_date')
                return RequestComment.objects.filter(user=self.request.user,
                                                     status=self.request.GET.get('status')).order_by('-submission_date')
        if self.request.user.groups.filter(name='Worker').exists():
            return RequestComment.objects.filter(request__worker=self.request.user.worker,
                                                 status__in=['Принято к устранению', 'Отложено', 'Устранено'])\
                                 .order_by('-submission_date')

    @staticmethod
    def get_statuses():
        return RequestComment.objects.exclude(Q(status='Ответ') |
                                              Q(status='На рассмотрении') |
                                              Q(status='Отзыв')).values('status').distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["status"] = ''.join([f"status={x}&" for x in self.request.GET.getlist("status")])
        context["complaints_count"] = RequestComment.objects.filter(status='На рассмотрении').count()
        return context


class AllRequestsListView(ListView):
    model = Request
    template_name = 'requests/requests_list.html'
    paginate_by = 10

    def get_statuses(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return Request.objects.all().values('status').distinct()
        elif self.request.user.groups.filter(name='Tenant').exists():
            return Request.objects.filter(tenant=self.request.user.tenant).values('status').distinct()
        elif self.request.user.groups.filter(name='Master').exists():
            service_types = self.request.user.worker.position.service_type.all()
            return Request.objects.exclude(Q(status='На рассмотрении') |
                                           Q(status='Отклонена')).filter(service__service_type__in=service_types)\
                                  .values('status').distinct()
        elif self.request.user.groups.filter(name='Worker').exists():
            return Request.objects.filter(worker=self.request.user.worker).values('status').distinct()

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            if not self.request.GET.get('status'):
                return Request.objects.all().order_by('submission_date')
            return Request.objects.filter(status=self.request.GET.get('status')).order_by('submission_date')
        elif self.request.user.groups.filter(name='Tenant').exists():
            if not self.request.GET.get('status'):
                return Request.objects.filter(tenant=self.request.user.tenant).order_by('submission_date')
            return Request.objects.filter(tenant=self.request.user.tenant,
                                          status=self.request.GET.get('status')).order_by('submission_date')
        elif self.request.user.groups.filter(name='Master').exists():
            service_types = self.request.user.worker.position.service_type.all()
            if not self.request.GET.get('status'):
                return Request.objects.exclude(Q(status='На рассмотрении') |
                                               Q(status='Отклонена'))\
                                      .filter(service__service_type__in=service_types)\
                                      .order_by('submission_date')
            return Request.objects.filter(service__service_type__in=service_types,
                                          status=self.request.GET.get('status')).order_by('submission_date')
        elif self.request.user.groups.filter(name='Worker').exists():
            if not self.request.GET.get('status'):
                return Request.objects.filter(worker=self.request.user.worker).order_by('submission_date')
            return Request.objects.filter(worker=self.request.user.worker,
                                          status=self.request.GET.get('status')).order_by('submission_date')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["status"] = ''.join([f"status={x}&" for x in self.request.GET.getlist("status")])
        return context


class CommentListView(ListView):
    model = Comment
    template_name = 'requests/comments_list.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.groups.filter(name='Tenant').exists():
            return Comment.objects.filter(tenant=self.request.user.tenant).order_by('submission_date')
        elif self.request.user.groups.filter(name='Master').exists():
            service_types = self.request.user.worker.position.service_type.all()
            return Comment.objects.exclude(status='Выполнена').filter(service__service_type__in=service_types).order_by('submission_date')
        elif self.request.user.groups.filter(name='Worker').exists():
            return Comment.objects.filter(worker=self.request.user.worker).order_by('submission_date')


class RequestDetailView(DetailView):
    model = Request


class CreateRequest(CreateView):
    model = Request
    template_name = 'requests/create_request.html'
    fields = ['service', 'start_time', 'end_time']

    def form_valid(self, form):
        if form.cleaned_data['start_time'] >= form.cleaned_data['end_time']:
            form.add_error('start_time', 'Введите правильное время.')
            return self.form_invalid(form)
        form.instance.tenant = Tenant.objects.get(user=self.request.user)
        return super(CreateRequest, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['service'].queryset = Service.objects.filter(service_type__nature='Заявка')
        return context


class CreateComment(CreateView):
    model = Comment
    template_name = 'requests/create_comment.html'
    fields = ['text', 'service']

    def form_valid(self, form):
        form.instance.tenant = Tenant.objects.get(user=self.request.user)
        return super(CreateComment, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['service'].queryset = Service.objects.filter(service_type__nature__in=['Замечание', 'Уборка'])
        return context

    def get_success_url(self):
        return reverse_lazy('comments')


class ManagerRequestCreate(CreateView):
    model = Request
    template_name = 'requests/create_request.html'
    fields = ['tenant', 'service', 'start_time', 'end_time']

    def form_valid(self, form):
        if form.cleaned_data['start_time'] >= form.cleaned_data['end_time']:
            form.add_error('start_time', 'Введите правильное время.')
            return self.form_invalid(form)
        return super(ManagerRequestCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['service'].queryset = Service.objects.filter(service_type__nature='Заявка')
        return context


class UpdateRequest(UpdateView):
    model = Request
    template_name = 'requests/update_request.html'
    fields = ['service', 'start_time', 'end_time']

    def form_valid(self, form):
        if form.cleaned_data['start_time'] >= form.cleaned_data['end_time']:
            form.add_error('start_time', 'Введите правильное время.')
            return self.form_invalid(form)
        return super(UpdateRequest, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['service'].queryset = Service.objects.filter(service_type__nature='Заявка')
        return context


class ManagerUpdateRequest(UpdateView):
    model = Request
    template_name = 'requests/update_request.html'
    fields = ['status', 'start_time', 'end_time']

    def form_valid(self, form):
        if form.cleaned_data['start_time'] >= form.cleaned_data['end_time']:
            form.add_error('start_time', 'Введите правильное время.')
            return self.form_invalid(form)
        return super(ManagerUpdateRequest, self).form_valid(form)


class WorkWithRequestComment(View):
    def post(self, request, pk):
        form = RequestCommentForm(request.POST)
        request = Request.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.request = request
            form.user = self.request.user
            if self.request.POST.get("status"):
                form.status = self.request.POST.get("status")
            if self.request.POST.get("initial"):
                initial_comment = RequestComment.objects.get(id=int(self.request.POST.get("initial")))
                if self.request.POST.get("new_status") and self.request.POST.get("text"):
                    form.initial_id = initial_comment.id
                    initial_comment.status = self.request.POST.get("new_status")
                    initial_comment.save(update_fields=['status'])
                elif self.request.POST.get("text"):
                    initial_comment.text = self.request.POST.get("text")
                    initial_comment.save(update_fields=['text'])
                    return redirect(request.get_absolute_url())
            form.save()
        return redirect(request.get_absolute_url())


class WorkerAppointment(View):
    def post(self, request, pk):
        if self.request.POST.get("comment"):
            form = CommentForm(request.POST)
            comment = Comment.objects.get(id=pk)
            if form.is_valid():
                if self.request.POST.get("worker"):
                    comment.worker_id = self.request.POST.get("worker")
                    comment.status = 'Принято'
                else:
                    comment.worker_id = None
                    comment.status = 'На рассмотрении'
                comment.save(update_fields=['worker', 'status'])
            return redirect(reverse_lazy('comments'))
        else:
            form = RequestForm(request.POST)
            request = Request.objects.get(id=pk)
            if form.is_valid():
                if self.request.POST.get("worker"):
                    request.worker_id = self.request.POST.get("worker")
                    request.status = 'Принята'
                else:
                    request.worker_id = None
                    request.status = 'В обработке'
                request.save(update_fields=['worker', 'status'])
            return redirect(reverse_lazy('all_requests'))


class ChangeStatus(View):
    def post(self, request, pk):
        if self.request.POST.get("request_comment") or self.request.POST.get("comment"):
            if self.request.POST.get("request_comment"):
                comment = RequestComment.objects.get(id=pk)
            else:
                comment = Comment.objects.get(id=pk)
            if self.request.POST.get("status"):
                comment.status = self.request.POST.get("status")
                if self.request.POST.get("comment") and comment.status == "Выполнена":
                    comment.completion_date = datetime.date.today()
                else:
                    comment.completion_date = None
                if self.request.POST.get("answer"):
                    comment.answer = self.request.POST.get("answer")
                else:
                    comment.answer = None
                comment.save()
            if self.request.POST.get("request_comment"):
                return redirect(reverse_lazy('request_comments'))
            return redirect(reverse_lazy('comments'))
        else:
            request = Request.objects.get(id=pk)
            if self.request.POST.get("status"):
                if self.request.POST.get("status") == "Выполнена":
                    if not request.get_complaint():
                        request.status = self.request.POST.get("status")
                        request.completion_date = datetime.date.today()
                else:
                    request.status = self.request.POST.get("status")
                    request.completion_date = None
                if self.request.POST.get("answer"):
                    request.answer = self.request.POST.get("answer")
                else:
                    request.answer = None
                request.save(update_fields=['status', 'answer', 'completion_date'])
            return redirect(reverse_lazy('all_requests'))


class DeleteRequest(DeleteView):
    model = Request

    def get_success_url(self):
        return reverse_lazy('all_requests')


class DeleteRequestComment(DeleteView):
    model = RequestComment

    def get_success_url(self):
        return reverse_lazy('request_details', kwargs={'pk': self.object.request.id})


class DeleteComment(DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse_lazy('comments')


class SearchByRequests(ListView):
    paginate_by = 10
    template_name = 'requests/requests_list.html'

    def get_queryset(self):
        search = self.request.GET.get("search")
        if self.request.user.groups.filter(name='Manager').exists():
            return Request.objects.filter(Q(tenant__full_name__icontains=search) |
                                          Q(service__name__icontains=search) |
                                          Q(submission_date__icontains=search) |
                                          Q(tenant__user__username__icontains=search)).order_by('submission_date')
        if self.request.user.groups.filter(name='Tenant').exists():
            return Request.objects.filter(Q(service__name__icontains=search, tenant=self.request.user.tenant) |
                                          Q(submission_date__icontains=search, tenant=self.request.user.tenant))\
                                  .order_by('submission_date')
        if self.request.user.groups.filter(name='Master').exists():
            service_types = self.request.user.worker.position.service_type.all()
            return Request.objects.exclude(Q(status='На рассмотрении') |
                                           Q(status='Отклонена'))\
                                  .filter(Q(service__name__icontains=search, service__service_type__in=service_types) |
                                          Q(submission_date__icontains=search, service__service_type__in=service_types))\
                                  .order_by('submission_date')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["search"] = f"search={self.request.GET.get('search')}&"
        return context


def export_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Akt za ' + str(datetime.date.today()) + '.xls'
    work_book = xlwt.Workbook(encoding='utf-8')
    sheet = work_book.add_sheet('Акт выполненных работ')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Услуга', 'Жилец', 'Дата подачи']
    for col_num in range(len(columns)):
        sheet.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = Request.objects.filter(status='В обработке')\
                          .values_list('service__name', 'tenant__full_name', 'submission_date')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            sheet.write(row_num, col_num, str(row[col_num]), font_style)
    work_book.save(response)
    return response


def export_to_pdf(request):
    file = request.GET.get('file')
    if file == 'request':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename=Akt za ' + str(datetime.date.today()) + '.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        requests = Request.objects.filter(status='Выполнена')
        comments = Comment.objects.filter(status='Выполнена')
        html_string = render_to_string('requests/pdf_output.html', {'requests': requests, 'comments': comments})
        html = HTML(string=html_string)
        result = html.write_pdf()
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output.seek(0)
            response.write(output.read())
        return response
