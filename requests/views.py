from django.shortcuts import render
from django.views.generic import ListView
from .models import RepairRequest


class TenantRequestsListView(ListView):
    model = RepairRequest
    template_name = 'requests/tenant_requests.html'
    paginate_by = 10

    def get_queryset(self):
        return RepairRequest.objects.filter(tenant=self.request.user.tenant).order_by('submission_date')
