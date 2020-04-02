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
    man_day_price_avg = models.FloatField(verbose_name='平均人天单价', help_text='单位：元', default=0)
    ac_rmb = models.FloatField(verbose_name='ac', help_text='单位：元', default=0)
    pv_rmb = models.FloatField(verbose_name='pv', help_text='单位：元', default=0)
    ev_rmb = models.FloatField(verbose_name='ev', help_text='单位：元', default=0)


class WBS(TimeStampedModel, MPTTModel):
    class Meta:
        verbose_name = verbose_name_plural = 'WBS'
        ordering = ('tree_id', 'lft')

    class MPTTMeta:
        order_insertion_by = ['code', 'name']
        parent_attr = 'parent'

    def __str__(self):
        return f'{self.code or "-"} {self.name}'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=16, blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    pv = models.FloatField(default=0, help_text="计划价值，单元人天")
    ev = models.FloatField(default=0, help_text="挣值，单位人天")
    ac_ymb = models.FloatField(default=0, help_text='实际成本，单位元')
    pv_ymb = models.FloatField(default=0, help_text='计划价值，单位元')
    ev_ymb = models.FloatField(default=0, help_text='完工价值，单位元')


class Staff(TimeStampedModel):
    class Meta:
        verbose_name = verbose_name_plural = '成员'

    def __str__(self):
        return self.name

    name = models.CharField(max_length=128)
    man_day_price = models.FloatField(verbose_name='人天单价', default=0)


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
        return super().save(**kwargs)
