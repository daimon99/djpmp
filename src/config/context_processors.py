# coding: utf-8
from django.conf import settings


def footer(request):
    return {'footer': settings.FOOTER, 'version': settings.VERSION}
