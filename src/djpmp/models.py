# coding: utf-8

from django.contrib.auth.models import User, Group
from django.db import models
from django.http import HttpRequest
from django.utils.safestring import mark_safe
from django_extensions.db.models import TimeStampedModel
from django_middleware_global_request.middleware import get_request
from mptt.models import MPTTModel, TreeForeignKey

weekday = {
    0: '星期一',
    1: '星期二',
    2: '星期三',
    3: '星期四',
    4: '星期五',
    5: '星期六',
    6: '星期日'
}


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
                'company__in': [x.company for x in user.companies.select_related('company').all()]
            }


def my_companies():
    request: HttpRequest = get_request()
    if request and request.user:
        user = request.user
        if user.is_superuser:
            return {}
        else:
            _my_companies = [x.company.id for x in user.companies.select_related('company').all()]
            return {
                'pk__in': _my_companies
            }


def my_staff():
    request: HttpRequest = get_request()
    if request and request.user:
        user = request.user
        if user.is_superuser:
            return {}
        else:
            return {
                'company__in': [x.company for x in user.companies.select_related('company').all()]
            }


def my_tasks():
    request: HttpRequest = get_request()
    if request and request.user:
        user = request.user
        if user.is_superuser:
            return {}
        else:
            return {
                'company__in': [x.company for x in user.companies.select_related('company').all()]
            }


class Company(TimeStampedModel):
    class Meta:
        verbose_name = verbose_name_plural = '公司'

    def __str__(self):
        return f'{self.name}'

    name = models.CharField(verbose_name='公司', max_length=128)


class UserCompany(TimeStampedModel):
    class Meta:
        verbose_name = verbose_name_plural = '用户数据权限'

    def __str__(self):
        return f'{self.user} - {self.company}'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Project(TimeStampedModel):
    class Meta:
        verbose_name = verbose_name_plural = '项目'

    def __str__(self):
        return self.name

    company = models.ForeignKey(Company, verbose_name='公司', on_delete=models.CASCADE, limit_choices_to=my_companies)
    pm = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='项目经理', blank=True, null=True)
    name = models.CharField(max_length=128, verbose_name='项目名称')
    man_day_price_avg = models.FloatField(verbose_name='平均人天单价', help_text='单位：元', default=0)
    ac_rmb = models.FloatField(verbose_name='AC', help_text='单位：元', default=0)
    pv_rmb = models.FloatField(verbose_name='PV', help_text='单位：元', default=0)
    ev_rmb = models.FloatField(verbose_name='EV', help_text='单位：元', default=0)
    # group = models.ForeignKey(Group, blank=True, null=True, verbose_name='权限组', on_delete=models.SET_NULL,
    #                           help_text='在此组中的用户可以浏览此项目信息')
    status = models.CharField(verbose_name='状态', max_length=64, choices=(
        ('未开始', '未开始'),
        ('进行中', '进行中'),
        ('完成', '完成')
    ), default='进行中')
    token = models.CharField(verbose_name='权限码', blank=True, null=True, max_length=128)

    def save(self, **kwargs):
        if not self.pm:
            self.pm = get_request().user
        ret = super().save(**kwargs)
        return ret

    def _pm_name(self):
        return f'{self.pm.first_name}' if self.pm and self.pm.first_name else '-'

    _pm_name.short_description = '项目经理'


class WBS(TimeStampedModel, MPTTModel):
    class Meta:
        verbose_name = verbose_name_plural = 'WBS'
        ordering = ('tree_id', 'lft')

    class MPTTMeta:
        order_insertion_by = ['code', 'name']
        parent_attr = 'parent'

    def __str__(self):
        return f'{self.code or "-"} {self.name}'

    company = models.ForeignKey(Company, verbose_name='公司', on_delete=models.CASCADE, limit_choices_to=my_companies)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目', limit_choices_to=my_projects)
    name = models.CharField(max_length=128, verbose_name='任务')
    code = models.CharField(max_length=16, blank=True, null=True, verbose_name='编码')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    pv = models.FloatField(default=0, help_text="计划价值，单位：人天")
    ev = models.FloatField(default=0, help_text="挣值，单位：人天")
    ac_ymb = models.FloatField(default=0, help_text='实际成本，单位元', verbose_name='实际成本')
    pv_ymb = models.FloatField(default=0, help_text='计划价值，单位元', verbose_name='计划价值')
    ev_ymb = models.FloatField(default=0, help_text='完工价值，单位元', verbose_name='完工价值')

    def _name(self):
        """缩进的name"""
        level = self.get_level()
        return mark_safe(f'<span style="padding-left: {24 * level}px">{self.code} {self.name}</span>')

    _name.short_description = '任务'

    def _code_name(self):
        if self.code and self.name:
            return f'{self.code} {self.name}'
        else:
            return self.name


class Staff(TimeStampedModel):
    class Meta:
        verbose_name = verbose_name_plural = '人力资源'

    def __str__(self):
        return f'{self.id} - {self.name}'

    company = models.ForeignKey(Company, verbose_name='公司', on_delete=models.CASCADE, limit_choices_to=my_companies)
    name = models.CharField(max_length=128, verbose_name='姓名')
    man_day_price = models.FloatField(verbose_name='人天单价', default=0, help_text='元/人天')
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

    company = models.ForeignKey(Company, verbose_name='公司', on_delete=models.CASCADE, limit_choices_to=my_companies)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目', limit_choices_to=my_projects)
    work_date = models.DateField(verbose_name='日期')
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name='人员', limit_choices_to=my_staff)
    # staff = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name='人员')
    ev = models.FloatField(default=0, choices=(
        (0.0, 0.0),
        (0.5, 0.5),
        (1.0, 1.0),
        (1.5, 1.5),
        (2.0, 2.0)
    ))
    tasks = models.ManyToManyField(WBS, blank=True, limit_choices_to=my_tasks)
    tasks_memo = models.CharField(max_length=512, blank=True, null=True, verbose_name='任务说明')
    status = models.CharField(max_length=32, verbose_name='状态', choices=(
        ('待确认', '待确认'),
        ('已确认', '已确认'),
    ), default='待确认')

    def save(self, **kwargs):
        if self.id:
            self.tasks_memo = ' / '.join([str(i) for i in self.tasks.all()])
        if self.project:
            self.company = self.project.company
        return super().save(**kwargs)

    def _work_date(self):
        return f'{self.work_date.strftime("%Y年%m月%d日")} {weekday[self.work_date.weekday()]}'

    _work_date.short_description = '日期'
