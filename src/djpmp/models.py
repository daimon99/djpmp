# coding: utf-8

from django.contrib.auth.models import User, Group
from django.db import models
from django.http import HttpRequest
from django_extensions.db.models import TimeStampedModel
from django_middleware_global_request.middleware import get_request
from mptt.models import MPTTModel, TreeForeignKey


def generate_choices(*choices):
    return list(zip(choices, choices))


def my_projects():
    request: HttpRequest = get_request()
    if request and request.user:
        user = request.user
        if user.is_superuser:
            return {}
        else:
            return {
                'group__in': user.groups.all()
            }


class Project(TimeStampedModel):
    class Meta:
        verbose_name = verbose_name_plural = '项目'

    def __str__(self):
        return self.name

    name = models.CharField(max_length=128)
    man_day_price_avg = models.FloatField(verbose_name='平均人天单价', help_text='单位：元', default=0)
    ac_rmb = models.FloatField(verbose_name='ac', help_text='单位：元', default=0)
    pv_rmb = models.FloatField(verbose_name='pv', help_text='单位：元', default=0)
    ev_rmb = models.FloatField(verbose_name='ev', help_text='单位：元', default=0)
    group = models.ForeignKey(Group, blank=True, null=True, verbose_name='权限组', on_delete=models.SET_NULL,
                              help_text='在此组中的用户可以浏览此项目信息')
    status = models.CharField(verbose_name='状态', max_length=64, choices=(
        ('未开始', '未开始'),
        ('进行中', '进行中'),
        ('完成', '完成')
    ), default='进行中')


class WBS(TimeStampedModel, MPTTModel):
    class Meta:
        verbose_name = verbose_name_plural = 'WBS'
        ordering = ('tree_id', 'lft')

    class MPTTMeta:
        order_insertion_by = ['code', 'name']
        parent_attr = 'parent'

    def __str__(self):
        return f'{self.code or "-"} {self.name}'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目', limit_choices_to=my_projects)
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

    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目', limit_choices_to=my_projects)
    name = models.CharField(max_length=128)
    man_day_price = models.FloatField(verbose_name='人天单价', default=0)
    role = models.CharField(max_length=64, verbose_name='角色', choices=(
        ('后端中级', '后端中级'),
        ('后端高级', '后端高级'),
        ('前端中级', '前端中级'),
        ('前端高级', '前端高级'),
        ('UI中级', 'UI中级'),
        ('UI高级', 'UI高级'),
        ('测试中级', '测试中级'),
        ('测试高级', '测试高级'),
        ('产品中级', '产品中级'),
        ('产品高级', '产品高级'),
    ), default='后端中级')


class HRCalendar(TimeStampedModel):
    class Meta:
        verbose_name = verbose_name_plural = '资源日历'
        unique_together = ('project', 'work_date', 'staff')

    def __str__(self):
        return f"{self.work_date.strftime('%Y-%m-%d')}-{self.staff}"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目', limit_choices_to=my_projects)
    work_date = models.DateField()
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    ev = models.FloatField(default=0, choices=(
        (0.0, 0.0),
        (0.5, 0.5),
        (1.0, 1.0),
        (1.5, 1.5),
        (2.0, 2.0)
    ))
    tasks = models.ManyToManyField(WBS, blank=True)
    tasks_memo = models.CharField(max_length=512, blank=True, null=True, verbose_name='任务说明')

    def save(self, **kwargs):
        if self.id:
            self.tasks_memo = ' / '.join([str(i) for i in self.tasks.all()])
        return super().save(**kwargs)
