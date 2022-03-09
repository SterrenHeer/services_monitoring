from django.contrib import admin
from .models import RepairRequest, RequestComment, Comment, Recommendation

admin.site.register(RepairRequest)
admin.site.register(RequestComment)
admin.site.register(Comment)
admin.site.register(Recommendation)
