# -*- coding: utf-8 -*-

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

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
        'id',
        'code',
        'level',
        'name',
        'pv',
        'ev',
        'created',
        'modified',
    )
    list_filter = (IsLeafFilter, 'level', 'created', 'modified', ('parent', TreeRelatedFieldListFilter),)
    search_fields = ('name',)
    list_editable = ('pv', 'ev')
    ordering = ('tree_id', 'lft')
    actions = ['do_batch_update_parent', 'do_batch_update_code', 'do_clear_parent']

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

    def do_clear_parent(self, req, qs):
        for i in qs:
            i.parent = None
            i.save()
        self.message_user(req, '清空成功')


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


@admin.register(HRCalendar)
class HRCalendarAdmin(admin.ModelAdmin):
    list_display = ('id', 'work_date', 'staff', 'ev', 'created', 'modified')
    list_filter = ('created', 'modified', 'work_date', 'staff')
    raw_id_fields = ('tasks',)
