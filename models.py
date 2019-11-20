from django.db import models
from datetime import datetime
# Create your models here.


class Video(models.Model):

    video_addtime= models.DateTimeField(default=datetime.now,verbose_name='视频添加时间')
    video_name = models.CharField(max_length=255,verbose_name='视频名称')
    video_detail = models.CharField(max_length=255,verbose_name='视频描述')
    video_address = models.CharField(max_length=255,verbose_name='视频地址')
    video_user = models.CharField(max_length=255,verbose_name='用户名')
    video_passwd = models.CharField(max_length=255,verbose_name='密码')


    class Meta:
        verbose_name = '视频表'
        permissions = (
            ('video_view','视频查看'),
            ('video_control','视频控制'),
        )
