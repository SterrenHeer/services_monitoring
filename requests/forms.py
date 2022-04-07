from django import forms
from .models import RequestComment


class RequestCommentForm(forms.ModelForm):
    class Meta:
        model = RequestComment
        fields = ('text',)
