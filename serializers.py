from rest_framework import serializers, validators
from .models import *
from django.utils import timezone

class AccessSerializer(serializers.ModelSerializer):
    door_status = serializers.HiddenField(
        default=1
    )
    user_id = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    door_audittime = serializers.HiddenField(
        default=datetime.now
    )

    class Meta:
        model = Door_approval
        fields = "__all__"

        extra_kwargs = {
            'door_addtime': {'required': False, 'read_only': True},
            'door_status': {'required': False, 'read_only': True},
            'door_user': {'required': False, 'read_only': True},
            'door_audittime': {'required': False, 'read_only': True},
            'door_feedback': {'required': False, 'read_only': True},
            'user_id': {'required': False, 'read_only': True},

        }

class AccessSerializer1(serializers.ModelSerializer):
    door_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault
    )
    door_audittime=serializers.HiddenField(
        default=datetime.now
    )
    class Meta:
        model  =  Door_approval
        fields =  "__all__"

        extra_kwargs = {
            'user_id': {'required': False, 'read_only': True},
            'door_addtime': {'required': False, 'read_only': True},
            'door_start': {'required': False, 'read_only': True},
            'door_end': {'required': False, 'read_only': True},
            'door_follownum': {'required': False, 'read_only': True},
            'door_detail': {'required': False, 'read_only': True},
            'door_audittime': {'required': False, 'read_only': True},
            'scene_id': {'required': False, 'read_only': True},
            'door_follow': {'required': False, 'read_only': True},




        }
