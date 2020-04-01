# coding: utf-8
import logging

from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

log = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def save_user(sender, instance: User, created, **kwargs):
    """这里可以用来创建 User 的相关对象。如 One2One 的那些模型数据"""
    if not created:
        return
    log.warning('新建用户：%s', instance)
