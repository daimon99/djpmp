# -*- coding: utf-8 -*-
from datetime import datetime
from functools import reduce

from django.contrib import admin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse, path
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin
from mptt.admin import TreeRelatedFieldListFilter

from . import forms
from . import models as m
from .biz import core
from .filters import IsLeafFilter, EvFilter
from .models import Project, WBS, Staff, HRCalendar
from .utils import JQUERY_MIN_JS


def get_user_projects(user: User):
    user_companies = [x.company for x in user.companies.select_related('company').all()]
    projects = m.Project.objects.filter(company__in=user_companies).all()
    return projects


def get_user_companies(user: User):
    user_companies = [x.company for x in user.companies.select_related('company').all()]
    return user_companies


def get_user_last_company(user: User):
    user_companies = get_user_companies(user)
    if user_companies:
        return user_companies[-1]
    else:
        return None


def get_user_last_project(user):
    user_projects = get_user_projects(user)
    return user_projects.last()


class StaffInline(admin.TabularInline):
    model = m.Staff
    fields = ('name', 'man_day_price', 'role')
    extra = 0

    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class WBSInline(admin.TabularInline):
    model = m.WBS
    fields = ('_name', 'pv', 'ev', 'pv_ymb', 'ev_ymb', 'ac_ymb')
    # readonly_fields = ('ev', 'pv_ymb', 'ev_ymb', 'ac_ymb')
    readonly_fields = fields

    ordering = ('code', 'name')
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class HRCalendarInline(admin.TabularInline):
    model = m.HRCalendar
    fields = ['_work_date', 'staff', 'ev', 'tasks_memo']
    readonly_fields = fields
    can_delete = False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    class Media:
        js = [JQUERY_MIN_JS, 'admin/js/summary.js', 'admin/djpmp/project/project.js', ]

    list_display = ('id', 'name', 'company', '_pm_name', 'status', 'pv_rmb', 'ev_rmb', 'ac_rmb', 'created', '操作')
    list_filter = ('status', 'created', 'modified')
    search_fields = ('name',)
    readonly_fields = ['pv_rmb', 'ev_rmb', 'ac_rmb']
    actions = ['do_balance', ]
    list_display_links = ('id', 'name')
    radio_fields = {
        'status': admin.HORIZONTAL
    }
    inlines = [WBSInline, HRCalendarInline]
    menu_index = 10

    def get_queryset(self, request):
        user = request.user
        qs = super().get_queryset(request)
        if not user.is_superuser:
            qs = get_user_projects(user)
        return qs

    def 操作(self, obj):
        return mark_safe(f'<a href="/static/app/self-report/index.html?pid={obj.pk}&token={obj.token}" target="_blank">自助填报</a>')

    def get_changeform_initial_data(self, request):
        init = super().get_changeform_initial_data(request)
        init['company'] = get_user_last_company(request.user)
        init['pm'] = request.user
        return init

    def do_balance(self, req, qs):

        for i in qs:
            i: Project
            # 更新项目的 wbs ev
            core.assign_hr_cost_to_wbs(i.hrcalendar_set.all())
            # 计算项目的 ac
            man_day_price_avg = i.man_day_price_avg
            pv_rmb = 0.
            ev_rmb = 0.
            ac_rmb = 0.
            for task in i.wbs_set.all():
                if not task.is_leaf_node():
                    continue
                pv_rmb += man_day_price_avg * task.pv
                ev_rmb += man_day_price_avg * task.ev
            work_day_done = set()
            for work_day in m.HRCalendar.objects.filter(tasks__project=i).select_related('staff').all():
                print(
                    f'{work_day}: work_day.ev={work_day.ev}, work_day.staff.man_day_price={work_day.staff.man_day_price}')
                if work_day.id not in work_day_done:
                    ac_rmb += work_day.ev * work_day.staff.man_day_price
                    work_day_done.add(work_day.id)

            i.pv_rmb = round(pv_rmb, 2)
            i.ev_rmb = round(ev_rmb, 2)
            i.ac_rmb = round(ac_rmb, 2)
            i.save()
            self.message_user(req, f'项目: {i} 试算完成')

    do_balance.short_description = '项目成本试算'
    do_balance.allowed_permissions = ['change', ]


