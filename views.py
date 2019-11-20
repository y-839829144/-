from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, views
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import mixins
from collections import Counter
from datetime import timedelta

from rest_framework.views import APIView

from log.views import log_create
from.serializers import *
from .models import *
from .schemas import *
from .filters import *
import xlwt
from io import BytesIO

# Create your views here.


class AlarmListView(generics.ListAPIView):

    '''

         获取告警管理列表
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |am_addtime|告警添加时间|False|2019-10-25|
        |am_type_id|告警类型|True|int|
        |am_level_id|告警级别|True|int|
        |am_device|告警设备|False|string|
        |am_contene|告警内容|True|string|
        |am_status|告警状态|True|int|
        |am_deal_user|告警处理人|True|int|
        |am_deal_time|告警处理时间|False|2019-10-25|
        |am_deal_detail|告警处理说明|True|string|
        |am_audit_user|告警审核人|False|int|
        |am_audit_time|告警审核时间|True|2019-10-25|
        |scene_id|场景ID|True|int|
        |am_audit_detail|告警审核说明|True|string|




        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|


    '''
    queryset = Alarm_Management.objects.all()
    serializer_class = AlarmListSerializers
    module_perms = ['alarm.am_list']
    filter_backends = (DjangoFilterBackend,)
    filter_class = AlarmFilter


class AlarmManyTypeView(generics.ListAPIView):
    """
    告警类型列表

    """
    queryset =  Alarm_Management.objects.all()
    serializer_class = AlarmManyListSerializers
    schema = AlarmManySchema
    module_perms = ['alarm.am_type_list']
    def get_queryset(self):
        am_type_id = self.request.query_params.get('Type_id_id')
        queryset = Alarm_Management.objects.filter(am_type_id_id=am_type_id,am_status=1)
        user = self.request.user
        log_create(log_content='查看告警类型列表', log_module='告警管理', user=user)
        return queryset
class AlarmManyListView(views.APIView):
    '''

         批量处理列表
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |am_id   |批量处理ID|False| correct Type:   1，2，3, /error Type: 1 |




        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|


    '''

    module_perms = ['alarm.am_control']
    schema = AlarmManySchema1
    def post(self,request,*args,**kwargs):
        am_id = self.request.query_params.get('am_id')[:-1].split(',')
        am_deal_detail = self.request.query_params.get('am_deal_detail')

        try:
            for id in am_id:
                data = Alarm_Management.objects.get(id=id)
                data.am_audit_detail = am_deal_detail
                data.am_status = 3
                data.am_deal_user = self.request.user.id
                data.am_addtime = datetime.now()
                data.save()
        except:
            return Response(data={'code':400,'message':'修改失败'},status=status.HTTP_400_BAD_REQUEST)
        user = self.request.user
        log_create(log_content='告警批量处理', log_module='告警管理', user=user)
        return Response(data={'code':200,'message':'修改成功'},status=status.HTTP_200_OK)

