from datetime import datetime

from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, views
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import mixins

from log.views import log_create
from .models import Door_approval
from .serializers import AccessSerializer,AccessSerializer1
from .filters import AccessFilter
from .schemas import AccessUpdateSchema,CountSchema,DoorTimeSchema
# Create your views here.

class AccessListView(generics.ListAPIView):
    '''

        获取门禁管理列表
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |door_addtime|门禁增加时间|False|2019-10-25|
        |user_id|门禁申请人|True|int|
        |door_start|申请开始时间|True|2019-10-25|
        |door_end|申请结束时间|True|2019-10-25|
        |door_follow|随行人员|True|string|
        |door_follownum|随行人数|True|int|
        |door_detail|申请说明|True|string|
        |door_status|申请状态|False|int|
        |door_user|审核人|False|int|
        |door_audittime|审核时间|False|2019-10-25|
        |door_feedback|审批反馈|True|string|
        |scene_id|场景ID|False|int|




        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|


    '''
    queryset = Door_approval.objects.all()
    serializer_class = AccessSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = AccessFilter
    module_perms = ['access.door_listview']




class AccessCreateView(generics.CreateAPIView):
    '''

        门禁申请
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |door_start|申请开始时间|True|2019-10-25|
        |door_end|申请结束时间|True|2019-10-25|
        |door_follow|随行人员|True|string|
        |door_follownum|随行人数|True|int|
        |door_detail|申请说明|True|string|
        |scene_id|场景ID|False|int|




        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|


    '''
    serializer_class = AccessSerializer
    permission_classes = ()

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
        log_create(log_content='门禁申请', log_module='门禁管理', user=user)
        return res



class AccessUpdateView(views.APIView):
    '''

        门禁审批
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |door_status|申请状态|False|int|
        |door_feedback|审批反馈|True|string|





        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|


    '''
    module_perms = ['access.door_updateview']
    schema = AccessUpdateSchema
    def post(self,request):
        try:
            data = self.request.data['Door_approval']
            door_status = data['door_status']
            door_feedback = data['door_feedback']
            queryset = Door_approval.objects.get(id =data['id'])
            queryset.door_status = door_status
            queryset.door_addtime=datetime.now()
            queryset.door_feedback=door_feedback
            queryset.save()
        except:

            return Response(data={
                'code': 400,
                'message': '修改失败',
            }, status=status.HTTP_400_BAD_REQUEST)
        user = self.request.user
        log_create(log_content='门禁审批', log_module='门禁管理', user=user)
        return Response(data={
            'code': 200,
            'message': '修改成功',
        }, status=status.HTTP_200_OK)


class DoorCountView(views.APIView):
    '''

        用户申请开门次数计算占比
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
    schema = CountSchema
    module_perms = ['access.door_countview']

    def post(self,request):
        data = self.request.data['Count']
        start_time = data['start_time']
        end_time = data['end_time']
        queryset = Door_approval.objects.filter(door_addtime__range=(start_time,end_time))
        user=[]
        s=[]
        for i in queryset:
            user.append(i.user_id_id)
        num = len(user)
        set_user = set(user)
        for j in set_user:
            s.append(str(round(user.count(j)/num*100,2))+'%')
        user = self.request.user
        log_create(log_content='计算用户开门次数占比', log_module='门禁管理', user=user)
        return Response(dict(zip(set_user,s)))


class DoorTimeView(views.APIView):
    '''

        用户开门总时间占比
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
    schema = DoorTimeSchema
    module_perms = ['access.door_timeview']
    def post(self,request):
        data = self.request.data['Time']
        start_time = data['start_time']
        end_time = data['end_time']
        queryset = Door_approval.objects.filter(door_addtime__range=(start_time,end_time))
        user=[]
        users_id = []
        onetime=[]
        for i in queryset:
            user.append(i)
            users_id.append(i.user_id_id)
        user_id = set(users_id)
        k=[]
        for i in user_id:
            res=Door_approval.objects.filter(user_id_id=i)
            print(res)
            m=[]
            for j in res:
                m.append((j.door_end-j.door_start).seconds)
            print(m)
            n=sum(m)
            print(n)
            k.append(n)
            onetime.append(n)
        alltime = sum(onetime)
        bili = []
        for x in onetime:
            bili.append(str(round((x/alltime)*100,2))+'%')
        user = self.request.user
        log_create(log_content='计算用户开门总时间占比', log_module='门禁管理', user=user)
        return Response(dict(zip(user_id,bili)))






        # onetime = []
        # print(users_id)
        # for j in user:
        #     onetime.append((j.door_end-j.door_start).seconds)
        # sumtime = sum(onetime)
        # bili = []
        # for x in onetime:
        #     bili.append(str(round((x/sumtime)*100,2))+'%')
        # print(onetime)
        #
        # return Response(dict(zip(user_id,bili)))