@admin.register(WBS)
class WBSAdmin(DraggableMPTTAdmin):
    class Media:
        js = (JQUERY_MIN_JS, 'admin/js/summary.js', 'admin/djpmp/wbs/wbs.js')

    list_display = (
        'tree_actions',
        'indented_title',
        'pv',
        'ev',
        'spi',
        'created',
    )
    list_filter = ('project', IsLeafFilter, 'level', 'created', 'modified', ('parent', TreeRelatedFieldListFilter))
    search_fields = ('name',)
    list_editable = ('pv',)
    ordering = ('tree_id', 'lft')
    actions = ['do_batch_update_parent', 'do_batch_update_code', 'do_calc', 'do_pv_clear', 'do_rebuild_tree']
    readonly_fields = ['ev']
    exclude = ['pv_ymb', 'ev_ymb', 'ac_ymb']
    menu_index = 30

    def get_queryset(self, request):
        user = request.user
        qs = super().get_queryset(request)
        if not user.is_superuser:
            qs = qs.filter(company__in=get_user_companies(user))
        return qs

    def get_changeform_initial_data(self, request):
        init = super().get_changeform_initial_data(request)
        init['company'] = get_user_last_company(request.user)
        init['project'] = get_user_last_project(request.user)
        return init

    def get_fields(self, request, obj=None):
        if not obj:
            fields = ['name', 'company', 'project']
        else:
            fields = super().get_fields(request, obj)
        return fields

    @property
    def total_pv(self):
        # functions to calculate whatever you want...
        try:
            total = self.get_queryset().filter(children__isnull=True).aggregate(tot=Sum('pv'))['tot']
            return round(total, 2)
        except:
            pass

    @property
    def total_ev(self):
        try:
            total = m.WBS.objects.filter(children__isnull=True).aggregate(tot=Sum('ev'))['tot']
            return round(total, 2)
        except:
            pass

    @property
    def total_spi(self):
        try:
            spi = f'{round(self.total_ev / self.total_pv * 100, 2)}%'
            return spi
        except:
            pass

    def spi(self, obj):
        try:
            return f'{round(obj.ev / obj.pv * 100, 2)}%'
        except:
            pass

    def do_batch_update_parent(self, request: HttpRequest, qs):
        """批量更新父任务"""
        if 'apply' in request.POST:
            parent_id = request.POST.get('wbs_list')
            parent = m.WBS.objects.get(pk=parent_id)
            for i in qs:
                i: m.WBS
                i.parent = parent
                i.save()

            self.message_user(request, f'选择的任务的父级任务已经设置为：{parent_id}')
            return HttpResponseRedirect(request.build_absolute_uri())
        context = {
            'title': '选择父级任务',
            'wbs': m.WBS.objects.filter(project_id=qs.first().project_id).exclude(
                pk__in=[x.id for x in qs.all()]).all(),
            'task_selected': qs
        }
        return render(request, 'admin/djpmp/wbs/batch-update-parent.html', context=context)

    do_batch_update_parent.short_description = '批量指定父任务'
    do_batch_update_parent.allowed_permissions = ['change', ]

    def do_batch_update_code(self, request, qs):
        """批量生成code"""
        roots = qs.filter(parent__isnull=True).order_by('pk').all()
        # next_index = 0
        for root in roots:
            # root.code = f'{next_index}'
            root.code = ""
            root.save()
            # next_index += 1
            set_index(root)
        self.message_user(request, '编码更新成功')

    do_batch_update_code.short_description = '批量分配编码'
    do_batch_update_code.allowed_permissions = ['change', ]

    def do_calc(self, req, qs):
        for i in qs:
            i: m.WBS
            if not i.is_leaf_node():
                i.pv = reduce(lambda x, y: x + y.pv, i.get_leafnodes(), 0)
                i.save()
        self.message_user(req, 'WBS计算成功')

    do_calc.short_description = '计算父节点PV'
    do_calc.allowed_permissions = ['change', ]

    def do_pv_clear(self, req, qs):
        qs.update(pv=0)
        self.message_user(req, 'pv清零')

    do_pv_clear.short_description = 'PV清零'
    do_pv_clear.allowed_permissions = ['change', ]

    def do_rebuild_tree(self, req, qs):
        m.WBS.objects.rebuild()
        self.message_user(req, '任务树重建完成')

    do_rebuild_tree.short_description = '重建树结构'


def set_index(parent: m.WBS):
    next_index = 1
    for child in parent.get_children().order_by('pk').all():
        if child.is_root_node() or str(child.parent.code) == '0' or str(child.parent.code) == '':
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
    list_display = ('id', 'name', 'company', 'role', 'man_day_price', 'created', 'modified')
    list_filter = ('company', 'created', 'modified')
    search_fields = ('name',)
    list_display_links = ('id', 'name')
    menu_index = 20

    def get_queryset(self, request):
        user = request.user
        qs = super().get_queryset(request)
        if not user.is_superuser:
            qs = qs.filter(company__in=get_user_companies(user))
        return qs

    def get_changeform_initial_data(self, request):
        init = super().get_changeform_initial_data(request)
        init['company'] = get_user_last_company(request.user)
        return init


