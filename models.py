from django.db import models
from datetime import datetime

# Create your models here.


class Scene(models.Model):
    STATUS = (
        (1,'在线'),
        (2,'离线'),
    )


    scene_addtime = models.DateTimeField(default=datetime.now,verbose_name='场景添加时间')
    scene_name = models.CharField(max_length=255,verbose_name='场景名称')
    scene_code = models.CharField(max_length=255,verbose_name='场景识别码')
    scene_status = models.IntegerField(choices=STATUS,verbose_name='场景状态',default=1)
    scene_level = models.IntegerField(verbose_name='场景优先级')

    class Meta:
        verbose_name='场景表'
        permissions=(
            ('scene_view','场景浏览'),
            ('scene_control','场景控制')
        )


class Humidity(models.Model):
    STATUS = (
        (1,'正常'),
        (2,'异常'),
    )
    ONLINE = (
        (1,'在线'),
        (2,'离线'),
    )

    humidity_insert_time = models.DateTimeField(default=datetime.now,verbose_name='湿度更新时间')
    humidity_value = models.FloatField(verbose_name='湿度值')
    humidity_status = models.IntegerField(choices=STATUS,verbose_name='湿度传感器状态',default=1)
    humidity_online = models.IntegerField(choices=ONLINE,verbose_name='在线状态',default=1)
    scene_id = models.ForeignKey('Scene',on_delete=models.CASCADE,verbose_name='场景')

    class Meta:
        verbose_name = '湿度传感器表'
        ordering = ['-humidity_insert_time']

class Temperature(models.Model):
    STATUS = (
        (1,'正常'),
        (2,'异常'),
    )
    ONLINE = (
        (1,'在线'),
        (2,'离线'),
    )

    temperature_insert_time = models.DateTimeField(default=datetime.now,verbose_name='温度更新时间')
    temperature_value = models.FloatField(verbose_name='温度值')
    temperature_status = models.IntegerField(choices=STATUS,verbose_name='温度传感器状态',default=1)
    temperature_online = models.IntegerField(choices=ONLINE,verbose_name='在线状态',default=1)
    scene_id = models.ForeignKey('Scene',on_delete=models.CASCADE,verbose_name='场景')

    class Meta:
        verbose_name = '温度传感器表'
        ordering = ['-temperature_insert_time']


class Beam(models.Model):
    STATUS = (
        (1,'正常'),
        (2,'异常'),
    )
    ONLINE = (
        (1,'在线'),
        (2,'离线'),
    )

    beam_insert_time = models.DateTimeField(default=datetime.now,verbose_name='光照更新时间')
    beam_value = models.FloatField(verbose_name='光照强度值')
    beam_status = models.IntegerField(choices=STATUS,verbose_name='光照强度状态',default=1)
    beam_online = models.IntegerField(choices=ONLINE,verbose_name='在线状态',default=1)
    scene_id = models.ForeignKey('Scene',on_delete=models.CASCADE,verbose_name='场景')

    class Meta:
        verbose_name = '光照传感器表'
        ordering = ['-beam_insert_time']

class Co2(models.Model):
    STATUS = (
        (1,'正常'),
        (2,'异常'),
    )
    ONLINE = (
        (1,'在线'),
        (2,'离线'),
    )

    Co2_insert_time = models.DateTimeField(default=datetime.now,verbose_name='Co2的更新时间')
    Co2_value = models.FloatField(verbose_name='Co2的值')
    Co2_status = models.IntegerField(choices=STATUS,verbose_name='Co2的状态',default=1)
    Co2_online = models.IntegerField(choices=ONLINE,verbose_name='在线状态',default=1)
    scene_id = models.ForeignKey('Scene',on_delete=models.CASCADE,verbose_name='场景')


    class Meta:
        verbose_name = 'Co2传感器表'
        ordering = ['-Co2_insert_time']


