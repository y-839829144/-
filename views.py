from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import mixins

from log.views import log_create
from .models import *
from.serializers import *
from .schemas import *
# Create your views here.



class VideoListView(generics.ListAPIView):
    '''
            1 获取视频资源列表
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |vr_owner|视频所属-用户查询|False|int|
        |vr_permission|用户权限搜索(0, "VIP"),(1, "FREE"),(2, "OTHER")|False|int|
        |vr_format|格式|False|string|
        |vr_enable|可以状态(1, "可用"),(0, "不可用")|False|int|
        |videp_id|视频id|False|int|
        |catalogue|编目id|False|int|
        |catalogue_path|编码路径|False|int|
        |vr_created_time_start|查找开始时间|False|2019-02-03|
        |vr_created_time_end|结束时间|False|2019-02-03|
        |bytime|是否按时间排序|False|string|
        |byhot|是否按照热度排序（暂时为观看量）|False|string|


        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |video_id|视频id|--|int|
        |video_name|视频名|--|string|
        |video_url|视频地址|--|string|
        |video_owner|视频所属(0, "杰普资源"),(1, "网络资源")|--|int|
        |video_permission|视频权限(0, "VIP"),(1, "FREE"),(2, "OTHER")|--|int|
        |video_format|视频格式专辑or视频|--|string|
        |video_created_time|视频创建时间|--|string|
        |video_enable|视频状态-是否可以(1, "可用"),(0, "不可用")|--|int|
        |va|所属专辑|--|dict|
        |va_id|视频专辑id|--|int|
        |va_user|视频所属用户名|--|string|
        |va_va_name|视频专辑名称|--|string|
        |vr_cata_one|技术|--|string|
        |vr_cata_two|方向|--|string|
        |vr_play_times|阅读次数|--|string|
        |vr_favor_num|视频点赞次数|--|string|
        |vr_collection_num|视频收藏次数|--|string|
        |vr_comment_num|视频收藏次数|--|string|

        #### 注意说明
        - 1 列表中均为审核通过的视频,既 vr_audit_status=1
        - 2 vr_favor_num、vr_collection_num、vr_comment_num 假数据

        #### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回用户列表|
    '''
    serializer_class = VideoSerializers
    module_perms = ['video.video_view']
    schema = VideoListSchema
    def get_queryset(self):
        video_id = self.request.query_params.get('video_id', '')
        if video_id:
            queryset=Video.objects.filter(pk=video_id)
        else:
            queryset = Video.objects.all()
        return queryset


class VideoCreateView(generics.CreateAPIView):
    """
    创建视频
    """
    module_perms = ['video.video_control']
    serializer_class =VideoSerializers
    def create(self, request, *args, **kwargs):
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
        log_create(log_content='视频创建', log_module='视频管理', user=user)
        return res

class VideoDeleteView(generics.GenericAPIView):
    """
   视频删除
    """
    module_perms = ['video.video_control']
    schema = VideoListSchema
    serializer_class = VideoSerializers
    # 重写destory方法 ，自定义返回结果
    def get(self,request):
        # 获取地址url中的参数
        try:
            Video.objects.get(pk=self.request.query_params.get('video_id')).delete() # 使用get获取单条数据 ,使用filter会获取一个列表 列表为空不会报错
        except:
            return Response(data={'code':400,'message':'删除失败'},status=status.HTTP_400_BAD_REQUEST)
        user = self.request.user
        log_create(log_content='视频删除', log_module='视频管理', user=user)
        return Response(data={'code':200,'message':'删除成功'},status=status.HTTP_200_OK)

class VideoUpdateView(generics.GenericAPIView,mixins.UpdateModelMixin):
    """
    视频修改
    """
    module_perms = ['video.video_control']
    queryset = Video.objects.all()
    serializer_class = VideoSerializers
    def post(self,request,pk,*args,**kwargs):
        try:
            self.update(request, *args, **kwargs)
            print(1)
        except:
            return Response(data={
                'code':400,
                'message':'修改失败',
            },status=status.HTTP_400_BAD_REQUEST)
        user = self.request.user
        log_create(log_content='视频修改', log_module='视频管理', user=user)
        return Response(data={
                'code':200,
                'message':'修改成功',
            },status=status.HTTP_200_OK)


