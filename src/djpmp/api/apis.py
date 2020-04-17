# coding: utf-8
"""接口业务逻辑实现代码"""

from rest_framework import viewsets
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


class SelfReportApi(viewsets.ViewSet):
    authentication_classes = ()
    permission_classes = ()

    @action(['get'], detail=False)
    def get_init_data(self, req: Request):
        token = req.GET.get('token')
        pid = req.GET.get('pid')
        try:
            project = m.Project.objects.get(token=token, pk=pid)
        except m.Project.DoesNotExist:
            return Response({
                'code': -1,
                'msg': '项目不存在或令牌不对'
            })

        roots = project.wbs_set.filter(project_id=pid, level=0).all()
        tasks = []
        for i in roots:
            data = {'value': i.id, 'label': i.name}
            if not i.is_leaf_node():
                data['children'] = get_children(i)
            tasks.append(data)
        ret = {
            'code': 0,
            'msg': '返回项目初始信息成功',
            'company_name': project.company.name,
            'project_name': project.name,
            'staffs': [{'name': x.name, 'id': x.id} for x in project.company.staff_set.all()],
            'tasks': tasks
        }
        return Response(ret)


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
