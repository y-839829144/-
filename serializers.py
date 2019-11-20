from rest_framework import serializers, validators
from .models import *


class VideoSerializers(serializers.ModelSerializer):
    video_addtime = serializers.HiddenField(
        default=datetime.now()
    )

    class Meta:
        model = Video
        fields = "__all__"
        extra_kwargs = {  # 对模型已有参数重新设置和编辑
            'video_addtime': {'required': False, 'read_only': True}  # 可以不填   read_only 不显示该字段
        }