class AlarmCreateView(generics.CreateAPIView):
    '''

         新增告警
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |am_type_id|告警类型|True|int|
        |am_level_id|告警级别|True|int|
        |am_device|告警设备|False|string|
        |am_contene|告警内容|True|string|
        |scene_id|场景ID|True|int|




        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|


    '''
    queryset = Alarm_Management.objects.all()
    serializer_class = AlarmCreateSerializers
    module_perms = ['alarm.am_control']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:  # 失败信息的定制
            serializer.is_valid(raise_exception=True)
        except:
            return Response(data={'code': 400, 'message': '添加失败'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # 成功后返回信息的定制
        res.data['code'] = 200
        res.data['message'] = '添加成功'
        user = self.request.user
        log_create(log_content='新增告警', log_module='告警管理', user=user)
        return res


class AlarmApplicationView(views.APIView):
    """
    告警单条处理
    """
    module_perms = ['alarm.am_control']
    schema = AlarmApplicationSchema
    def post(self,request):
        alarm_id  = self.request.query_params.get('alarm_id')
        alarm_dealtail = self.request.query_params.get('alarm_dealtail')
        try:
            alarm = Alarm_Management.objects.get(id = alarm_id)
            alarm.am_deal_time = datetime.now()
            alarm.am_status = 2
            alarm.am_deal_user =  self.request.user.id
            alarm.am_deal_detail = alarm_dealtail
            alarm.save()
        except:
            return Response(data={'code': 400, 'message': '修改失败'}, status=status.HTTP_400_BAD_REQUEST)
        user = self.request.user
        log_create(log_content='告警单条数据处理', log_module='告警管理', user=user)
        return Response(data={'code': 200, 'message': '修改成功'}, status=status.HTTP_200_OK)

class AlarmAuditView(views.APIView):
    '''

         告警审批
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |am_status|告警状态|True|int|
        |am_audit_user|告警审核人|False|int|
        |am_audit_time|告警审核时间|True|2019-10-25|
        |scene_id|场景ID|True|int|
        |am_audit_detail|告警审核说明|True|string|




        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|


    '''
    schema = AlarmAuditSchema
    module_perms = ['alarm.am_control']
    def post(self,request):
        try:
            alarm_id = self.request.query_params.get('alarm_id')
            am_audit_detail = self.request.query_params.get('am_audit_detail')
            alarm = Alarm_Management.objects.get(id = alarm_id)
            alarm.am_status = 3
            alarm.am_audit_detail = am_audit_detail
            alarm.am_audit_time = datetime.now()
            alarm.am_audit_user = self.request.user.id
            alarm.save()
        except:
            return Response(data={'code': 400, 'message': '修改失败'}, status=status.HTTP_400_BAD_REQUEST)
        user = self.request.user
        log_create(log_content='告警审批', log_module='告警管理', user=user)
        return Response(data={'code': 200, 'message': '修改成功'}, status=status.HTTP_200_OK)



class AlarmTypeCountView(views.APIView):
    '''

        各类型告警占比
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |start_time|筛选开始时间|True|2019-10-25|
        |end_time|筛选结束时间|True|2019-10-25|





        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|


    '''
    schema =  AlarmTypeCountSchema
    module_perms = ['alarm.am_control']
    def post(self,request):

        data = self.request.data['input_time']
        start_time = data['start_time']
        end_time = data['end_time']
        queryset = Alarm_Management.objects.filter(am_addtime__range=(start_time, end_time))
        type = []
        s = []
        for i in queryset:
            type.append(i.am_type_id_id)
        num = len(type)
        for j in type:
            s.append(str(round(type.count(j)/num*100,2))+'%')
        user = self.request.user
        log_create(log_content='各类型告警占比', log_module='告警管理', user=user)
        return Response(dict(zip(type,s)))


class SafeCountView(views.APIView):
    '''

        安防监测各状态告警数量占比
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |start_time|筛选开始时间|True|2019-10-25|
        |end_time|筛选结束时间|True|2019-10-25|





        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|


    '''
    schema =  SafeCountSchema
    module_perms = ['alarm.am_control']
    def post(self,request):
        safe_id = self.request.query_params.get('type_id')
        data = self.request.data['input_time']
        start_time = data['start_time']
        end_time = data['end_time']
        anfa = []
        s=[]
        queryset = Alarm_Management.objects.filter(am_addtime__range=(start_time, end_time),am_type_id=safe_id)
        for i in queryset:
            anfa.append(i.am_status)
        num = len(anfa)
        for j in anfa:
            s.append(str(round(anfa.count(j)/num*100,2))+'%')
        user = self.request.user
        log_create(log_content='安防监测各状态告警数量占比', log_module='告警管理', user=user)
        return Response(dict(zip(anfa,s)))


        
class DealCountView(views.APIView):

    module_perms = ['alarm.am_control']
    def post(self,request):
        data = Alarm_Management.objects.all()
        queryset = Alarm_Management.objects.filter(am_status=1)
        qcount = []
        for i in queryset:
            qcount.append(i)
        dealcount = len(qcount)
        allcount =  len(data)
        s = dealcount/allcount
        return Response(s,)

class NotDealTimeView(APIView):
    """
     未处理告警时间和
     ---
     #### 参数说明
     | 字段名称 | 描述 | 必须 | 类型 |
     | -- | -- | -- | -- |
     | alarm_time | 筛选时间段 | True | dict |


     #### 响应字段说明
     | 字段名称 | 描述 | 必须 | 类型 |
     | -- | -- | -- | -- |
     | code | 200 | -- | int |
     | sum_time | 未处理告警时间和 | -- | dict |

     #### 响应消息：
     | Http响应码 | 原因 | 响应模型 |
     | -- | -- | -- |
     | 200 | 请求成功 | 返回时间和 |
     """
    schema = AlarmTypePrecentSchema
    module_perms = ['alarm.am_list']


    def post(self, request):
        data = self.request.data['alarm_time']
        start_time = data['start_time']
        end_time = data['end_time']
        if not start_time:
            start_time = '1970-01-01 00:00:00'
        if not end_time:
            end_time = datetime.now()
        queryset = Alarm_Management.objects.filter(am_addtime__range=(start_time, end_time), am_status=1)
        user = self.request.user
        log_create(log_content='计算未处理告警时间和', log_module='告警管理', user=user)
        return Response(data={'code': 200, 'sum_time': calculate_time(queryset)}, status=status.HTTP_200_OK)

def calculate_time(queryset):
    alarm_time = []
    for time in queryset:
        alarm_time.append(time.am_addtime)
    result = {}
    print(Counter(alarm_time))
    for key, value in Counter(alarm_time).items():
        result[key.strftime('%Y-%m-%d %H:%M:%S')] = round(((datetime.now() - key).total_seconds() * value) / 60, 0)
    return result



