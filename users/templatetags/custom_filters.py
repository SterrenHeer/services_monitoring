from django import template
from django.contrib.auth.models import Group
from users.models import Worker

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@register.simple_tag
def get_worker(name):
    return Worker.objects.get(full_name=name)
