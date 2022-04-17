from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from users.models import Worker


class Request(models.Model):
    STATUS_CHOICES = (
        ('На рассмотрении', 'На рассмотрении'),
        ('В обработке', 'В обработке'),
        ('Принята', 'Принята'),
        ('Отклонена', 'Отклонена'),
        ('Отложена', 'Отложена'),
        ('В процессе', 'В процессе'),
        ('Выполнена', 'Выполнена'),
    )
    service = models.ForeignKey('documentation.Service', on_delete=models.SET_NULL, null=True)
    tenant = models.ForeignKey('users.Tenant', on_delete=models.SET_NULL, null=True)
    worker = models.ForeignKey('users.Worker', on_delete=models.SET_NULL, null=True, blank=True)
    submission_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="На рассмотрении", help_text="Введите статус заявки")
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)

    def __str__(self):
        return f"{self.service}"

    def get_absolute_url(self):
        return reverse('request_details', args=[str(self.id)])

    def get_comments(self):
        return self.requestcomment_set.filter(initial__isnull=True)

    def get_workers(self):
        return Worker.objects.filter(position__service_type=self.service.service_type)


class RequestComment (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=600, help_text="Введите комментарий")
    status = models.CharField(max_length=200, default="Ответ", help_text="Введите статус заявки")
    submission_date = models.DateField(auto_now_add=True)
    request = models.ForeignKey('Request', on_delete=models.SET_NULL, null=True)
    initial = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.text} ({self.request.service})"

    def get_summary(self):
        if len(self.text) > 130:
            summary = self.text[:130] + '...'
        else:
            summary = self.text
        return summary


class Comment(models.Model):
    comment_text = models.CharField(max_length=600, help_text="Введите комментарий")
    status = models.CharField(max_length=200, default="На рассмотрении", help_text="Введите статус заявки")
    submission_date = models.DateField(auto_now_add=True)
    service = models.ForeignKey('documentation.Service', on_delete=models.SET_NULL, null=True)
    tenant = models.ForeignKey('users.Tenant', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.comment_text} ({self.service})"


class Recommendation(models.Model):
    service = models.ForeignKey('documentation.Service', on_delete=models.SET_NULL, null=True)
    building = models.ForeignKey('documentation.Building', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.service} ({self.building})"
