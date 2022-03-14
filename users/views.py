from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.models import Group, User
from users.models import Tenant
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            user_group = Group.objects.get(name='Tenant')
            user_group.user_set.add(signup_user)
            Tenant.objects.create(user=signup_user, full_name=username)
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
                if user.groups.filter(name='Tenant').exists():
                    return redirect('tenant_home_page')
                if user.groups.filter(name='Master').exists():
                    return redirect('master_home_page')
            else:
                return redirect('signup')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def tenant_home_page(request):
    return render(request, 'users/tenant_home_page.html')


def master_home_page(request):
    return render(request, 'users/master_home_page.html')
