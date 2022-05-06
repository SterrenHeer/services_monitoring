from django.contrib import admin
from .models import Request, RequestComment, Comment


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('service', 'tenant', 'start_time', 'end_time', 'submission_date',
                    'completion_date', 'status', 'answer', 'worker')


@admin.register(RequestComment)
class RequestCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'status', 'submission_date', 'request', 'answer')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'status', 'submission_date', 'completion_date', 'service', 'tenant', 'answer')
