from django.contrib import admin
from .models import Request, RequestComment, Comment

admin.site.register(Request)
admin.site.register(RequestComment)
admin.site.register(Comment)
