from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Tenant


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    patronymic = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=250, help_text='eg.youremail.gmail.com')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'patronymic', 'username', 'password1', 'password2', 'email')

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        patronymic = cleaned_data.get("patronymic")

        if not Tenant.objects.filter(full_name=' '.join([last_name, first_name, patronymic])).exists():
            message = "Вы не являетесь жильцом данного участка"
            self.add_error('first_name', message)
            self.add_error('last_name', message)
            self.add_error('patronymic', message)
