# coding: utf-8
import datetime

from django import forms
from django_middleware_global_request.middleware import get_request

from . import models as m


class DateSpanForm(forms.Form):
    company = forms.ModelChoiceField(None, required=True, label='公司')
    project = forms.ModelChoiceField(None, required=True, label='项目')
    start_date = forms.DateField(required=True, label='开始日期', widget=forms.DateInput(attrs={"type": "date"}))
    # end_date = forms.DateField(required=True, label='结束日期', widget=forms.SelectDateWidget)
    count = forms.IntegerField(required=True, initial=7, label='天数', help_text='持续天数')
    staffs = forms.ModelMultipleChoiceField(None, required=True, label='员工列表')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = get_request().user
        companie_ids = [x.company_id for x in user.companies.all()]
        self.fields['company'].queryset = m.Company.objects.filter(pk__in=companie_ids).order_by('name')
        self.fields['project'].queryset = m.Project.objects.filter(company_id__in=companie_ids).order_by('name')
        self.fields['staffs'].queryset = m.Staff.objects.filter(company_id__in=companie_ids).order_by('name')
        self.initial = {
            'company': self.fields['company'].queryset.last(),
            'project': self.fields['project'].queryset.last(),
            'staffs': self.fields['staffs'].queryset.all(),
            'start_date': datetime.datetime.now().strftime('%Y-%m-%d')
        }

    def save(self):
        data = self.cleaned_data
        for d in range(data['count']):
            day = data['start_date'] + datetime.timedelta(days=d)
            project = data['project']
            for staff in data['staffs']:
                m.HRCalendar.objects.create(work_date=day, staff=staff, project=project, company=data['company'])
