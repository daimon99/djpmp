# coding: utf-8
"""接口业务逻辑实现代码"""

import logging
from datetime import datetime

from rest_framework import viewsets, permissions
# from .serializers import ProjectSerializer, ContractSerializer
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from . import serializers
from .. import models as m

log = logging.getLogger(__name__)


class HRCalendarApi(viewsets.ModelViewSet):
    queryset = m.HRCalendar.objects.all()
    serializer_class = serializers.HRCalendarSerializer


class WBSApi(viewsets.ModelViewSet):
    queryset = m.WBS.objects.all()
    serializer_class = serializers.WBSSerializer


class ProjectApi(viewsets.ModelViewSet):
    queryset = m.Project.objects.all()
    serializer_class = serializers.ProjectSerializer


class CompanyApi(viewsets.ModelViewSet):
    queryset = m.Company.objects.all()
    serializer_class = serializers.CompanySerializer


class SelfReportPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        pid = request.GET.get('pid')
        token = request.GET.get('token')
        if not pid:
            return False
        try:
            project = m.Project.objects.get(token=token, pk=pid)
            view.project = project
            return True
        except:
            return False


class SelfReportApi(viewsets.ViewSet):
    authentication_classes = ()
    permission_classes = [SelfReportPermission]

    @action(['get'], detail=False)
    def get_init_data(self, req: Request):
        project = self.project
        roots = list(project.wbs_set.filter(project=project, level=0).all())
        # tasks = [{'value': x.id, 'label': x._code_name(), 'level': x.level} for x in
        #          project.wbs_set.filter(project_id=project.id).all()]
        tasks = tree_for_nodes(roots)
        table_data = [{
            'work_date': x.work_date.strftime('%Y-%m-%d'),
            'staff_name': x.staff.name,
            'ev': x.ev,
            'status': x.status,
            'tasks_memo': x.tasks_memo} for x in project.hrcalendar_set.order_by('-staff', '-work_date').all()
            if x.ev > 0
        ]
        ret = {
            'code': 0,
            'msg': '返回项目初始信息成功',
            'company_name': project.company.name,
            'project_name': project.name,
            'staffs': [{'name': x.name, 'id': x.id} for x in project.company.staff_set.all()],
            'tasks': tasks,
            'table_data': table_data
        }
        return Response(ret)

    @action(methods=['post'], detail=False)
    def save(self, req, *args, **kwargs):
        form = req.data.get('form')
        if not form:
            return Response({
                'code': -1,
                'msg': 'no form'
            })
        staff_id = form.get('staff_id')
        project_id = form.get('project_id')
        work_date = datetime.fromtimestamp(int(form.get('work_date')) / 1000)
        tasks = form.get('tasks')
        ev = form.get('ev')
        try:
            record = m.HRCalendar.objects.get(project_id=project_id, work_date=work_date, staff_id=staff_id)
            if record.status == '已确认':
                return Response({
                    'code': -2,
                    'msg': f'{record.staff.name} 在 {record.work_date.strftime("%Y-%m-%d")}的工作量已经被确认，无法再调整。'
                })
            record.ev = ev
        except m.HRCalendar.DoesNotExist:
            record = m.HRCalendar.objects.create(
                project_id=project_id,
                work_date=work_date,
                staff_id=staff_id,
                ev=ev
            )
        record.tasks.set(tasks)
        record.save()  # 重新计算 hrcalendar 的tasks_memo 值
        return Response({
            'code': 0,
            'msg': '成功',
        })


def tree_for_nodes(roots):
    """获取节点列表的 element cascade 表示"""
    tasks = []
    for i in roots:
        data = {'value': i.id, 'label': i.name}
        if not i.is_leaf_node():
            data['children'] = get_children(i)
        tasks.append(data)
    return tasks


def get_children(node):
    """获取节点树"""
    if node.is_leaf_node():
        return
    children = node.get_children()
    ret = []
    for i in children:
        data = {'value': i.id, 'label': i.name}
        if not i.is_leaf_node():
            data['children'] = get_children(i)
        ret.append(data)
    return ret
