from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tenant, Worker


class SignUpTenantForm(UserCreationForm):
    last_name = forms.CharField(max_length=100, required=True, label='Фамилия')
    first_name = forms.CharField(max_length=100, required=True, label='Имя')
    patronymic = forms.CharField(max_length=100, required=True, label='Отчество')
    email = forms.EmailField(max_length=250, help_text='eg.youremail.gmail.com', label='Электронная почта')

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'patronymic', 'username', 'password1', 'password2', 'email')

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        patronymic = cleaned_data.get("patronymic")

        if not Tenant.objects.filter(full_name=' '.join([last_name, first_name, patronymic])).exists():
            message = "Вы не являетесь жильцом данного участка."
            self.add_error('first_name', message)
            self.add_error('last_name', message)
            self.add_error('patronymic', message)


class SignUpWorkerForm(UserCreationForm):
    last_name = forms.CharField(max_length=100, required=True, label='Фамилия')
    first_name = forms.CharField(max_length=100, required=True, label='Имя')
    patronymic = forms.CharField(max_length=100, required=True, label='Отчество')

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'patronymic', 'username', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        patronymic = cleaned_data.get("patronymic")

        if not Worker.objects.filter(full_name=' '.join([last_name, first_name, patronymic])).exists():
            message = "Данный работник не зарегистрирован в базе"
            self.add_error('first_name', message)
            self.add_error('last_name', message)
            self.add_error('patronymic', message)


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ('position',)
