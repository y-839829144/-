from django.db import models
from django.conf import settings
# Create your models here.
from datetime import datetime

class Log(models.Model):
    log_addtime = models.DateTimeField(default=datetime.now,verbose_name='日志添加时间')
    log_content = models.CharField(max_length=255,verbose_name='日志内容')
    user_id  = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='操作用户')
    log_module = models.CharField(max_length=255,verbose_name='所属模块')
    scene_id = models.IntegerField(verbose_name='所属场景',null=True,blank=True)


    class Meta:
        verbose_name = '日志表'
        permissions = (
            ('log_view', '日志查看'),
        )

