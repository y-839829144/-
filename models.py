from django.db import models
from datetime import datetime
from scene.models import Scene
# Create your models here.


class Alarm_Type(models.Model):
    alarm_type_id = models.IntegerField(primary_key=True,verbose_name='告警类型')
    alarm_type_addtime = models.DateTimeField(default=datetime.now,verbose_name='告警类型添加时间')
    alarm_type_name = models.CharField(max_length=255,verbose_name='告警类型名称')
    alarm_type_detail = models.CharField(max_length=255,verbose_name='告警类型说明')

    class Meta:
        verbose_name = '告警类型表'
        permissions = (
            ('am_type_list','告警类型查看'),
        )


class Alarm_Level(models.Model):
    alarm_level_id  = models.IntegerField(primary_key=True,verbose_name='告警级别id')
    alarm_level_addtime = models.DateTimeField(default=datetime.now,verbose_name='告警级别添加时间')
    alarm_level_name = models.CharField(max_length=255,verbose_name='告警级别名称')
    alarm_level_detail = models.CharField(max_length=255,verbose_name='告警级别说明')

    class Meta:
        verbose_name = '告警级别表'



class Alarm_Management(models.Model):
    STATUS =(
        (1,'待处理'),
        (2,'待审核'),
        (3,'审核通过'),
        (4,'审核不通过'),
    )
    am_addtime = models.DateTimeField(default=datetime.now,verbose_name='告警添加时间')
    am_type_id = models.ForeignKey('Alarm_Type',on_delete=models.CASCADE,verbose_name='告警类型')
    am_level_id = models.ForeignKey('Alarm_Level',on_delete=models.CASCADE,verbose_name='告警级别')
    scene_id = models.ForeignKey(Scene,on_delete=models.CASCADE,verbose_name='所属场景id')
    am_device = models.CharField(max_length=255,verbose_name='告警设备')
    am_contene = models.CharField(max_length=255,verbose_name='告警内容')
    am_status = models.IntegerField(choices=STATUS,verbose_name='告警状态',default=1)
    am_deal_user = models.IntegerField(verbose_name='告警处理人')
    am_deal_time = models.DateTimeField(verbose_name='告警处理时间')
    am_deal_detail = models.CharField(max_length=255,verbose_name='告警处理说明')
    am_audit_user = models.IntegerField(verbose_name='告警审核人')
    am_audit_time = models.DateTimeField(verbose_name='告警审核时间')
    am_audit_detail = models.CharField(max_length=255,verbose_name='告警审核反馈')


    class Meta:
        verbose_name = '告警信息表'
        permissions = (
            ('am_list','告警查看'),
            ('am_control','告警控制'),
        )