from rest_framework import serializers, validators
from .models import *


class AlarmListSerializers(serializers.ModelSerializer):

    class Meta:
        model = Alarm_Management
        fields = "__all__"


class AlarmManyListSerializers(serializers.ModelSerializer):

    class Meta:
        model = Alarm_Management
        fields = ('am_type_id','am_level_id','am_contene',)

class AlarmCreateSerializers(serializers.ModelSerializer):

    class Meta:
        model = Alarm_Management
        fields = ('am_type_id','am_level_id','scene_id','am_contene','am_device',)

class AlarmlevelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Alarm_Level
        fields = "__all__"
class AlarmTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Alarm_Type
        fields = "__all__"