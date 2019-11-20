from django_filters import rest_framework
from .models import Door_approval


# 自定义过滤器
class AccessFilter(rest_framework.FilterSet):
    stime = rest_framework.DateTimeFilter(field_name='door_addtime',lookup_expr='gte')
    etime = rest_framework.DateTimeFilter(field_name='door_addtime',lookup_expr='lte')
    time_min = rest_framework.DateTimeFilter(field_name='door_audittime',lookup_expr='gte')
    time_max = rest_framework.DateTimeFilter(field_name='door_audittime',lookup_expr='lte')
    status = rest_framework.NumberFilter(field_name='door_status')

    class Meta:
        model = Door_approval
        fields = ['stime','etime','time_min','time_max','status']