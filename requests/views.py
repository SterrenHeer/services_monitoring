from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Request
from users.models import Tenant


class TenantRequestsListView(ListView):
    model = Request
    template_name = 'requests/tenant_requests.html'
    paginate_by = 10

    def get_queryset(self):
        return Request.objects.filter(tenant=self.request.user.tenant).order_by('submission_date')


class RequestDetailView(DetailView):
    model = Request


class RequestCreate(CreateView):
    model = Request
    template_name = 'requests/create_request.html'
    fields = ['service', 'start_time', 'end_time']

    def form_valid(self, form):
        form.instance.tenant = Tenant.objects.get(user=self.request.user)
        return super(RequestCreate, self).form_valid(form)


class RequestUpdate(UpdateView):
    model = Request
    template_name = 'requests/update_request.html'
    fields = ['service', 'start_time', 'end_time']


class RequestDelete(DeleteView):
    model = Request
    success_url = reverse_lazy('tenant_requests')
