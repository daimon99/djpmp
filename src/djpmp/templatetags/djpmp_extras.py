# coding: utf-8
from django import template

register = template.Library()


@register.filter()
def percentof(value, arg):
    """value占传进参数的百分比"""
    return f'{value / arg * 100:.1f}%'


@register.filter()
def divide(value, arg):
    """除法"""
    return value / arg
