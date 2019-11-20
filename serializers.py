from rest_framework import serializers, validators
from scene.models import Unlocking
from alarm.models import Alarm_Management



class IndexLockserializer(serializers.ModelSerializer):

    class Meta:
        model = Unlocking
        fields = ('user_id','Unlocking_insert_time','Unlocking_online','scene_id')


class IndexAlarmSerializer(serializers.ModelSerializer):


    class Meta:
        model = Alarm_Management
        fields = ('am_device','am_contene','am_level_id','am_status')