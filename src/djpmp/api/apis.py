# coding: utf-8
"""接口业务逻辑实现代码"""

from rest_framework import viewsets, permissions
# from .serializers import ProjectSerializer, ContractSerializer
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from . import serializers
from .. import models as m


#
#
# class ProjectApi(viewsets.ReadOnlyModelViewSet):
#     queryset = m.Project.objects.all()
#     serializer_class = ProjectSerializer
#
#
# class ContractApi(viewsets.ReadOnlyModelViewSet):
#     queryset = m.Contract.objects.all()
#     serializer_class = ContractSerializer


# class ToolsApi(viewsets.ViewSet):
#     authentication_classes = ()
#     permission_classes = ()
#
#     @action(['get'], detail=False)
#     def hello(self, req: Request):
#         """Sample code
#         """
#         with TimeIt() as timeit:
#             code = 0
#         telegraf.metric('hello', {'duration': timeit.duration}, {'code': code})
#         return Response({'code': code, 'msg': 'success'})

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
        print('--1', pid, token)
        try:
            project = m.Project.objects.get(token=token, pk=pid)
            view.project = project
            return True
        except m.Project.DoesNotExist:
            print('--2')
            return False


class SelfReportApi(viewsets.ViewSet):
    authentication_classes = ()
    permission_classes = [SelfReportPermission]

    @action(['get'], detail=False)
    def get_init_data(self, req: Request):
        project = self.project
        # roots = project.wbs_set.filter(project_id=pid, level=0).all()
        # tasks = tree_for_nodes(roots)
        tasks = [{'value': x.id, 'label': x._code_name(), 'level': x.level} for x in
                 project.wbs_set.filter(project_id=project.id).all()]
        ret = {
            'code': 0,
            'msg': '返回项目初始信息成功',
            'company_name': project.company.name,
            'project_name': project.name,
            'staffs': [{'name': x.name, 'id': x.id} for x in project.company.staff_set.all()],
            'tasks': tasks
        }
        return Response(ret)

    @action(methods=['post'], detail=False)
    def save(self, req, *args, **kwargs):
        pid = req.GET.get('pid')


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
