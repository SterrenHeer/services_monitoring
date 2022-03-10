from django.shortcuts import render
from .forms import SignUpForm
from django.contrib.auth.models import Group, User


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            user_group = Group.objects.get(name='Tenant')
            user_group.user_set.add(signup_user)
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def tenant_home_page(request):
    return render(request, 'users/tenant_home_page.html')
