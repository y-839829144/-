from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, views
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import mixins

from log.views import log_create
from .models import *
from .serializers import *
from .schemas import *
# Create your views here.

class UserListView(generics.ListAPIView):

    '''

         获取用户管理列表
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |user_addtime|用户添加时间|False|2019-10-25|
        |user_name|用户名字|True|string|
        |user_number|用户工号|True|int|
        |user_tel|用户电话|False|string|
        |user_gender|用户性别|False|int|
        |user_status|用户状态|False|int|
        |user_detail|用户说明|False|string|
        |user_picture|用户头像|False|image|





        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|


    '''
    queryset = UserProfile.objects.all()
    serializer_class = UserListSerializers
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('user_name', 'user_tel')  # 模糊查询 搜索
    ordering_fields = ('date_joined')  # 默认创建时间升序排列
    module_perms = ['users.user_view']



class UserDetailView(generics.RetrieveAPIView):
    '''

         用户列表详情
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |user_addtime|用户添加时间|False|2019-10-25|
        |user_name|用户名字|True|string|
        |user_number|用户工号|True|int|
        |user_tel|用户电话|False|string|
        |user_gender|用户性别|False|int|
        |user_status|用户状态|False|int|
        |user_detail|用户说明|False|string|
        |user_picture|用户头像|False|image|





        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|


    '''
    queryset = UserProfile.objects.all()
    serializer_class = UserCreateSerializers
    module_perms = ['users.user_control']


class UserCreateView(generics.CreateAPIView):
    '''

         用户新增
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |user_name|用户名字|True|string|
        |user_number|用户工号|True|int|
        |user_tel|用户电话|False|string|
        |user_gender|用户性别|False|int|
        |user_detail|用户说明|False|string|






        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|


    '''
    serializer_class = UserCreateSerializers
    module_perms = ['users.user_control']
    # 自定义返回结果
    def create(self, request, *args, **kwargs):
        password = request.data['password']
        request.data['password'] = make_password(password)
        serializer = self.get_serializer(data=request.data)
        try: # 失败信息的定制
            serializer.is_valid(raise_exception=True)
        except:
            return Response(data={'code':400,'message':'创建失败'},status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        # 成功后返回信息的定制
        res.data['code'] = 200
        res.data['message'] = '创建成功'
        user = self.request.user
        log_create(log_content='用户创建', log_module='用户管理', user=user)
        return res

class UserDeleteView(generics.GenericAPIView):
    """
    用户删除
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserCreateSerializers
    module_perms = ['users.user_control']
    def get(self,request,pk):
        try:
            obj = UserProfile.objects.get(pk=pk)
            self.check_object_permissions(request,obj)
            if obj.is_active== False:
                UserProfile.objects.get(pk=pk).delete() # 使用get获取单条数据 ,使用filter会获取一个列表 列表为空不会报错
        except:
            return Response(data={'code':400,'message':'删除失败'},status=status.HTTP_400_BAD_REQUEST)
        user = self.request.user
        log_create(log_content='用户删除', log_module='用户管理', user=user)
        return Response(data={'code':200,'message':'删除成功'},status=status.HTTP_200_OK)


class UserUpdateView(generics.GenericAPIView,mixins.UpdateModelMixin):
    """
    用户修改
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserCreateSerializers
    module_perms = ['users.user_control']

    # 数据编辑post方式
    def post(self, request, pk, *args, **kwargs):
        # print('request:',request)
        # print('**kwargs',kwargs)
        # 调用updateModelMixin中的update方法
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            password = request.data['password']
            request.data['password'] = make_password(password)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except:
            return Response(data={'code': 400, 'message': '修改失败'}, status=status.HTTP_400_BAD_REQUEST)
        user = self.request.user
        log_create(log_content='用户修改', log_module='用户管理', user=user)
        return Response(data={'code': 200, 'message': '修改成功'}, status=status.HTTP_200_OK)
class UserActiveView(views.APIView):
    """
    用户冻结
    """
    module_perms = ['users.user_control']
    schema = ActiveUpdateSchema
    def post(self,request):
        try:
            data = self.request.data['User_active']
            user_status=data['user_status']
            queryset = UserProfile.objects.get(id=data['id'])
            queryset.user_status=user_status
            queryset.save()
        except:

            return Response(data={
                'code':400,
                'message':'修改失败',
            },status=status.HTTP_400_BAD_REQUEST)
        user = self.request.user
        log_create(log_content='用户冻结', log_module='用户管理', user=user)
        return Response(data={
                'code':200,
                'message':'修改成功',
            },status=status.HTTP_200_OK)
