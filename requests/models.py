from django.db import models
from django.utils import timezone


class RepairRequest(models.Model):
    service = models.ForeignKey('documentation.Service', on_delete=models.SET_NULL, null=True)
    tenant = models.ForeignKey('documentation.Tenant', on_delete=models.SET_NULL, null=True)
    submission_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=200, default="На рассмотрении", help_text="Введите статус заявки")
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)

    def __str__(self):
        return f"{self.service}"


class RequestComment (models.Model):
    comment_text = models.CharField(max_length=200, help_text="Введите комментарий")
    status = models.CharField(max_length=200, default="На рассмотрении", help_text="Введите статус заявки")
    submission_date = models.DateField(auto_now_add=True)
    request = models.ForeignKey('RepairRequest', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.comment_text} ({self.request.service})"


class Comment(models.Model):
    comment_text = models.CharField(max_length=200, help_text="Введите комментарий")
    status = models.CharField(max_length=200, default="На рассмотрении", help_text="Введите статус заявки")
    submission_date = models.DateField(auto_now_add=True)
    service = models.ForeignKey('documentation.Service', on_delete=models.SET_NULL, null=True)
    tenant = models.ForeignKey('documentation.Tenant', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.comment_text} ({self.service})"


class Recommendation(models.Model):
    service = models.ForeignKey('documentation.Service', on_delete=models.SET_NULL, null=True)
    building = models.ForeignKey('documentation.Building', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.service} ({self.building})"


