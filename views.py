from datetime import timedelta
from django.db import connection,utils
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, views
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.views import APIView

from log.views import log_create
from .models import *
from.serializers import *
from .schemas import *
# Create your views here.

class SceneListView(generics.ListAPIView):

    '''

         获取场景管理列表
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |scene_addtime|场景添加时间|False|2019-10-25|
        |scene_name|场景名字|True|string|
        |scene_code|场景码|True|string|
        |scene_status|场景状态|False|int|
        |scene_level|场景优先级别|False|int|





        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |code|200|查询成功|string|


    '''
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer
    module_perms = ['scene.scene_view']
class SceneCreateView(generics.CreateAPIView):

    '''

        新增场景管理列表
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |scene_name|场景名字|True|string|
        |scene_code|场景码|True|string|
        |scene_level|场景优先级别|False|int|





        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |code|200|新增成功|string|


    '''
    queryset = Scene.objects.all()
    module_perms = ['scene.scene_control']
    serializer_class = SceneCreateSerializer
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
        log_create(log_content='新增场景', log_module='场景管理', user=user)
        return res

class SceneUpdateView(views.APIView):

    '''

         修改场景管理列表
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |scene_name|场景名字|True|string|
        |scene_code|场景码|True|string|
        |scene_level|场景优先级别|False|int|





        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |code|200|修改成功|string|


    '''
    schema = SceneUpdateSchema
    module_perms = ['scene.scene_control']
    def post(self,request):
        try:
            scene_id = self.request.query_params.get('scene_id')
            data = self.request.data['scene']
            scene_name = data['scene_name']
            scene_code = data['scene_code']
            scene_level = data['scene_level']
            queryset = Scene.objects.get(id = scene_id)
            queryset.scene_addtime = datetime.now()
            queryset.scene_code = scene_code
            queryset.scene_level = scene_level
            queryset.scene_name = scene_name
            queryset.scene_status = 1
            queryset.save()
        except:

            return Response(data={
                'code': 400,
                'message': '修改失败',
            }, status=status.HTTP_400_BAD_REQUEST)
        user = self.request.user
        log_create(log_content='修改场景', log_module='场景管理', user=user)
        return Response(data={
            'code': 200,
            'message': '修改成功',
        }, status=status.HTTP_200_OK)

class SceneDeleteView(views.APIView):
    '''

             删除场景管理列表
            ---
            #### 参数说明
            |字段名称|描述|必须|类型|
            |--|--|--|--|
            |page|分页|True|int|
            |scene_|场景|True|int|






            #### 响应字段说明
            |字段名称|描述|必须|类型|
            |code|200|删除成功|string|


        '''
    schema =  SceneDeleteSchema
    module_perms = ['scene.scene_control']
    def get(self,request):
        try:
            Scene.objects.get(pk=self.request.query_params.get('scene_id')).delete() # 使用get获取单条数据 ,使用filter会获取一个列表 列表为空不会报错
        except:
            return Response(data={'code':400,'message':'删除失败'},status=status.HTTP_400_BAD_REQUEST)
        user = self.request.user
        log_create(log_content='删除场景', log_module='场景管理', user=user)
        return Response(data={'code':200,'message':'删除成功'},status=status.HTTP_200_OK)