class PM25(models.Model):
    STATUS = (
        (1,'正常'),
        (2,'异常'),
    )
    ONLINE = (
        (1,'在线'),
        (2,'离线'),
    )

    PM25_insert_time = models.DateTimeField(default=datetime.now,verbose_name='PM25的更新时间')
    PM25_value = models.FloatField(verbose_name='PM25的值')
    PM25_status = models.IntegerField(choices=STATUS,verbose_name='PM25的状态',default=1)
    PM25_online = models.IntegerField(choices=ONLINE,verbose_name='在线状态',default=1)
    scene_id = models.ForeignKey('Scene',on_delete=models.CASCADE,verbose_name='场景')

    class Meta:
        verbose_name = 'PM2.5传感器表'
        ordering = ['-PM25_insert_time']


class Smoke(models.Model):
    STATUS = (
        (1,'正常'),
        (2,'异常'),
    )
    ONLINE = (
        (1,'在线'),
        (2,'离线'),
    )

    Smoke_insert_time = models.DateTimeField(default=datetime.now,verbose_name='烟雾的更新时间')
    Smoke_status = models.IntegerField(choices=STATUS,verbose_name='烟雾的状态',default=1)
    Smoke_online = models.IntegerField(choices=ONLINE,verbose_name='在线状态',default=1)
    scene_id = models.ForeignKey('Scene',on_delete=models.CASCADE,verbose_name='场景')


    class Meta:
        verbose_name = '烟雾传感器表'
        ordering = ['-Smoke_insert_time']


class Flame(models.Model):
    STATUS = (
        (1,'正常'),
        (2,'异常'),
    )
    ONLINE = (
        (1,'在线'),
        (2,'离线'),
    )

    Flame_insert_time = models.DateTimeField(default=datetime.now,verbose_name='火光的更新时间')
    Flame_status = models.IntegerField(choices=STATUS,verbose_name='火光的状态',default=1)
    Flame_online = models.IntegerField(choices=ONLINE,verbose_name='在线状态',default=1)
    scene_id = models.ForeignKey('Scene',on_delete=models.CASCADE,verbose_name='场景')

    class Meta:
        verbose_name = '火光传感器表'
        ordering = ['-Flame_insert_time']

class Methane(models.Model):
    STATUS = (
        (1,'正常'),
        (2,'异常'),
    )
    ONLINE = (
        (1,'在线'),
        (2,'离线'),
    )

    Methane_insert_time = models.DateTimeField(default=datetime.now,verbose_name='甲烷的更新时间')
    Methane_status = models.IntegerField(choices=STATUS,verbose_name='甲烷的状态',default=1)
    Methane_online = models.IntegerField(choices=ONLINE,verbose_name='在线状态',default=1)
    scene_id = models.ForeignKey('Scene',on_delete=models.CASCADE,verbose_name='场景')


    class Meta:
        verbose_name = '甲烷传感器表'
        ordering = ['-Methane_insert_time']


class AlarmLamp(models.Model):
    STATUS = (
        (1,'正常'),
        (2,'异常'),
    )
    ONLINE = (
        (1,'在线'),
        (2,'离线'),
    )

    AlarmLamp_insert_time = models.DateTimeField(default=datetime.now,verbose_name='报警灯的更新时间')
    AlarmLamp_status = models.IntegerField(choices=STATUS,verbose_name='报警灯的状态',default=1)
    AlarmLamp_online = models.IntegerField(choices=ONLINE,verbose_name='在线状态',default=1)
    scene_id = models.ForeignKey('Scene',on_delete=models.CASCADE,verbose_name='场景')


    class Meta:
        verbose_name = '报警灯表'
        ordering = ['-AlarmLamp_insert_time']



class Alertor(models.Model):
    STATUS = (
        (1,'正常'),
        (2,'异常'),
    )
    ONLINE = (
        (1,'在线'),
        (2,'离线'),
    )

    Alertor_insert_time = models.DateTimeField(default=datetime.now,verbose_name='报警器的更新时间')
    Alertor_status = models.IntegerField(choices=STATUS,verbose_name='报警器的状态',default=1)
    Alertor_online = models.IntegerField(choices=ONLINE,verbose_name='在线状态',default=1)
    scene_id = models.ForeignKey('Scene',on_delete=models.CASCADE,verbose_name='场景')

    class Meta:
        verbose_name = '报警器表'
        ordering = ['-Alertor_insert_time']


