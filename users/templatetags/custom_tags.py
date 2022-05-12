from datetime import date, timedelta
from django import template
from django.contrib.auth.models import Group
from django.db.models import Q
from users.models import Worker
from requests.models import Request, RequestComment
from django.db.models import Sum

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@register.simple_tag
def get_worker(name):
    return Worker.objects.get(full_name=name)


@register.simple_tag
def get_requests_statuses(user):
    if user.groups.filter(name='Manager').exists():
        return Request.objects.all().values('status').distinct()
    elif user.groups.filter(name='Tenant').exists():
        return Request.objects.filter(tenant=user.tenant).values('status').distinct()
    elif user.groups.filter(name='Master').exists():
        service_types = user.worker.position.service_type.all()
        return Request.objects.exclude(Q(status='На рассмотрении') |
                                       Q(status='Отклонена')).filter(service__service_type__in=service_types)\
                              .values('status').distinct()
    elif user.groups.filter(name='Worker').exists():
        return Request.objects.filter(worker=user.worker).values('status').distinct()


@register.simple_tag
def get_complaints_count():
    return RequestComment.objects.filter(status='На рассмотрении').count()


@register.simple_tag
def get_request_comment_statuses():
    return RequestComment.objects.exclude(Q(status='Ответ') |
                                          Q(status='Отзыв')).values('status').distinct()


@register.simple_tag
def get_current_date():
    return date.today().strftime('%Y-%m-%d')


@register.simple_tag
def get_previous_date():
    return (date.today() - timedelta(days=31)).strftime('%Y-%m-%d')


@register.simple_tag
def get_requests_sum(worker, previous_date, current_date):
    return worker.request_set.filter(completion_date__gte=previous_date, completion_date__lte=current_date,
                                     status='Выполнена').aggregate(Sum('service__price'))['service__price__sum']


@register.simple_tag
def get_comments_sum(worker, previous_date, current_date):
    return worker.comment_set.filter(completion_date__gte=previous_date, completion_date__lte=current_date,
                                     status='Выполнена').aggregate(Sum('service__price'))['service__price__sum']


@register.simple_tag
def get_requests_worked_time_sum(worker, previous_date, current_date):
    delta = worker.request_set.filter(completion_date__gte=previous_date, completion_date__lte=current_date,
                                      status='Выполнена').aggregate(Sum('service__duration'))['service__duration__sum']
    total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(total_seconds, 60 * 60)
    minutes, seconds = divmod(remainder, 60)
    return '{} ч. {} м.'.format(hours, minutes)


@register.simple_tag
def get_comments_worked_time_sum(worker, previous_date, current_date):
    delta = worker.comment_set.filter(completion_date__gte=previous_date, completion_date__lte=current_date,
                                      status='Выполнена').aggregate(Sum('service__duration'))['service__duration__sum']
    total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(total_seconds, 60 * 60)
    minutes, seconds = divmod(remainder, 60)
    return '{} ч. {} м.'.format(hours, minutes)
