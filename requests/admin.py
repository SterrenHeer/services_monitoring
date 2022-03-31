from django.contrib import admin
from .models import Request, RequestComment, Comment, Recommendation

admin.site.register(Request)
admin.site.register(RequestComment)
admin.site.register(Comment)
admin.site.register(Recommendation)
