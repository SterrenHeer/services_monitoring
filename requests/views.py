from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Request, RequestComment
from users.models import Tenant
from django.views.generic.base import View
from .forms import RequestCommentForm
from django.db.models import Q


class RequestComplaintsListView(ListView):
    model = RequestComment
    template_name = 'requests/request_comments.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            if not self.request.GET.get('status'):
                return RequestComment.objects.exclude(Q(status='Ответ') |
                                                      Q(status='Замечание') |
                                                      Q(status='Отзыв')).order_by('submission_date')
            return RequestComment.objects.filter(status=self.request.GET.get('status')).order_by('submission_date')
        elif self.request.user.groups.filter(name='Tenant').exists():
            if not self.request.GET.get('status'):
                return RequestComment.objects.exclude(Q(status='Ответ') |
                                                      Q(status='Отзыв')).filter(user=self.request.user).order_by('submission_date')
            else:
                if self.request.GET.get('status') == 'Ответ':
                    return RequestComment.objects.filter(
                        initial_id__in=RequestComment.objects.filter(user=self.request.user).values('id'))
                return RequestComment.objects.filter(user=self.request.user,
                                                     status=self.request.GET.get('status')).order_by('submission_date')

    @staticmethod
    def get_statuses():
        return RequestComment.objects.exclude(Q(status='Ответ') |
                                              Q(status='Замечание') |
                                              Q(status='Отзыв')).values('status').distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["status"] = ''.join([f"status={x}&" for x in self.request.GET.getlist("status")])
        context["complaints_count"] = RequestComment.objects.filter(status='Замечание').count()
        return context


class AllRequestsListView(ListView):
    model = Request
    template_name = 'requests/all_requests.html'
    paginate_by = 10

    def get_statuses(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return Request.objects.all().values('status').distinct()
        elif self.request.user.groups.filter(name='Tenant').exists():
            return Request.objects.filter(tenant=self.request.user.tenant).values('status').distinct()

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            if not self.request.GET.get('status'):
                return Request.objects.all().order_by('submission_date')
            else:
                return Request.objects.filter(status=self.request.GET.get('status')).order_by('submission_date')
        elif self.request.user.groups.filter(name='Tenant').exists():
            if not self.request.GET.get('status'):
                return Request.objects.filter(tenant=self.request.user.tenant).order_by('submission_date')
            else:
                return Request.objects.filter(tenant=self.request.user.tenant,
                                              status=self.request.GET.get('status')).order_by('submission_date')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["status"] = ''.join([f"status={x}&" for x in self.request.GET.getlist("status")])
        return context


class RequestDetailView(DetailView):
    model = Request


class CreateRequest(CreateView):
    model = Request
    template_name = 'requests/create_request.html'
    fields = ['service', 'start_time', 'end_time']

    def form_valid(self, form):
        form.instance.tenant = Tenant.objects.get(user=self.request.user)
        return super(CreateRequest, self).form_valid(form)


class ManagerRequestCreate(CreateView):
    model = Request
    template_name = 'requests/create_request.html'
    fields = ['tenant', 'service', 'start_time', 'end_time']


class UpdateRequest(UpdateView):
    model = Request
    template_name = 'requests/update_request.html'
    fields = ['service', 'start_time', 'end_time']


class ManagerUpdateRequest(UpdateView):
    model = Request
    template_name = 'requests/update_request.html'
    fields = ['status', 'start_time', 'end_time']


class WorkWithRequestComment(View):
    def post(self, request, pk):
        form = RequestCommentForm(request.POST)
        request = Request.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.request = request
            print(self.request.POST)
            form.user = self.request.user
            if self.request.POST.get("status", None):
                form.status = self.request.POST.get("status")
            if self.request.POST.get("initial", None):
                initial_comment = RequestComment.objects.get(id=int(self.request.POST.get("initial")))
                if self.request.POST.get("new_status", None) and self.request.POST.get("text", None):
                    form.initial_id = initial_comment.id
                    initial_comment.status = self.request.POST.get("new_status")
                    initial_comment.save(update_fields=['status'])
                elif self.request.POST.get("text", None):
                    initial_comment.text = self.request.POST.get("text")
                    initial_comment.save(update_fields=['text'])
                    return redirect(request.get_absolute_url())
            form.save()
        return redirect(request.get_absolute_url())


class DeleteRequest(DeleteView):
    model = Request

    def get_success_url(self):
        return reverse_lazy('all_requests')


class DeleteRequestComment(DeleteView):
    model = RequestComment

    def get_success_url(self):
        return reverse_lazy('request_details', kwargs={'pk': self.object.request.id})


class Search(ListView):
    paginate_by = 10
    template_name = 'requests/all_requests.html'

    def get_queryset(self):
        search = self.request.GET.get("search")
        self.template_name = 'requests/all_requests.html'
        if self.request.user.groups.filter(name='Manager').exists():
            return Request.objects.filter(Q(tenant__full_name__icontains=search) |
                                          Q(service__name__icontains=search) |
                                          Q(submission_date__icontains=search) |
                                          Q(tenant__user__username__icontains=search)).order_by('submission_date')
        if self.request.user.groups.filter(name='Tenant').exists():
            return Request.objects.filter(Q(service__name__icontains=search) |
                                          Q(submission_date__icontains=search)).order_by('submission_date')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["search"] = f"search={self.request.GET.get('search')}&"
        return context
