from rest_framework import serializers, validators
from .models import *


class LogSerializers(serializers.ModelSerializer):
    user_id = serializers.HiddenField(
        default= serializers.CurrentUserDefault
    )
    class Meta:
        model = Log
        fields = "__all__"

    extra_kwargs = {
        'log_addtime': {'required': False, 'read_only': True},
        'user_id': {'required': False, 'read_only': True},
    }
