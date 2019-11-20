from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import mixins
from .models import Log
from .serializers import *
from .filters import *


# Create your views here.

def log_create(log_content, log_module, user, scene_id=None):

    log = Log()
    log.user_id_id = user.id
    log.log_module = log_module
    log.log_addtime = datetime.now()
    log.log_content = log_content

    if scene_id:
        log.scene_id = scene_id
    try:

        log.save()

    except Exception as e:
        raise RuntimeError('日志插入错误'+str(e))

    return True


class LogListView(generics.ListAPIView):
    """
    日志列表查询
    """
    queryset = Log.objects.all()
    serializer_class = LogSerializers
    module_perms = ['log.log_view']

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('user_id', 'log_content')  # 模糊查询 搜索
    ordering_fields = ('-log_addtime')  # 默认时间降序排列
    filter_class = LogFilter

    def get_queryset(self):
        log_id = self.request.query_params.get('log_id', '')
        if log_id:
            queryset = Log.objects.filter(pk=log_id)  # 获取具体日志的信息
        else:
            queryset = Log.objects.all()
        return queryset


class LogCreateView(generics.CreateAPIView):
    """
    创建日志
    """
    serializer_class = LogSerializers
    module_perms = ['log.log_view']

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
        return res



