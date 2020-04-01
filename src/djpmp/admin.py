# coding: utf-8

# https://github.com/lukasvinclav/django-admin-numeric-filter
from admin_numeric_filter.admin import RangeNumericFilter, NumericFilterModelAdmin

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render

from . import models as m

admin.site.site_header = 'djpmp'
admin.site.site_title = 'djpmp'
admin.site.index_title = '首页'
admin.site.site_url = None

# Register your models here.

# sample admin
"""

@admin.register(m.Customer)
class CustomerAdmin(admin.NumericFilterModelAdmin):
    list_display = ('id', 'project', 'name', 'mobile_enc', 'task_name', 'created', 'modified')
    actions = ('do_uni_update_info', 'do_make_call', 'assign_task')
    list_select_related = ('task',)
    autocomplete_fields = ('project', 'task')
    search_fields = ('name', 'mobile_enc', 'project__name', 'task__name')
    ordering = ('id', )
    list_filter = (('id', RangeNumericFilter))

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            try:
                company = request.user.userext.company
                return m.Customer.objects.filter(project__company=company)
            except ObjectDoesNotExist:
                return m.Customer.objects.none()

    def assign_task(self, req, qs):
        user = req.user
        company = user.userext.company
        task_list = list(m.Task.objects.filter(assign_to__userext__company=company).all())
        customer_list = list(qs)

        if 'apply' in req.POST:
            task_id = req.POST.get('task_id')
            if not task_id:
                self.message_user(req, '没选择项目')
                return
            else:
                task = m.Task.objects.get(pk=task_id)
                qs.update(task_id=task_id)
                customerbiz.refresh_task(task)
                self.message_user(req, f"分配到任务成功：{task_id}")
                return
        return render(req, 'admin/customer/assign_task.html', context={'tasks': task_list, 'customers': customer_list})

    assign_task.short_description = '分配任务'
    
class ProjectInline(admin.TabularInline):
    model = m.Project
    formfield_overrides = {
        models.DecimalField: {'widget': widgets.DecimalInput},
    }

class ContractTermInline(admin.TabularInline):
    model = m.ContractTerm
    exclude = ['department', 'seq']
    fields = ['name', 'contract', 'payment_terms', 'amount', 'payment_ratio',
              'payment_time_estimated', 'invoice_time_estimated', 'invoice_amount_estimated', 'invoice_time_actual',
              'invoice_type',
              'invoice_amount_actual', 'money_estimate_time', 'money_estimate_amount', 'money_actual_time',
              'money_actual_amount',
              'memo',
              ]
    readonly_fields = ['payment_ratio', ]
    formfield_overrides = {
        models.DecimalField: {'widget': widgets.DecimalInput},
    }
    extra = 0
    

@admin.register(m.Project)
class ProjectAdmin(admin.ModelAdmin):
    class Media:
        js = (JQUERY_MIN_JS, 'admin/pm/projectadmin.js',)
        css = {
            'screen': ('admin/pm/css/projectadmin.css',)
        }

    list_display = ('id', 'code', 'name', 'created', 'modified')
    list_display_links = ('id', 'code', 'name')
    search_fields = ['name', 'code', 'customer__name', ]
    list_filter = ['contract_category', 'business_category', 'contract_submit_status', 'project_status',
                   'invoice_status',
                   'income_status', 'service_status', 'customer_category', 'manager', ]
    inlines = [BudgetInline, MileStoneInline]
    exclude = ['period']
    radio_fields = {'business_category': admin.HORIZONTAL,
                    'contract_submit_status': admin.HORIZONTAL,
                    'service_status': admin.HORIZONTAL}
    formfield_overrides = {
        models.DecimalField: {'widget': widgets.DecimalInput},
    }
    # inlines = [ContractInline]
    # list_select_related = ('task', )
    # autocomplete_fields = ('task', )
    actions = ['action_export_summary', ]

    def get_queryset(self, request):
        qs = m.Project.objects.prefetch_related('department', 'customer', 'manager') \
            .select_related('department', 'customer', 'manager')
        return qs

@admin.register(m.Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'seq', 'name', '_project_code', 'created', 'modified', '_action']
    list_display_links = ['id', 'category', 'name', 'seq']
    search_fields = ['project__name', 'name', 'project__code']
    list_filter = ['department', 'category']
    exclude = ['department', 'position', 'retention_period']
    radio_fields = {'category': admin.HORIZONTAL}
    autocomplete_fields = ['project', ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('project', 'department')
        return qs

    def _project_code(self, obj):
        return obj.project.code

    _project_code.short_description = '项目编号'
    _project_code.admin_order_field = 'project'

    def _action(self, obj: m.Attachment):
        token = f'{uuid.uuid4()}'
        cache.set(f'download_token_{token}', '1', 3600 * 2)
        html = f'<a href="{obj.file.url}?download_token={token}" target="_blank">下载附件</a>'''
        return mark_safe(html)

    _action.short_description = '操作'


@admin.register(m.Budget)
class BudgetAdmin(admin.ModelAdmin):
    class Media:
        js = (JQUERY_MIN_JS, 'admin/pm/get_project_on_project_change.js')

    list_display = (
        'id', 'department', 'project', 'category', 'coa', 'budget_amount', 'actual_amount', 'available_amount')
    list_display_links = ['id', 'category']
    search_fields = ['project__name', 'category', 'coa']
    exclude = ['department', ]
    list_filter = ['department', ]
    autocomplete_fields = ['project']
    readonly_fields = ['available_amount', '_project_code']
    fields = ['project', '_project_code', 'category', 'coa', 'budget_amount', 'actual_amount', 'available_amount']

    form = forms.BudgetAdminForm

    formfield_overrides = {
        models.DecimalField: {'widget': widgets.DecimalInput},
    }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('project', 'department')
        return qs

    def _project_code(self, obj):
        return obj.project.code

    _project_code.short_description = '项目编号'
"""


