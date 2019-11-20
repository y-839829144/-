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

AlarmManySchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "Type_id_id",
                required=True,
                location="query",# form
                schema=coreschema.Integer(),
                # schema=coreschema.String(),
                description="类型id",
            ),



])
AlarmManySchema1 = AutoSchema([
    # token_field,
coreapi.Field(
                "am_id",
                required=True,
                location="query",# form
                schema=coreschema.Anything,
                # schema=coreschema.String(),
                description="处理id",
            ),
coreapi.Field(
                "am_deal_detail",
                required=True,
                location="query",# form
                schema=coreschema.String(),
                # schema=coreschema.String(),
                description="处理内容",
            ),


])

AlarmApplicationSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "alarm_id",
                required=True,
                location="query",# form
                schema=coreschema.Integer(),
                # schema=coreschema.String(),
                description="告警id",
            ),
coreapi.Field(
                "alarm_dealtail",
                required=True,
                location="query",# form
                schema=coreschema.String(),
                # schema=coreschema.String(),
                description="告警处理说明",
            ),



])

AlarmAuditSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "alarm_id",
                required=True,
                location="query",# form
                schema=coreschema.Integer(),
                # schema=coreschema.String(),
                description="告警ID",
            ),
coreapi.Field(
                "am_audit_detail",
                required=True,
                location="query",# form
                schema=coreschema.String(),
                # schema=coreschema.String(),
                description="审批说明",
            ),



])

AlarmTypeCountSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "input_time",
                required=True,
                location="form",# form
                schema=coreschema.Object(),
                # schema=coreschema.String(),
                description="类型统计占比",
            ),



])

SafeCountSchema = AutoSchema([
    # token_field,
coreapi.Field(
                "type_id",
                required=True,
                location="query",# form
                schema=coreschema.Integer(),
                # schema=coreschema.String(),
                description="安防类型ID",
            ),
    coreapi.Field(
                "input_time",
                required=True,
                location="form",# form
                schema=coreschema.Object(),
                # schema=coreschema.String(),
                description="安防监测告警各状态数量占比",
            ),



])
AlarmTypePrecentSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "alarm_time",
                required=True,
                location="form",  # from,query,url
                schema=coreschema.Object(),
                # schema=coreschema.String(),
                description="告警时间段",
            ),
])