class SceneDeviceView(APIView):
    '''

               场景设备部分列表
              ---
              #### 参数说明
              |字段名称|描述|必须|类型|
              |--|--|--|--|
              |page|分页|True|int|
              |scene_id|场景id|True|int|
              |humidity|湿度传感器|True|int|
              |temperature|温度传感器|True|int|
              |co2|二氧化碳|True|int|
              |pm25|PM2.5|True|int|
              |unlocking|开锁|True|int|







              #### 响应字段说明
              |字段名称|描述|必须|类型|
              |code|200|查看成功|string|


          '''
    schema = SceneListSchema
    module_perms = ['scene.scene_view']
    def get(self,request):
        device_status_dict={}
        scene_id = self.request.query_params.get('scene_id','')
        if scene_id:
            try:
                humidity = Humidity.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['humidity']=HumiditySerializer(humidity).data
                temperature = Temperature.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['temperature'] = TemperatureSerializer(temperature).data
                co2 = Co2.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['co2'] = Co2Serializer(co2).data
                pm25 = PM25.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['pm25'] = PM25Serializer(pm25).data
                methane = Methane.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['methane'] = MethaneSerializer(methane).data
                unlocking = Unlocking.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['unlocking'] = UnlockingSerializer(unlocking).data

            except:
                return Response(data={'message': '暂无数据'})
        else:
            try:
                humidity = Humidity.objects.filter(scene_id_id=1)[0]
                device_status_dict['humidity'] = HumiditySerializer(humidity).data
                temperature = Temperature.objects.filter(scene_id_id=1)[0]
                device_status_dict['temperature'] = TemperatureSerializer(temperature).data
                co2 = Co2.objects.filter(scene_id_id=1)[0]
                device_status_dict['co2'] = Co2Serializer(co2).data
                pm25 = PM25.objects.filter(scene_id_id=1)[0]
                device_status_dict['pm25'] = PM25Serializer(pm25).data
                methane = Methane.objects.filter(scene_id_id=1)[0]
                device_status_dict['methane'] = MethaneSerializer(methane).data
                unlocking = Unlocking.objects.filter(scene_id_id=1)[0]
                device_status_dict['unlocking'] = UnlockingSerializer(unlocking).data
            except:
                return Response(data={'message':'暂无数据'})
        user = self.request.user
        log_create(log_content='查看场景部分设备列表', log_module='场景管理', user=user)
        return Response(device_status_dict)

