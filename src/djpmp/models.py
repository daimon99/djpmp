# coding: utf-8
from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel
from mptt.models import MPTTModel, TreeForeignKey


def generate_choices(*choices):
    return list(zip(choices, choices))


class Project(TimeStampedModel):
    class Meta:
        verbose_name = verbose_name_plural = '项目'

    def __str__(self):
        return self.name

    name = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class WBS(TimeStampedModel, MPTTModel):
    class Meta:
        verbose_name = verbose_name_plural = 'WBS'
        ordering = ('tree_id', 'lft')

    class MPTTMeta:
        order_insertion_by = ['code', 'name']
        parent_attr = 'parent'

    def __str__(self):
        return f'{self.code or "-"} {self.name}'

    name = models.CharField(max_length=128)
    code = models.CharField(max_length=16, blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    pv = models.FloatField(default=0)
    ev = models.FloatField(default=0)


class Staff(TimeStampedModel):
    class Meta:
        verbose_name = verbose_name_plural = '成员'

    def __str__(self):
        return self.name

    name = models.CharField(max_length=128)


class HRCalendar(TimeStampedModel):
    class Meta:
        verbose_name = verbose_name_plural = '资源日历'
        unique_together = ('work_date', 'staff')

    def __str__(self):
        return f"{self.work_date.strftime('%Y-%m-%d')}-{self.staff}"

    work_date = models.DateField()
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    ev = models.FloatField(default=0)
    tasks = models.ManyToManyField(WBS, blank=True)
    tasks_memo = models.CharField(max_length=512, blank=True, null=True, verbose_name='任务说明')

    def save(self, **kwargs):
        self.tasks_memo = ' / '.join([str(i) for i in self.tasks.all()])
        tasks = self.tasks.all()
        # ev_total = self.ev
        # for task in tasks:

        return super().save(**kwargs)
