from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Request


class TenantRequestsListView(ListView):
    model = Request
    template_name = 'requests/tenant_requests.html'
    paginate_by = 10

    def get_queryset(self):
        return Request.objects.filter(tenant=self.request.user.tenant).order_by('submission_date')


class RequestDetailView(DetailView):
    model = Request
