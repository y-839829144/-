import coreapi
import coreschema
from rest_framework.schemas import AutoSchema, ManualSchema
token_field = coreapi.Field(
                name="Authorization",
                required=False,
                location="header",
                schema=coreschema.String(),
                description="格式：JWT 值",
        )
TokenSchema = AutoSchema([
                token_field
        ]
)
SceneListSchema = AutoSchema([
    # token_field,
coreapi.Field(
                "scene_id",
                required=False,
                location="query",# form
                schema=coreschema.Integer(),
                # schema=coreschema.String(),
                description="场景ID",
            ),
])

SceneUpdateSchema = AutoSchema([
    # token_field,
coreapi.Field(
                "scene_id",
                required=True,
                location="query",# form
                schema=coreschema.Integer(),
                # schema=coreschema.String(),
                description="场景ID",
            ),
    coreapi.Field(
                "scene",
                required=True,
                location="form",# form
                schema=coreschema.Object(),
                # schema=coreschema.String(),
                description="场景修改内容",
            ),

])
SceneDeleteSchema = AutoSchema([
    # token_field,
coreapi.Field(
                "scene_id",
                required=True,
                location="query",# form
                schema=coreschema.Integer(),
                # schema=coreschema.String(),
                description="场景ID",
            ),
])
FireCountSchema = AutoSchema([
    # token_field,
coreapi.Field(
                "data",
                required=True,
                location="form",# form
                schema=coreschema.Integer(),
                # schema=coreschema.String(),
                description="消防设备统计",
            ),
])
SceneFireHistorySchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "start_time",
                required=False,
                location="query",  # from,query,url
                schema=coreschema.Integer,
                # schema=coreschema.String(),
                description="开始时间",
            ),
    coreapi.Field(
                "end_time",
                required=False,
                location="query",  # from,query,url
                schema=coreschema.Integer,
                # schema=coreschema.String(),
                description="结束时间",
            ),
    coreapi.Field(
                "scene_id",
                required=True,
                location="query",  # from,query,url
                schema=coreschema.Integer,
                # schema=coreschema.String(),
                description="场景id",
            ),
])
LightSchema = AutoSchema([
    # token_field,
coreapi.Field(
                "light_id",
                required=True,
                location="query",# form
                schema=coreschema.Integer(),
                # schema=coreschema.String(),
                description="灯光传感器ID",
            ),
coreapi.Field(
                "light_online",
                required=True,
                location="query",# form
                schema=coreschema.Integer(),
                # schema=coreschema.String(),
                description="灯光传感器在线状态",
            ),
])

PumpSchema = AutoSchema([
    # token_field,
coreapi.Field(
                "pump_id",
                required=True,
                location="query",# form
                schema=coreschema.Integer(),
                # schema=coreschema.String(),
                description="水泵传感器ID",
            ),
coreapi.Field(
                "pump_online",
                required=True,
                location="query",# form
                schema=coreschema.Integer(),
                # schema=coreschema.String(),
                description="水泵传感器在线状态",
            ),
])

FanSchema = AutoSchema([
    # token_field,
coreapi.Field(
                "fan_id",
                required=True,
                location="query",# form
                schema=coreschema.Integer(),
                # schema=coreschema.String(),
                description="风扇传感器ID",
            ),
coreapi.Field(
                "fan_online",
                required=True,
                location="query",# form
                schema=coreschema.Integer(),
                # schema=coreschema.String(),
                description="风扇传感器在线状态",
            ),
])

AlertorSchema = AutoSchema([
    # token_field,
coreapi.Field(
                "Alertor_id",
                required=True,
                location="query",# form
                schema=coreschema.Integer(),
                # schema=coreschema.String(),
                description="报警器ID",
            ),
coreapi.Field(
                "Alertor_online",
                required=True,
                location="query",# form
                schema=coreschema.Integer(),
                # schema=coreschema.String(),
                description="报警器在线状态",
            ),
])
SceneEnvironmentHistorySchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "start_time",
                required=False,
                location="query",  # from,query,url
                schema=coreschema.String,
                # schema=coreschema.String(),
                description="开始时间",
            ),
    coreapi.Field(
                "end_time",
                required=False,
                location="query",  # from,query,url
                schema=coreschema.String,
                # schema=coreschema.String(),
                description="结束时间",
            ),
    coreapi.Field(
                "scene_id",
                required=True,
                location="query",  # from,query,url
                schema=coreschema.Integer,
                # schema=coreschema.String(),
                description="场景id",
            ),
    coreapi.Field(
                "scene_env_device",
                required=True,
                location="query",  # from,query,url
                schema=coreschema.String,
                # schema=coreschema.String(),
                description="环境设备名称",
            ),
])
SceneEnvironmentAlarmSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "start_time",
                required=False,
                location="query",  # from,query,url
                schema=coreschema.Integer,
                # schema=coreschema.String(),
                description="开始时间",
            ),
    coreapi.Field(
                "end_time",
                required=False,
                location="query",  # from,query,url
                schema=coreschema.Integer,
                # schema=coreschema.String(),
                description="结束时间",
            ),
    coreapi.Field(
                "scene_id",
                required=True,
                location="query",  # from,query,url
                schema=coreschema.Integer,
                # schema=coreschema.String(),
                description="场景id",
            ),
    coreapi.Field(
                "scene_env_device",
                required=True,
                location="query",  # from,query,url
                schema=coreschema.String,
                # schema=coreschema.String(),
                description="环境设备名称",
            ),
])
DisplayCreateSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "scene_id",
                required=True,
                location="form",  # from,query,url
                schema=coreschema.Integer,
                # schema=coreschema.String(),
                description="场景id",
            ),
    coreapi.Field(
                "display_context",
                required=True,
                location="form",  # from,query,url
                schema=coreschema.String,
                # schema=coreschema.String(),
                description="显示屏显示内容",
            ),
])