from rest_framework import serializers, validators
from .models import *
from alarm.models import Alarm_Management

class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = "__all__"


class SceneCreateSerializer(serializers.ModelSerializer):
    scene_addtime =serializers.HiddenField(
        default=datetime.now()
    )
    scene_status = serializers.HiddenField(
        default=1
    )
    class Meta:
        model = Scene
        fields = "__all__"

class SceneUpdateSerializer(serializers.ModelSerializer):
    scene_addtime =serializers.HiddenField(
        default=datetime.now()
    )
    scene_status = serializers.HiddenField(
        default=1
    )
    class Meta:
        model = Scene
        fields = "__all__"


class HumiditySerializer(serializers.ModelSerializer):

    class Meta:
        model = Humidity
        fields = "__all__"
class Co2Serializer(serializers.ModelSerializer):

    class Meta:
        model = Co2
        fields = "__all__"



class TemperatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Temperature
        fields = "__all__"
class BeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Beam
        fields = "__all__"
class PM25Serializer(serializers.ModelSerializer):

    class Meta:
        model = PM25
        fields = "__all__"
class SmokeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Smoke
        fields = "__all__"

class FlameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flame
        fields = "__all__"

class MethaneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Methane
        fields = "__all__"
class AlarmLampSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlarmLamp
        fields = "__all__"
class AlertorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alertor
        fields = "__all__"
class DisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Display
        fields = "__all__"
class LightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Light
        fields = "__all__"
class PumpSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pump
        fields = "__all__"
class FanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fan
        fields = "__all__"
class UnlockingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unlocking
        fields = "__all__"
class InvadeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invade
        fields = "__all__"


class SceneFireAlarmSerializers(serializers.ModelSerializer):
    sum_time = serializers.SerializerMethodField(source='get_sum_time', read_only=True)

    class Meta:
        model = Alarm_Management
        fields = ('sum_time', 'am_device', 'am_contene')

    def get_sum_time(self, obj):
        return obj.sum_time
class DisplaySerializers1(serializers.ModelSerializer):
    Display_insert_time = serializers.HiddenField(
        default=datetime.now()
    )
    class Meta:
        model = Display
        fields = '__all__'
        extra_kwargs = {
            'display_stutas': {'required': False, 'read_only': True},
            'display_online': {'required': False, 'read_only': True},
        }