class SceneAllDeviceView(APIView):
    '''

               场景所有设备最新一条数据列表
              ---
              #### 参数说明
              |字段名称|描述|必须|类型|
              |--|--|--|--|
              |page|分页|True|int|
              |scene_id|场景id|True|int|
              |humidity|湿度传感器|True|int|
              |temperature|温度传感器|True|int|
              |co2|二氧化碳|True|int|
              |pm25|PM2.5|True|int|
              |beam|光照|True|int|
              |smoke|烟雾|True|int|
              |flame|火光|True|int|
              |alarmLamp|报警灯|True|int|
              |alertor|报警器|True|int||
              |fan|开锁|风扇|int|
              |invade|入侵检测|True|int|
              |pump|水泵|True|int|
              |light|灯光|True|int|








              #### 响应字段说明
              |字段名称|描述|必须|类型|
              |code|200|查看成功|string|


          '''
    schema = SceneListSchema
    module_perms = ['scene.scene_view']

    def get(self, request):
        device_status_dict = {}
        scene_id = self.request.query_params.get('scene_id', '')
        if scene_id:
            try:
                humidity = Humidity.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['humidity'] = HumiditySerializer(humidity).data
                temperature = Temperature.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['temperature'] = TemperatureSerializer(temperature).data
                co2 = Co2.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['co2'] = Co2Serializer(co2).data
                pm25 = PM25.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['pm25'] = PM25Serializer(pm25).data
                methane = Methane.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['methane'] = MethaneSerializer(methane).data
                unlocking = Unlocking.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['unlocking'] = UnlockingSerializer(unlocking).data
                beam = Beam.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['beam'] = BeamSerializer(beam).data
                smoke = Smoke.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['smoke'] = SmokeSerializer(smoke).data
                flame = Flame.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['flame'] = FlameSerializer(flame).data
                alarmLamp = AlarmLamp.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['alarmLamp'] = AlarmLampSerializer(alarmLamp).data
                alertor = Alertor.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['alertor'] = AlertorSerializer(alertor).data
                display = Display.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['display'] = DisplaySerializer(display).data
                light = Light.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['light'] = LightSerializer(light).data
                pump = Pump.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['pump'] = PumpSerializer(pump).data
                fan = Fan.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['fan'] = FanSerializer(fan).data
                invade = Invade.objects.filter(scene_id_id=scene_id)[0]
                device_status_dict['invade'] = InvadeSerializer(invade).data

            except:
                return Response(data={'message': '暂无数据'})
        else:
            try:
                humidity = Humidity.objects.filter(scene_id_id=1)[0]
                device_status_dict['humidity'] = HumiditySerializer(humidity).data
                temperature = Temperature.objects.filter(scene_id_id=1)[0]
                device_status_dict['temperature'] = TemperatureSerializer(temperature).data
                co2 = Co2.objects.filter(scene_id_id=1)[0]
                device_status_dict['co2'] = Co2Serializer(co2).data
                pm25 = PM25.objects.filter(scene_id_id=1)[0]
                device_status_dict['pm25'] = PM25Serializer(pm25).data
                methane = Methane.objects.filter(scene_id_id=1)[0]
                device_status_dict['methane'] = MethaneSerializer(methane).data
                unlocking = Unlocking.objects.filter(scene_id_id=1)[0]
                device_status_dict['unlocking'] = UnlockingSerializer(unlocking).data
                beam = Beam.objects.filter(scene_id_id=1)[0]
                device_status_dict['beam'] = BeamSerializer(beam).data
                smoke = Smoke.objects.filter(scene_id_id=1)[0]
                device_status_dict['smoke'] = SmokeSerializer(smoke).data
                flame = Flame.objects.filter(scene_id_id=1)[0]
                device_status_dict['flame'] = FlameSerializer(flame).data
                alarmLamp = AlarmLamp.objects.filter(scene_id_id=1)[0]
                device_status_dict['alarmLamp'] = AlarmLampSerializer(alarmLamp).data
                alertor = Alertor.objects.filter(scene_id_id=1)[0]
                device_status_dict['alertor'] = AlertorSerializer(alertor).data
                display = Display.objects.filter(scene_id_id=1)[0]
                device_status_dict['display'] = DisplaySerializer(display).data
                light = Light.objects.filter(scene_id_id=1)[0]
                device_status_dict['light'] = LightSerializer(light).data
                pump = Pump.objects.filter(scene_id_id=1)[0]
                device_status_dict['pump'] = PumpSerializer(pump).data
                fan = Fan.objects.filter(scene_id_id=1)[0]
                device_status_dict['fan'] = FanSerializer(fan).data
                invade = Invade.objects.filter(scene_id_id=1)[0]
                device_status_dict['invade'] = InvadeSerializer(invade).data
            except:
                return Response(data={'message': '暂无数据'})
        user = self.request.user
        log_create(log_content='查看场景所有设备信息', log_module='场景管理', user=user)
        return Response(device_status_dict)

