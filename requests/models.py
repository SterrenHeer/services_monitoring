import datetime
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from users.models import Worker
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class Request(models.Model):
    STATUS_CHOICES = (
        ('На рассмотрении', 'На рассмотрении'),
        ('В обработке', 'В обработке'),
        ('Принята', 'Принята'),
        ('Отклонена', 'Отклонена'),
        ('Отложена', 'Отложена'),
        ('Выполнена', 'Выполнена'),
    )
    service = models.ForeignKey('documentation.Service', on_delete=models.CASCADE, verbose_name="Услуга")
    tenant = models.ForeignKey('users.Tenant', on_delete=models.CASCADE, verbose_name="Жилец")
    worker = models.ForeignKey('users.Worker', on_delete=models.SET_NULL,
                               null=True, blank=True, verbose_name="Работник")
    submission_date = models.DateField("Дата подачи", auto_now_add=True)
    completion_date = models.DateField("Дата выполнения", null=True, blank=True)
    status = models.CharField("Состояние", max_length=200, choices=STATUS_CHOICES,
                              default="На рассмотрении")
    start_time = models.TimeField("Время начала", default=timezone.now)
    end_time = models.TimeField("Время завершения", default=timezone.now)
    answer = models.CharField("Ответ", max_length=85, null=True, blank=True)

    class Meta:
        verbose_name = 'заявку'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f"{self.service}"

    def get_absolute_url(self):
        return reverse('request_details', args=[str(self.id)])

    def get_comments(self):
        return self.requestcomment_set.filter(initial__isnull=True)

    def get_workers(self):
        return Worker.objects.exclude(position__name__icontains='Мастер')\
                             .filter(position__service_type=self.service.service_type)

    def get_complaint(self):
        return self.requestcomment_set.exclude(status__in=['Устранено', 'Ответ', 'Отклонено', 'Отзыв']).exists()

    def get_valid_date(self):
        if self.completion_date:
            return datetime.date.today() <= self.completion_date + datetime.timedelta(days=3)

    def get_overdue(self):
        return datetime.date.today() > self.submission_date + datetime.timedelta(days=7)


class RequestComment (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    text = models.CharField("Текст замечания", max_length=600)
    status = models.CharField("Состояние", max_length=200, default="Ответ")
    submission_date = models.DateField("Дата подачи", auto_now_add=True)
    request = models.ForeignKey('Request', on_delete=models.CASCADE, verbose_name="Заявка")
    initial = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True,
                                null=True, verbose_name="Исходный комментарий")
    answer = models.CharField("Ответ", max_length=85, null=True, blank=True)

    class Meta:
        verbose_name = 'комментарий по заявке'
        verbose_name_plural = 'Комментарии по заявкам'

    def __str__(self):
        return f"{self.text} ({self.request})"

    def get_summary(self):
        if len(self.text) > 130:
            summary = self.text[:130] + '...'
        else:
            summary = self.text
        return summary

    def get_overdue(self):
        return datetime.date.today() > self.submission_date + datetime.timedelta(days=3)


class Comment(models.Model):
    text = models.CharField("Текст замечания", max_length=85)
    status = models.CharField("Состояние", max_length=200, default="На рассмотрении")
    submission_date = models.DateField("Дата подачи", auto_now_add=True)
    completion_date = models.DateField("Дата выполнения", null=True, blank=True)
    service = models.ForeignKey('documentation.Service', on_delete=models.CASCADE, verbose_name="Услуга")
    tenant = models.ForeignKey('users.Tenant', on_delete=models.CASCADE, verbose_name="Жилец")
    worker = models.ForeignKey('users.Worker', on_delete=models.SET_NULL, null=True,
                               blank=True, verbose_name="Работник")
    answer = models.CharField("Ответ", max_length=85, null=True, blank=True)
    image = models.ImageField("Фотография", upload_to='comments', blank=True)

    class Meta:
        verbose_name = 'замечание'
        verbose_name_plural = 'Замечания'

    def __str__(self):
        return f"{self.text} ({self.service})"

    def get_workers(self):
        return Worker.objects.filter(position__service_type=self.service.service_type)

    def get_overdue(self):
        return datetime.date.today() > self.submission_date + datetime.timedelta(days=7)


@receiver(pre_delete, sender=Comment)
def comment_model_delete(sender, instance, **kwargs):
    if instance.image.name:
        instance.image.delete(False)
