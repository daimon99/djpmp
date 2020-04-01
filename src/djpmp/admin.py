# -*- coding: utf-8 -*-
from functools import reduce

from django.contrib import admin
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse, path
from . import forms
from . import models as m
from .filters import IsLeafFilter
from .models import Project, WBS, Staff, HRCalendar

from mptt.admin import DraggableMPTTAdmin
from mptt.admin import TreeRelatedFieldListFilter


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'created', 'modified',)
    list_filter = ('created', 'modified', 'user')
    search_fields = ('name',)


@admin.register(WBS)
class WBSAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions',
        'indented_title',
        'code',
        'name',
        'pv',
        'ev',
        'created',
    )
    list_filter = (IsLeafFilter, 'level', 'created', 'modified', ('parent', TreeRelatedFieldListFilter),)
    search_fields = ('name',)
    list_editable = ('pv', 'ev')
    ordering = ('tree_id', 'lft')
    actions = ['do_batch_update_parent', 'do_batch_update_code', 'do_calc']

    @property
    def total_pv(self):
        # functions to calculate whatever you want...
        total = m.WBS.objects.filter(children__isnull=True).aggregate(tot=Sum('pv'))['tot']
        return total

    @property
    def total_ev(self):
        # functions to calculate whatever you want...
        total = m.WBS.objects.filter(children__isnull=True).aggregate(tot=Sum('ev'))['tot']
        return total

    def changelist_view(self, request, *args, **kwargs):
        extra = {
            'total_pv': self.total_pv
        }
        return super().changelist_view(request, extra_context=extra)

    def do_batch_update_parent(self, request, qs):
        """批量更新父任务"""
        if 'apply' in request.POST:
            parent_id = request.POST.get('parent_id')
            for i in qs:
                i.parent_id = parent_id
                i.save()
            self.message_user(request, f'选择的任务的父级任务已经设置为：{parent_id}')
            return HttpResponseRedirect(reverse('admin:djpmp_wbs_changelist'))
        context = {
            'title': '选择父级任务',
            'tasks': m.WBS.objects.all(),
            'task_selected': qs
        }
        return render(request, 'admin/djpmp/wbs/batch-update-parent.html', context=context)

    do_batch_update_parent.short_description = '批量指定父任务'

    def do_batch_update_code(self, request, qs):
        """批量生成code"""
        roots = m.WBS.objects.filter(parent__isnull=True).order_by('pk').all()
        next_index = 1
        for root in roots:
            root.code = f'{next_index}'
            root.save()
            next_index += 1
            set_index(root)
        self.message_user(request, '编码更新成功')

    do_batch_update_code.short_description = '批量分配编码'

    def do_calc(self, req, qs):
        for i in qs:
            i: m.WBS
            if not i.is_leaf_node():
                i.pv = reduce(lambda x, y: x + y.pv, i.get_leafnodes(), 0)
                i.save()
        self.message_user(req, 'WBS计算成功')

    do_calc.short_description = '计算'


def set_index(parent: m.WBS):
    next_index = 1
    for child in parent.get_children().order_by('pk').all():
        if child.is_root_node():
            child.code = f'{next_index}'
        else:
            child.code = f'{child.parent.code}.{next_index}'
        child.save()
        next_index += 1
        if child.is_leaf_node():
            continue
        else:
            set_index(child)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created', 'modified')
    list_filter = ('created', 'modified')
    search_fields = ('name',)


weekday = {
    0: '星期一',
    1: '星期二',
    2: '星期三',
    3: '星期四',
    4: '星期五',
    5: '星期六',
    6: '星期日'
}


@admin.register(HRCalendar)
class HRCalendarAdmin(admin.ModelAdmin):
    list_display = ('id', '_work_date', 'staff', 'ev', 'tasks_memo')
    list_filter = ('work_date', 'staff')
    # raw_id_fields = ('tasks',)
    list_editable = ('ev',)
    filter_horizontal = ('tasks',)
    ordering = ('work_date', 'staff')
    actions = ['do_batch_assign_wbs', 'do_calc']
    list_select_related = ['staff']
    readonly_fields = ['tasks_memo']

    def _work_date(self, obj):
        return f'{obj.work_date.strftime("%Y年%m月%d日")} {weekday[obj.work_date.weekday()]}'

    def get_urls(self):
        return [
                   path('batch-create/', self.admin_site.admin_view(self.view_batch_create),
                        name='djpmp_hrcalendar_batch-create')
               ] + super().get_urls()

    def view_batch_create(self, request):
        """批量创建资源日历"""
        if request.method == 'POST':
            form = forms.DateSpanForm(request.POST)
            if form.is_valid():
                form.save()
                self.message_user(request, f'批量创建日历成功!')
                return HttpResponseRedirect(reverse('admin:djpmp_hrcalendar_changelist'))
        else:
            form = forms.DateSpanForm()
        context = {
            'title': '批量创建资源日历',
            'form': form,
        }
        return render(request, 'admin/djpmp/hrcalendar/batch-update-parent.html', context=context)

    def do_batch_assign_wbs(self, request: HttpRequest, qs):
        """批量指派wbs"""
        if 'apply' in request.POST:
            wbs_list = request.POST.getlist('wbs_list')
            for i in qs:
                i: m.HRCalendar
                for wbs_id in wbs_list:
                    i.tasks.add(m.WBS.objects.get(pk=wbs_id))
            self.message_user(request, f'任务增加成功')
            return HttpResponseRedirect(request.build_absolute_uri())
        context = {
            'title': '选择要指派的任务',
            'selected': qs,
            'wbs': m.WBS.objects.all()
        }
        return render(request, 'admin/djpmp/hrcalendar/batch-assign-wbs.html', context=context)

    do_batch_assign_wbs.short_description = '分配WBS'

    def do_calc(self, req, qs):
        for i in qs:
            i.save()

        self.message_user(req, '计算完毕')

    do_calc.short_description = '计算'