class SceneFireHistoryView(APIView):
    '''

               消防历史记录
              ---
              #### 参数说明
              |字段名称|描述|必须|类型|
              |--|--|--|--|
              |page|分页|True|int|
              |scene_id|场景id|True|int|
              |humidity|湿度传感器|True|int|
              |temperature|温度传感器|True|int|
              |co2|二氧化碳|True|int|
              |pm25|PM2.5|True|int|
              |beam|光照|True|int|
              |smoke|烟雾|True|int|
              |flame|火光|True|int|
              |alarmLamp|报警灯|True|int|
              |alertor|报警器|True|int||
              |fan|开锁|风扇|int|
              |invade|入侵检测|True|int|
              |pump|水泵|True|int|
              |light|灯光|True|int|








              #### 响应字段说明
              |字段名称|描述|必须|类型|
              |code|200|查看成功|string|


          '''
    schema = SceneFireHistorySchema
    module_perms = ['scene.scene_view']
    def post(self, request):
        # 传了是字符串字符串，不传是当前时间字符串
        end_time = self.request.query_params.get('end_time', datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
        start_time = self.request.query_params.get('start_time', datetime.strftime(datetime.now() - timedelta(weeks=1), "%Y-%m-%d %H:%M:%S"))
        scene_id = self.request.query_params.get('scene_id')
        result_dict = {}
        smoke_sql = """SELECT DATE_FORMAT(smoke_insert_time,"%Y-%m-%d") from scene_smoke 
                    where Smoke_status = 2 and Smoke_insert_time> '{}' and Smoke_insert_time < '{}' and scene_id_id = {}
                    GROUP BY DATE_FORMAT(Smoke_insert_time,"%Y-%m-%d")
                    """

        result_dict['smoke'] = calculate_fire_history(end_time, start_time, scene_id, smoke_sql)
        flame_sql = """SELECT DATE_FORMAT(Flame_insert_time,"%Y-%m-%d") from scene_flame 
                    where Flame_status = 2 and Flame_insert_time> '{}' and Flame_insert_time < '{}' and scene_id_id = {}
                    GROUP BY DATE_FORMAT(Flame_insert_time,"%Y-%m-%d")
                    """

        result_dict['flame'] = calculate_fire_history(end_time, start_time, scene_id, flame_sql)
        methane_sql = """SELECT DATE_FORMAT(Methane_insert_time,"%Y-%m-%d") from scene_methane 
                    where Methane_status = 2 and Methane_insert_time> '{}' and Methane_insert_time < '{}' and scene_id_id = {}
                    GROUP BY DATE_FORMAT(Methane_insert_time,"%Y-%m-%d")
                    """

        result_dict['methane'] = calculate_fire_history(end_time, start_time, scene_id, methane_sql)
        alarmlamp_sql = """SELECT DATE_FORMAT(AlarmLamp_insert_time,"%Y-%m-%d") from scene_alarmlamp 
                        where AlarmLamp_status = 2 and AlarmLamp_insert_time> '{}' and AlarmLamp_insert_time < '{}' and scene_id_id = {}
                        GROUP BY DATE_FORMAT(AlarmLamp_insert_time,"%Y-%m-%d")
                        """

        result_dict['alarmlamp'] = calculate_fire_history(end_time, start_time, scene_id, alarmlamp_sql)
        alertor_sql = """SELECT DATE_FORMAT(Alertor_insert_time,"%Y-%m-%d") from scene_alertor 
                    where Alertor_status = 2 and Alertor_insert_time> '{}' and Alertor_insert_time < '{}' and scene_id_id = {}
                    GROUP BY DATE_FORMAT(Alertor_insert_time,"%Y-%m-%d")
                    """

        result_dict['alertor'] = calculate_fire_history(end_time, start_time, scene_id, alertor_sql)
        user = self.request.user
        log_create(log_content='查看消防历史记录', log_module='场景管理', user=user)
        return Response(result_dict)


def calculate_fire_history(end_time, start_time, scene_id, sql):
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') + timedelta(days=1)  # 转化成时间加一天
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') - timedelta(days=1)  # 开始时间减一天
    end_time = datetime.strftime(end_time, '%Y-%m-%d')  # 结束时间去掉时分秒并转化成字符串
    start_time = datetime.strftime(start_time, '%Y-%m-%d')
    cursor = connection.cursor()
    sql = sql.format(start_time, end_time, scene_id)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    data = {}
    end_time_date = datetime.strptime(end_time, '%Y-%m-%d')  # 结束时间转化成时间类型
    start_time_date = datetime.strptime(start_time, '%Y-%m-%d') + timedelta(days=1)
    while end_time_date > start_time_date:
        end_time_date = end_time_date - timedelta(days=1)  # 减一天
        end_time = datetime.strftime(end_time_date, '%Y-%m-%d')  # 转化成字符串
        if result:
            for j in result:
                if end_time in j:
                    data[end_time] = '有'
                    break
                else:
                    data[end_time] = '无'
        else:
            data[end_time] = '无'
    return data



class SceneFireAlarmView(generics.ListAPIView):
    '''

               消防告警时长
              ---
              #### 参数说明
              |字段名称|描述|必须|类型|
              |--|--|--|--|
              |page|分页|True|int|
              |scene_id|场景id|True|int|
              |humidity|湿度传感器|True|int|
              |temperature|温度传感器|True|int|
              |co2|二氧化碳|True|int|
              |pm25|PM2.5|True|int|
              |beam|光照|True|int|
              |smoke|烟雾|True|int|
              |flame|火光|True|int|
              |alarmLamp|报警灯|True|int|
              |alertor|报警器|True|int||
              |fan|开锁|风扇|int|
              |invade|入侵检测|True|int|
              |pump|水泵|True|int|
              |light|灯光|True|int|








              #### 响应字段说明
              |字段名称|描述|必须|类型|
              |code|200|查看成功|string|


          '''
    serializer_class = SceneFireAlarmSerializers
    schema = SceneFireHistorySchema
    module_perms = ['scene.scene_view']

    def get_queryset(self):
        start_time = self.request.query_params.get('start_time', '1970-01-01 00:00:00')
        end_time = self.request.query_params.get('end_time', datetime.now())
        scene_id = self.request.query_params.get('scene_id')
        queryset = Alarm_Management.objects.filter(scene_id_id=scene_id, am_addtime__range=(start_time, end_time), am_type_id=2)
        for i in queryset:
            if i.am_deal_time:
                i.sum_time = round((i.am_deal_time - i.am_addtime).total_seconds() / 60, 2)
            else:
                i.sum_time = round((datetime.now() - i.am_addtime).total_seconds() / 60, 2)
        user = self.request.user
        log_create(log_content='消防告警时长', log_module='场景管理', user=user)
        return queryset

class SceneEnvironmentHistoryView(APIView):
    """
    环境监测历史记录
    """
    schema = SceneEnvironmentHistorySchema
    module_perms = ['scene.scene_view']

    def post(self, request):
        end_time = self.request.query_params.get('end_time', datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
        start_time = self.request.query_params.get('start_time', datetime.strftime(datetime.now() - timedelta(weeks=1), "%Y-%m-%d %H:%M:%S"))
        scene_id = self.request.query_params.get('scene_id')
        scene_env_device = self.request.query_params.get('scene_env_device')
        result_dict = {}
        if scene_env_device == '湿度传感器':
            humidity_sql = """SELECT DATE_FORMAT(humidity_insert_time,"%Y-%m-%d"),avg(humidity_value) from scene_humidity 
                        where humidity_insert_time> '{}' and humidity_insert_time < '{}' and scene_id_id = {}
                        GROUP BY DATE_FORMAT(humidity_insert_time,"%Y-%m-%d")
                        """
            result_dict['humidity'] = calculate_environment_history(end_time, start_time, scene_id, humidity_sql)
        if scene_env_device == '温度传感器':
            temperature_sql = """SELECT DATE_FORMAT(temperature_insert_time,"%Y-%m-%d"),avg(temperature_value) from scene_temperature
                        where temperature_insert_time> '{}' and temperature_insert_time < '{}' and scene_id_id = {}
                        GROUP BY DATE_FORMAT(temperature_insert_time,"%Y-%m-%d")
                        """
            result_dict['temperature'] = calculate_environment_history(end_time, start_time, scene_id, temperature_sql)
        if scene_env_device == '光照强度传感器':
            beam_sql = """SELECT DATE_FORMAT(beam_insert_time,"%Y-%m-%d"),avg(beam_value) from scene_beam
                        where beam_insert_time> '{}' and beam_insert_time < '{}' and scene_id_id = {}
                        GROUP BY DATE_FORMAT(beam_insert_time,"%Y-%m-%d")
                        """
            result_dict['berm'] = calculate_environment_history(end_time, start_time, scene_id, beam_sql)
        if scene_env_device == 'Co2传感器':
            co2_sql = """SELECT DATE_FORMAT(Co2_insert_time,"%Y-%m-%d"),avg(Co2_value) from scene_co2
                        where Co2_insert_time> '{}' and Co2_insert_time < '{}' and scene_id_id = {}
                        GROUP BY DATE_FORMAT(Co2_insert_time,"%Y-%m-%d")
                        """
            result_dict['co2'] = calculate_environment_history(end_time, start_time, scene_id, co2_sql)
        if scene_env_device == 'Pm2.5传感器':
            pm25_sql = """SELECT DATE_FORMAT(PM25_insert_time,"%Y-%m-%d"),avg(PM25_value) from scene_pm25
                        where PM25_insert_time> '{}' and PM25_insert_time < '{}' and scene_id_id = {}
                        GROUP BY DATE_FORMAT(PM25_insert_time,"%Y-%m-%d")
                        """
            result_dict['pm25'] = calculate_environment_history(end_time, start_time, scene_id, pm25_sql)
        user = self.request.user
        log_create(log_content='环境监测历史记录', log_module='场景管理', user=user)
        return Response(result_dict)


def calculate_environment_history(end_time, start_time, scene_id, sql):
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') + timedelta(days=1)  # 转化成时间加一天
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') - timedelta(days=1)  # 开始时间减一天
    end_time = datetime.strftime(end_time, '%Y-%m-%d')  # 结束时间去掉时分秒并转化成字符串
    start_time = datetime.strftime(start_time, '%Y-%m-%d')
    cursor = connection.cursor()
    sql = sql.format(start_time, end_time, scene_id)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    data = {}
    end_time_date = datetime.strptime(end_time, '%Y-%m-%d')  # 结束时间转化成时间类型
    start_time_date = datetime.strptime(start_time, '%Y-%m-%d') + timedelta(days=1)
    while end_time_date > start_time_date:
        end_time_date = end_time_date - timedelta(days=1)  # 减一天
        end_time = datetime.strftime(end_time_date, '%Y-%m-%d')  # 转化成字符串
        if result:
            for j in result:
                if end_time in j:
                    data[end_time] = j[1]
                    break
                else:
                    data[end_time] = 0
        else:
            data[end_time] = 0
    return data
class SceneEnvironmentAlarmView(generics.ListAPIView):
    """
    环境类型告警
    """
    serializer_class = SceneFireAlarmSerializers
    schema = SceneEnvironmentAlarmSchema
    module_perms = ['scene.scene_view']

    def get_queryset(self):
        start_time = self.request.query_params.get('start_time', '1970-01-01 00:00:00')
        end_time = self.request.query_params.get('end_time', datetime.now())
        scene_id = self.request.query_params.get('scene_id')
        scene_env_device = self.request.query_params.get('scene_env_device')
        queryset = Alarm_Management.objects.filter(scene_id=scene_id, am_addtime__range=(start_time, end_time), am_device=scene_env_device)
        for i in queryset:
            if i.am_deal_time:
                i.sum_time = round((i.am_deal_time - i.am_addtime).total_seconds() / 60, 2)
            else:
                i.sum_time = round((datetime.now() - i.am_addtime).total_seconds() / 60, 2)
        user = self.request.user
        log_create(log_content='环境类型告警', log_module='场景管理', user=user)
        return queryset


# 新增显示屏显示内容
class SceneDisplayCreateView(generics.CreateAPIView):
    """
    新增显示屏显示内容
    """
    serializer_class = DisplaySerializers1
    module_perms = ['scene.scene_control']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response(data={'code': 400, 'message': '新增失败'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        res.data['code'] = 200
        res.data['message'] = '新增成功'
        user = self.request.user
        log_create(log_content='新增显示屏显示内容', log_module='场景管理', user=user)
        return res


# 水泵、灯光、风扇数据统计图
class SceneDeviceHistoryView(APIView):
    """
    水泵、灯光、风扇数据统计图
    """
    schema = SceneFireHistorySchema
    module_perms = ['scene.scene_view']

    def post(self, request):
        # 传了是字符串字符串，不传是当前时间字符串
        end_time = self.request.query_params.get('end_time', datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
        start_time = self.request.query_params.get('start_time', datetime.strftime(datetime.now() - timedelta(weeks=1), "%Y-%m-%d %H:%M:%S"))
        scene_id = self.request.query_params.get('scene_id')
        result_dict = {}
        light_sql = """SELECT DATE_FORMAT(Light_insert_time,"%Y-%m-%d") from scene_light 
                    where Light_status = 2 and Light_insert_time> '{}' and Light_insert_time < '{}' and scene_id_id = {}
                    GROUP BY DATE_FORMAT(Light_insert_time,"%Y-%m-%d")
                    """
        result_dict['light'] = calculate_fire_history(end_time, start_time, scene_id, light_sql)
        pump_sql = """SELECT DATE_FORMAT(Pump_insert_time,"%Y-%m-%d") from scene_pump 
                    where Pump_status = 2 and Pump_insert_time> '{}' and Pump_insert_time < '{}' and scene_id_id = {}
                    GROUP BY DATE_FORMAT(Pump_insert_time,"%Y-%m-%d")
                    """
        result_dict['pump'] = calculate_fire_history(end_time, start_time, scene_id, pump_sql)
        fan_sql = """SELECT DATE_FORMAT(Fan_insert_time,"%Y-%m-%d") from scene_fan 
                    where Fan_status = 2 and Fan_insert_time> '{}' and Fan_insert_time < '{}' and scene_id_id = {}
                    GROUP BY DATE_FORMAT(Fan_insert_time,"%Y-%m-%d")
                    """
        result_dict['fan'] = calculate_fire_history(end_time, start_time, scene_id, fan_sql)
        user = self.request.user
        log_create(log_content='水泵灯光风扇数据统计图', log_module='场景管理', user=user)
        return Response(result_dict)


# 水泵、灯光、风扇数据打开占比图
class SceneDeviceOpenView(APIView):
    """
    水泵、灯光、风扇数据打开占比图
    """
    schema = SceneFireHistorySchema
    module_perms = ['scene.scene_view']

    def post(self, request):
        start_time = self.request.query_params.get('start_time', '1970-01-01 00:00:00')
        end_time = self.request.query_params.get('end_time', datetime.now())
        scene_id = self.request.query_params.get('scene_id')
        light = Light.objects.filter(Light_insert_time__range=(start_time, end_time), scene_id_id=scene_id)
        light_count = 0
        for i in range(len(light)-1):
            if light[i].Light_online != light[i+1].Light_online:
                if light[i].Light_online == 1:
                    light_count += 1
        if light[len(light)-1].Light_online == 1:
            light_count += 1
        pump = Pump.objects.filter(Pump_insert_time__range=(start_time, end_time), scene_id_id=scene_id)
        pump_count = 0
        for i in range(len(pump)-1):
            if pump[i].Pump_online != pump[i+1].Pump_online:
                if pump[i].Pump_online == 1:
                    pump_count += 1
        if pump[len(pump)-1].Pump_online == 1:
            pump_count += 1
        fan = Fan.objects.filter(Fan_insert_time__range=(start_time, end_time), scene_id_id=scene_id)
        fan_count = 0
        for i in range(len(fan) - 1):
            if fan[i].Fan_online != fan[i + 1].Fan_online:
                if fan[i].Fan_online == 1:
                    fan_count += 1
        if fan[len(fan)-1].Fan_online == 1:
            fan_count += 1
        light_precent = str(round(light_count / (light_count + pump_count + fan_count), 4)*100) + '%'
        pump_precent = str(round(pump_count / (light_count + pump_count + fan_count), 4) * 100) + '%'
        fan_precent = str(round(fan_count / (light_count + pump_count + fan_count), 4) * 100) + '%'
        light_data = []
        light_data.append(light_count)
        light_data.append(light_precent)
        pump_data = []
        pump_data.append(pump_count)
        pump_data.append(pump_precent)
        fan_data = []
        fan_data.append(fan_count)
        fan_data.append(fan_precent)
        result = {}
        result['light'] = light_data
        result['pump'] = pump_data
        result['fan'] = fan_data
        user = self.request.user
        log_create(log_content='水泵风扇灯光打开占比图', log_module='场景管理', user=user)
        return Response(result)
class SceneLightUponView(views.APIView):
    '''

             灯光传感器改变在线状态
            ---
            #### 参数说明
            |字段名称|描述|必须|类型|
            |--|--|--|--|
            |page|分页|True|int|
            |light_id   |灯光传感器ID||      |
            |light_online |灯光传感器在线状态|True:1|False:2      |




            #### 响应字段说明
            |字段名称|描述|必须|类型|
            |--|--|--|--|


        '''
    schema = LightSchema
    module_perms = ['scene.scene_view']
    def post(self,request,*args,**kwargs):
        try:
            light_id = self.request.query_params.get('light_id')
            light_online = self.request.query_params.get('light_online')
            queryset = Light.objects.get(id =light_id)
            queryset.Light_online =light_online
            queryset.save()
        except:
            return Response(data={'code':400,'message':'修改失败'},status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'code':200,'message':'修改成功'},status=status.HTTP_200_OK)

class ScenePumpUponView(views.APIView):
    '''

             水泵传感器改变在线状态
            ---
            #### 参数说明
            |字段名称|描述|必须|类型|
            |--|--|--|--|
            |page|分页|True|int|
            |pump_id   |水泵传感器ID||      |
            |pump_online |水泵传感器在线状态|True:1|False:2      |




            #### 响应字段说明
            |字段名称|描述|必须|类型|
            |--|--|--|--|


        '''
    schema = PumpSchema
    module_perms = ['scene.scene_view']
    def post(self,request,*args,**kwargs):
        try:
            pump_id = self.request.query_params.get('pump_id')
            pump_online = self.request.query_params.get('pump_online')
            queryset = Pump.objects.get(id =pump_id)
            queryset.Light_online =pump_online
            queryset.save()
        except:
            return Response(data={'code':400,'message':'修改失败'},status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'code':200,'message':'修改成功'},status=status.HTTP_200_OK)

class SceneFanUponView(views.APIView):
    '''

             风扇传感器改变在线状态
            ---
            #### 参数说明
            |字段名称|描述|必须|类型|
            |--|--|--|--|
            |page|分页|True|int|
            |fan_id   |风扇传感器ID||      |
            |fan_online |风扇传感器在线状态|True:1|False:2      |




            #### 响应字段说明
            |字段名称|描述|必须|类型|
            |--|--|--|--|


        '''
    schema = FanSchema
    module_perms = ['scene.scene_view']
    def post(self,request,*args,**kwargs):
        try:
            fan_id = self.request.query_params.get('fan_id')
            fan_online = self.request.query_params.get('fan_online')
            queryset = Fan.objects.get(id =fan_id)
            queryset.fan_online =fan_online
            queryset.save()
        except:
            return Response(data={'code':400,'message':'修改失败'},status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'code':200,'message':'修改成功'},status=status.HTTP_200_OK)

class SceneAlertorUponView(views.APIView):
    '''

             报警器改变在线状态
            ---
            #### 参数说明
            |字段名称|描述|必须|类型|
            |--|--|--|--|
            |page|分页|True|int|
            |Alertor_id   |报警器ID||      |
            |Alertor_online |报警器在线状态|True:1|False:2      |




            #### 响应字段说明
            |字段名称|描述|必须|类型|
            |--|--|--|--|


        '''
    schema = AlertorSchema
    module_perms = ['scene.scene_view']
    def post(self,request,*args,**kwargs):
        try:
            Alertor_id = self.request.query_params.get('Alertor_id')
            Alertor_online = self.request.query_params.get('Alertor_online')
            queryset = Fan.objects.get(id =Alertor_id)
            queryset.fan_online =Alertor_online
            queryset.save()
        except:
            return Response(data={'code':400,'message':'修改失败'},status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'code':200,'message':'修改成功'},status=status.HTTP_200_OK)



