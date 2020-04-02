# coding: utf-8
from django import forms
import datetime
from . import models as m


class DateSpanForm(forms.Form):
    project = forms.ModelChoiceField(m.Project.objects.all(), required=True, label='项目')
    start_date = forms.DateField(required=True, label='开始日期', widget=forms.DateInput(attrs={"type": "date"}))
    # end_date = forms.DateField(required=True, label='结束日期', widget=forms.SelectDateWidget)
    count = forms.IntegerField(required=True, initial=7, label='天数', help_text='持续天数')
    staffs = forms.ModelMultipleChoiceField(m.Staff.objects.all(), required=True, label='员工列表')

    def save(self):
        data = self.cleaned_data
        for d in range(data['count']):
            day = data['start_date'] + datetime.timedelta(days=d)
            project = data['project']
            for staff in data['staffs']:
                m.HRCalendar.objects.create(work_date=day, staff=staff, project=project)
