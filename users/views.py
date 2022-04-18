from django.shortcuts import render, redirect
from .forms import SignUpTenantForm, SignUpWorkerForm
from django.contrib.auth.models import Group, User
from users.models import Tenant, Worker
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.views.generic import UpdateView, ListView
from django.urls import reverse_lazy


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

    def get_success_url(self):
        return reverse_lazy('all_requests')


class WorkersListView(ListView):
    model = Worker
    template_name = 'users/all_users.html'
    paginate_by = 10

    def get_queryset(self):
        service_types = self.request.user.worker.position.service_type.all()
        return Worker.objects.filter(user__isnull=False, position__service_type__in=service_types).distinct()
