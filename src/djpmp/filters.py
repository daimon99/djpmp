# coding: utf-8
from django.contrib import admin
from django.db.models import Q


#
# from admin_auto_filters.filters import AutocompleteFilter
#
#
# class ProjectFilter(AutocompleteFilter):
#     title = '项目'  # display title
#     field_name = 'project'  # name of the foreign key field
#
# class InputFilter(admin.SimpleListFilter):
#     template = 'admin/input_filter.html'
#
#     def lookups(self, request, model_admin):
#         # Dummy, required to show the filter.
#         return ((),)
#
#     def choices(self, changelist):
#         # Grab only the "all" option.
#         all_choice = next(super().choices(changelist))
#         all_choice['query_parts'] = (
#             (k, v)
#             for k, v in changelist.get_filters_params().items()
#             if k != self.parameter_name
#         )
#         yield all_choice
#
#
# class SentenceIdFilter(InputFilter):
#     parameter_name = 'sentence_id'
#     title = '话术ID'
#
#     def queryset(self, request, qs):
#         if self.value() is not None:
#             sentence_id = self.value()
#             return qs.filter(
#                 Q(sentence_id=sentence_id)
#             )

class IsLeafFilter(admin.SimpleListFilter):
    title = '叶子节点'
    parameter_name = 'is_leaf'

    def lookups(self, request, model_admin):
        return (
            ('1', '是'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            print('--->')
            return queryset.filter(children__isnull=True)


class EvFilter(admin.SimpleListFilter):
    title = 'EV'
    parameter_name = 'ev_tag'

    def lookups(self, request, model_admin):
        return (
            ('1', '大于0'),
            ('2', '等于0')
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.exclude(ev=0)
        else:
            return queryset.filter(ev=0)
