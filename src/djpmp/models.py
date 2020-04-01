# coding: utf-8
from django.db import models
from django_extensions.db.models import TimeStampedModel

from django.contrib.auth.models import User


def generate_choices(*choices):
    return list(zip(choices, choices))

# Create your models here.
#
# class Budget(TimeStampedModel):
#     class Meta:
#         verbose_name = '12项目预算'
#         verbose_name_plural = '12项目预算'
#
#     def __str__(self):
#         if self.coa:
#             return str(self.id)
#         else:
#             return ''
#
#     department = models.ForeignKey(Department, verbose_name='部门', on_delete=models.CASCADE)
#
#     project = models.ForeignKey(Project, verbose_name='项目', on_delete=models.CASCADE)
#
#     category = models.CharField(max_length=128, verbose_name='费用', blank=True, null=True,
#                                 choices=generate_choices('销售成本', '销售费用'))
#     coa = models.CharField(max_length=128, verbose_name='科目', blank=True, null=True, choices=(
#         ('销售成本', generate_choices(
#             '材料（13%税率专票）',
#             '材料（普票）',
#             '服务费（6%税率专票）',
#             '工程费（9%税率专票）',
#             '维修费（13%税率专票）',
#             '工程费（3%税率专票）',
#             '其他成本')),
#         ('销售费用', generate_choices(
#             '车辆费',
#             '市内交通',
#             '差旅费',
#             '招待费',
#             '运营费',
#             '运输费',
#             '其它费用'))
#     ))
#     budget_amount = models.DecimalField(verbose_name='核准预算', blank=True, null=True, max_digits=12, decimal_places=2)
#     actual_amount = models.DecimalField(verbose_name='实际支出', blank=True, null=True, max_digits=12, decimal_places=2)
#     available_amount = models.DecimalField(verbose_name='剩余预算', blank=True, null=True, max_digits=12, decimal_places=2)
#
#     def save(self, **kwargs):
#         self.department = self.project.department
#         if self.budget_amount and self.actual_amount:
#             self.available_amount = self.budget_amount - self.actual_amount
#         return super().save(**kwargs)
