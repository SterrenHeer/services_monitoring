from datetime import date, timedelta
from django import template
from django.contrib.auth.models import Group
from django.db.models import Q
from users.models import Worker
from requests.models import Request, RequestComment

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