@admin.register(HRCalendar)
class HRCalendarAdmin(admin.ModelAdmin):
    class Media:
        js = (JQUERY_MIN_JS, 'admin/js/summary.js', 'admin/djpmp/hrcalendar/hrcalendar.js')

    list_display = ('id', '_work_date', 'staff', 'ev', 'status', 'tasks_memo')
    list_filter = (EvFilter, 'project', 'work_date', 'staff')
    # raw_id_fields = ('tasks',)
    # list_editable = ('ev',)
    filter_horizontal = ('tasks',)
    ordering = ('-work_date', 'staff')
    list_select_related = ['staff']
    readonly_fields = ['tasks_memo']
    list_display_links = ('id', '_work_date')
    menu_index = 40
    actions = ['do_batch_assign_wbs', 'do_calc', 'do_batch_confirm', 'do_batch_update_memo']

    def get_queryset(self, request):
        user = request.user
        qs = super().get_queryset(request)
        if not user.is_superuser:
            qs = qs.filter(company__in=get_user_companies(user))
        return qs

    def get_urls(self):
        return [
                   path('batch-create/', self.admin_site.admin_view(self.view_batch_create),
                        name='djpmp_hrcalendar_batch-create'),
                   path('self-report/', self.view_self_report,
                        name='djpmp_hrcalendar_self-report'),
               ] + super().get_urls()

    def get_changeform_initial_data(self, request):
        init = super().get_changeform_initial_data(request)
        user_last_company = get_user_last_company(request.user)
        init['company'] = user_last_company
        user_last_project = get_user_last_project(request.user)
        init['project'] = user_last_project
        init['work_date'] = datetime.now().strftime('%Y-%m-%d')
        try:
            init['staff'] = m.HRCalendar.objects.filter(project=user_last_project).latest('created').staff
        except:
            try:
                init['staff'] = m.Staff.objects.filter(company=user_last_company).last()
            except:
                pass
        return init

    def view_batch_create(self, request):
        """批量创建资源日历"""
        if not self.has_add_permission(request):
            raise PermissionDenied
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
                    i.save()
            self.message_user(request, f'任务增加成功')
            return HttpResponseRedirect(request.build_absolute_uri())
        context = {
            'title': '选择要指派的任务',
            'selected': qs,
            'wbs': m.WBS.objects.filter(company=qs.first().company).all()
        }
        return render(request, 'admin/djpmp/hrcalendar/batch-assign-wbs.html', context=context)

    do_batch_assign_wbs.short_description = '分配WBS'
    do_batch_assign_wbs.allowed_permissions = ['change', ]

    def do_calc(self, req, qs):
        core.assign_hr_cost_to_wbs(qs)
        self.message_user(req, '计算完毕')

    do_calc.short_description = '计算挣值'
    do_calc.allowed_permissions = ['change', ]

    def do_batch_confirm(self, req, qs):
        """批量确认"""
        qs.update(status='已确认')
        self.message_user(req, '选定的资源投入已经确认', 25)

    do_batch_confirm.short_description = '批量确认资源投入'
    do_batch_confirm.allowed_permissions = ['change', ]

    def has_change_permission(self, request, obj=None):
        is_ok = super().has_change_permission(request, obj)
        if obj and is_ok:
            return obj.status == '待确认'
        return is_ok

    def view_self_report(self, request, *args, **kwargs):
        # if not self.has_add_permission(request):
        #     raise PermissionDenied
        if request.method == 'POST':
            form = forms.DateSpanForm(request.POST)
            if form.is_valid():
                form.save()
                self.message_user(request, f'批量创建日历成功!')
                return HttpResponseRedirect(reverse('admin:djpmp_hrcalendar_changelist'))
        context = {
            'title': '批量创建资源日历',
            # 'form': form,
        }
        return render(request, 'admin/djpmp/hrcalendar/self-report.html', context=context)

    def do_batch_update_memo(self, req, qs):
        for i in qs:
            i.save()
        self.message_user(req, '更新任务说明成功')

    do_batch_update_memo.short_description = '批量更新任务说明'


@admin.register(m.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    menu_index = 90


@admin.register(m.UserCompany)
class UserCompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'company')
    menu_index = 91
