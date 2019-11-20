from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

# Create your models here.
class UserProfile(AbstractUser):
    STATUS = (
        (1, '男'),
        (2, '女'),
        (3, '保密'),

    )
    STATUS1 = (
        (1,'可用'),
        (2,'禁用')
    )


    user_name = models.CharField(max_length=255,verbose_name='用户姓名')

    user_number = models.CharField(max_length=255,verbose_name='用户工号')
    user_tel = models.CharField(max_length=20,verbose_name='用户电话')
    user_gender = models.IntegerField(choices=STATUS,verbose_name='用户性别',default=3)

    user_status= models.IntegerField(choices=STATUS1,verbose_name='用户状态',default=1)
    user_detail = models.CharField(max_length=255,verbose_name='用户详情')
    user_picture = models.ImageField(upload_to='uploads/user/%Y/',verbose_name='用户头像')


    class Meta:
        verbose_name = '用户表'
        ordering = ['-last_login']
        permissions = (
            ('user_view','用户浏览'),
            ('user_control','用户管理'),
            ('permission_view','权限浏览'),
            ('permission_control','权限管理')
        )





