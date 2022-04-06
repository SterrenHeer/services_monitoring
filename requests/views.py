from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Request
from users.models import Tenant
from django.contrib.auth.models import Group, User


class TenantRequestsListView(ListView):
    model = Request
    template_name = 'requests/tenant_requests.html'
    paginate_by = 10

    def get_queryset(self):
        return Request.objects.filter(tenant=self.request.user.tenant).order_by('submission_date')


class AllRequestsListView(ListView):
    model = Request
    template_name = 'requests/all_requests.html'
    paginate_by = 10
    order_by = 'submission_date'

    def get_statuses(self):
        return Request.objects.all().values('status').distinct()

    def get_queryset(self):
        if not self.request.GET.get('status'):
            return Request.objects.all()
        else:
            return Request.objects.filter(status=self.request.GET.get('status'))

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


class DeleteRequest(DeleteView):
    model = Request

    def get_success_url(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return reverse_lazy('all_requests')
        username = self.object.tenant.user.username
        return reverse_lazy('tenant_requests', kwargs={'pk': username})
