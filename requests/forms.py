from django import forms
from .models import RequestComment, Request


class RequestCommentForm(forms.ModelForm):
    class Meta:
        model = RequestComment
        fields = ('text',)


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('worker',)
