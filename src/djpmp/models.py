# coding: utf-8
from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel
from mptt.models import MPTTModel, TreeForeignKey


def generate_choices(*choices):
    return list(zip(choices, choices))


class Project(TimeStampedModel):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class WBS(TimeStampedModel, MPTTModel):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=128)
    code = models.CharField(max_length=16, blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    pv = models.FloatField(default=0)
    ev = models.FloatField(default=0)

    # class MPTTMeta:
        # order_insertion_by = ['code', 'id']
        # parent_attr = 'parent'


class Staff(TimeStampedModel):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=128)


class HRCalendar(TimeStampedModel):
    def __str__(self):
        return self.work_date

    work_date = models.DateField()
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    ev = models.FloatField(default=0)
    tasks = models.ManyToManyField(WBS, blank=True)