class Display(models.Model):
    STATUS = (
        (1,'正常'),
        (2,'异常'),
    )
    ONLINE = (
        (1,'在线'),
        (2,'离线'),
    )

    Display_insert_time = models.DateTimeField(default=datetime.now,verbose_name='显示内容更新时间')
    Display_content = models.CharField(max_length=255,verbose_name='显示内容')
    Display_status = models.IntegerField(choices=STATUS,verbose_name='显示器的状态',default=1)
    Display_online = models.IntegerField(choices=ONLINE,verbose_name='在线状态',default=1)
    scene_id = models.ForeignKey('Scene',on_delete=models.CASCADE,verbose_name='场景')


    class Meta:
        verbose_name = '显示器表'
        ordering = ['-Display_insert_time']

class Light(models.Model):
    STATUS = (
        (1,'正常'),
        (2,'异常'),
    )
    ONLINE = (
        (1,'在线'),
        (2,'离线'),
    )

    Light_insert_time = models.DateTimeField(default=datetime.now,verbose_name='灯光数据更新时间')
    Light_status = models.IntegerField(choices=STATUS,verbose_name='灯光状态',default=1)
    Light_online = models.IntegerField(choices=ONLINE,verbose_name='在线状态',default=1)
    scene_id = models.ForeignKey('Scene',on_delete=models.CASCADE,verbose_name='场景')

    class Meta:
        verbose_name = '灯光传感器表'
        ordering = ['-Light_insert_time']

class Pump(models.Model):
    STATUS = (
        (1,'正常'),
        (2,'异常'),
    )
    ONLINE = (
        (1,'在线'),
        (2,'离线'),
    )
    Pump_insert_time = models.DateTimeField(default=datetime.now,verbose_name='水泵更新时间')
    Pump_status = models.IntegerField(choices=STATUS,verbose_name='水泵状态',default=1)
    Pump_online = models.IntegerField(choices=ONLINE,verbose_name='在线状态',default=1)
    scene_id = models.ForeignKey('Scene',on_delete=models.CASCADE,verbose_name='场景')

    class Meta:
        verbose_name = '水泵传感器表'
        ordering = ['-Pump_insert_time']


class Fan(models.Model):
    STATUS = (
        (1,'正常'),
        (2,'异常'),
    )
    ONLINE = (
        (1,'在线'),
        (2,'离线'),
    )
    Fan_insert_time = models.DateTimeField(default=datetime.now,verbose_name='风扇更新时间')
    Fan_status = models.IntegerField(choices=STATUS,verbose_name='风扇状态',default=1)
    Fan_online = models.IntegerField(choices=ONLINE,verbose_name='在线状态',default=1)
    scene_id = models.ForeignKey('Scene', on_delete=models.CASCADE, verbose_name='场景')

    class Meta:
        verbose_name = '风扇传感器表'
        ordering = ['-Fan_insert_time']


class Unlocking(models.Model):
    STATUS = (
        (1,'正常'),
        (2,'异常'),
    )
    ONLINE = (
        (1,'在线'),
        (2,'离线'),
    )
    Unlocking_insert_time = models.DateTimeField(default=datetime.now,verbose_name='开锁记录更新时间')
    user_id = models.IntegerField(verbose_name='开锁用户')
    Unlocking_status = models.IntegerField(choices=STATUS,verbose_name='开锁状态',default=1)
    Unlocking_online = models.IntegerField(choices=ONLINE,verbose_name='在线状态',default=1)
    scene_id = models.ForeignKey('Scene',on_delete=models.CASCADE,verbose_name='场景')


    class Meta:
        verbose_name = '开锁传感器表'
        ordering = ['-Unlocking_insert_time']



class Invade(models.Model):
    STATUS = (
        (1,'正常'),
        (2,'异常'),
    )
    ONLINE = (
        (1,'在线'),
        (2,'离线'),
    )
    Invade_insert_time = models.DateTimeField(default=datetime.now,verbose_name='入侵监测更新时间')
    Invade_status = models.IntegerField(choices=STATUS,verbose_name='入侵状态',default=1)
    Invade_online = models.IntegerField(choices=ONLINE,verbose_name='在线状态',default=1)
    scene_id = models.ForeignKey('Scene',on_delete=models.CASCADE,verbose_name='场景')

    class Meta:
        verbose_name = '入侵检测传感器表'
        ordering = ['-Invade_insert_time']