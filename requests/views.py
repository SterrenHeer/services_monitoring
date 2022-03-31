from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
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
    fields = ['service', 'start_time', 'end_time']

    def form_valid(self, form):
        form.instance.tenant = Tenant.objects.get(user=self.request.user)
        return super(RequestCreate, self).form_valid(form)
