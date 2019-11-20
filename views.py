from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, views
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.views import APIView
from access.models import Door_approval
from alarm.models import Alarm_Management
from log.views import log_create
from .serializers import *
from scene.models import Scene
from .schemas import *
# Create your views here.

class IndexNumView(APIView):
    '''

         获取首页各状态的数据
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |scene  |场景在线数|False| / |
        |door |门禁待审批数|False| / |
        |alarm  |告警待审批数|False| / |
        |alarm_deal |告警待处理状态数|False| / |





        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|


    '''
    permission_classes = ()

    def post(self,request):
        scene = len(Scene.objects.filter(scene_status=1))
        door = len(Door_approval.objects.filter(door_status=1))
        alarm = len(Alarm_Management.objects.filter(am_status=2))
        alarm_deal = len(Alarm_Management.objects.filter(am_status=1))
        result = {}
        result['scene_online']=scene
        result['door_online']=door
        result['alarm_status1']=alarm
        result['alarm_status2']=alarm_deal
        user = self.request.user
        log_create(log_content='获取首页各状态数据', log_module='首页管理', user=user)
        return Response(result)

class IndexLockView(generics.ListAPIView):
    '''

         获取开锁信息记录
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|





        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|


    '''

    queryset = Unlocking.objects.all()
    serializer_class = IndexLockserializer
    permission_classes = ()


class IndexAlarmView(generics.ListAPIView):
    '''

         获取场景下告警设备信息
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |scene_id  |选取场景ID|False| correct Type:   1 /error Type: list |




        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|


    '''
    queryset = Alarm_Management.objects.all()
    serializer_class = IndexAlarmSerializer
    permission_classes = ()

    schema = IndexAlarmSchema
    def get_queryset(self):
        scene_id = self.request.query_params.get('scene_id')
        queryset = Alarm_Management.objects.filter(scene_id_id=scene_id)
        user = self.request.user
        log_create(log_content='获取场景下告警设备信息', log_module='首页管理', user=user)
        return queryset





