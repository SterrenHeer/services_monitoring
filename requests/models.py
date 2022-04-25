from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from users.models import Worker
import datetime


class Request(models.Model):
    STATUS_CHOICES = (
        ('На рассмотрении', 'На рассмотрении'),
        ('В обработке', 'В обработке'),
        ('Принята', 'Принята'),
        ('Отклонена', 'Отклонена'),
        ('Отложена', 'Отложена'),
        ('Выполнена', 'Выполнена'),
    )
    service = models.ForeignKey('documentation.Service', on_delete=models.CASCADE)
    tenant = models.ForeignKey('users.Tenant', on_delete=models.CASCADE)
    worker = models.ForeignKey('users.Worker', on_delete=models.SET_NULL, null=True, blank=True)
    submission_date = models.DateField(auto_now_add=True)
    completion_date = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="На рассмотрении", help_text="Введите статус заявки")
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)
    answer = models.CharField(max_length=85, null=True, blank=True)

    def __str__(self):
        return f"{self.service}"

    def get_absolute_url(self):
        return reverse('request_details', args=[str(self.id)])

    def get_comments(self):
        return self.requestcomment_set.filter(initial__isnull=True)

    def get_workers(self):
        return Worker.objects.filter(position__service_type=self.service.service_type)

    def get_complaint(self):
        return self.requestcomment_set.exclude(status__in=['Устранено', 'Ответ', 'Отклонено']).exists()


class RequestComment (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=600, help_text="Введите комментарий")
    status = models.CharField(max_length=200, default="Ответ", help_text="Введите статус заявки")
    submission_date = models.DateField(auto_now_add=True)
    request = models.ForeignKey('Request', on_delete=models.CASCADE)
    initial = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    answer = models.CharField(max_length=85, null=True, blank=True)

    def __str__(self):
        return f"{self.text} ({self.request})"

    def get_summary(self):
        if len(self.text) > 130:
            summary = self.text[:130] + '...'
        else:
            summary = self.text
        return summary


class Comment(models.Model):
    text = models.CharField(max_length=85, help_text="Введите комментарий длиной не более 85 символов")
    status = models.CharField(max_length=200, default="На рассмотрении", help_text="Введите статус заявки")
    submission_date = models.DateField(auto_now_add=True)
    completion_date = models.DateField(default=datetime.date.today)
    service = models.ForeignKey('documentation.Service', on_delete=models.CASCADE)
    tenant = models.ForeignKey('users.Tenant', on_delete=models.CASCADE)
    worker = models.ForeignKey('users.Worker', on_delete=models.SET_NULL, null=True, blank=True)
    answer = models.CharField(max_length=85, null=True, blank=True)

    def __str__(self):
        return f"{self.text} ({self.service})"

    def get_workers(self):
        return Worker.objects.filter(position__service_type=self.service.service_type)


class Recommendation(models.Model):
    service = models.ForeignKey('documentation.Service', on_delete=models.SET_NULL, null=True)
    building = models.ForeignKey('documentation.Building', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.service} ({self.building})"
