# custom_auth/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def is_admin(user):
    return user.designation == 'Admin'

@register.filter
def is_supervisor(user):
    return user.designation == 'Supervisor'

@register.filter
def is_employee(user):
    return user.designation == 'Employee'
