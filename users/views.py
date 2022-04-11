from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.models import Group, User
from users.models import Tenant
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.views.generic import UpdateView
from django.urls import reverse_lazy


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            patronymic = form.cleaned_data.get("patronymic")
            signup_user = User.objects.get(username=username)
            user_group = Group.objects.get(name='Tenant')
            user_group.user_set.add(signup_user)
            Tenant.objects.filter(full_name=' '.join([last_name, first_name, patronymic])).update(user=signup_user)
    else:
        form = SignUpForm()
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
                return redirect('home_page')
            else:
                return redirect('signup')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('login')


def home_page(request):
    return render(request, 'users/home_page.html')


class TenantUpdate(UpdateView):
    model = Tenant
    template_name = 'users/update_tenant.html'
    fields = ['full_name', 'contact_details', 'apartment']

    def get_success_url(self):
        return reverse_lazy('all_requests')
