from django.db import models
from datetime import datetime
from django.conf import settings
from scene.models import Scene
# Create your models here.


class Door_approval(models.Model):
    STATUS = (
        (1,'待审核'),
        (2,'已通过'),
        (3,'已拒绝'),
    )
    door_addtime = models.DateTimeField(default=datetime.now,verbose_name='门禁申请时间')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='门禁申请人')
    door_start = models.DateTimeField(verbose_name='申请开始时间')
    door_end = models.DateTimeField(verbose_name='申请结束时间')
    door_follow = models.CharField(max_length=255,verbose_name='随行人员')
    door_follownum = models.IntegerField(verbose_name='随行人数')
    door_detail = models.CharField(max_length=255,verbose_name='申请说明')
    door_status = models.IntegerField(choices=STATUS,verbose_name='申请状态',default=1)
    door_user = models.IntegerField(verbose_name='审核人',default=1)
    door_audittime = models.DateTimeField(verbose_name='审批时间')
    door_feedback = models.CharField(max_length=255,verbose_name='审批反馈')
    scene_id = models.ForeignKey(Scene,on_delete=models.CASCADE,verbose_name='场景')


    class Meta():
        verbose_name = '门禁表'
        permissions = (
            ('door_listview','门禁查看'),
            ('door_updateview','门禁审批'),
            ('door_countview','用户开门次数计算'),
            ('door_timeview','用户开门总时间计算')
        )