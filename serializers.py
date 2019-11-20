from rest_framework import serializers, validators
from .models import *



class UserListSerializers(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('user_name','user_number','user_gender','user_picture','user_status')


class UserCreateSerializers(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"