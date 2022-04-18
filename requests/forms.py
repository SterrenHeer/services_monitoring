from django import forms
from .models import RequestComment, Request, Comment


class RequestCommentForm(forms.ModelForm):
    class Meta:
        model = RequestComment
        fields = ('text',)


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('worker',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('worker',)
