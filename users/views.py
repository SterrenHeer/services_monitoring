from django.shortcuts import render, redirect
from .forms import SignUpTenantForm, SignUpWorkerForm, WorkerForm
from django.contrib.auth.models import Group, User
from users.models import Tenant, Worker
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.views.generic import UpdateView, ListView
from django.urls import reverse_lazy
from django.views.generic.base import View
import re


def sign_up(request):
    if request.method == 'POST':
        if request.user.groups.filter(name='Master').exists():
            form = SignUpWorkerForm(request.POST)
        else:
            form = SignUpTenantForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            patronymic = form.cleaned_data.get("patronymic")
            signup_user = User.objects.get(username=username)
            if request.user.groups.filter(name='Master').exists():
                user_group = Group.objects.get(name='Worker')
                user_group.user_set.add(signup_user)
                Worker.objects.filter(full_name=' '.join([last_name, first_name, patronymic])).update(user=signup_user)
            else:
                user_group = Group.objects.get(name='Tenant')
                user_group.user_set.add(signup_user)
                Tenant.objects.filter(full_name=' '.join([last_name, first_name, patronymic])).update(user=signup_user)
    else:
        if request.user.groups.filter(name='Master').exists():
            form = SignUpWorkerForm()
        else:
            form = SignUpTenantForm()
    return render(request, 'users/signup.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.user.groups.filter(name='Master').exists() and not request.user.has_perm(
                        'requests.change_repairrequest'):
                    return redirect('comments')
                else:
                    return redirect('all_requests')
            else:
                return redirect('signup')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('login')


class TenantUpdate(UpdateView):
    model = Tenant
    template_name = 'users/update_tenant.html'
    fields = ['full_name', 'contact_details', 'apartment']

    def form_valid(self, form):
        regex = '^(\+375|80)(29|25|44|33)(\d{3})(\d{2})(\d{2})$'
        if re.match(regex, form.cleaned_data['contact_details']) is None:
            form.add_error('contact_details', 'Введите номер в правильном формате.')
            return self.form_invalid(form)
        return super(TenantUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('all_requests')


class WorkersListView(ListView):
    model = Worker
    template_name = 'users/worker_list.html'
    paginate_by = 10

    def get_queryset(self):
        service_types = self.request.user.worker.position.service_type.all()
        return Worker.objects.filter(user__isnull=False, position__service_type__in=service_types).distinct()


class PositionChanging(View):
    def post(self, request, pk):
        form = WorkerForm(request.POST)
        worker = Worker.objects.get(id=pk)
        if form.is_valid():
            if self.request.POST.get("position"):
                worker.position_id = self.request.POST.get("position")
                worker.save()
        return redirect(reverse_lazy('all_workers'))
