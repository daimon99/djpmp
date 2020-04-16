# coding: utf-8
"""接口业务逻辑实现代码"""

from rest_framework import viewsets

# from .serializers import ProjectSerializer, ContractSerializer
from .. import models as m
from . import serializers


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
