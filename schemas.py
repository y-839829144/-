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


AccessUpdateSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "Door_approval",
                required=True,
                location="form",# form
                schema=coreschema.Object(),
                # schema=coreschema.String(),
                description="申请审核",
            ),

])
CountSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "Count",
                required=True,
                location="form",# form
                schema=coreschema.Object(),
                # schema=coreschema.String(),
                description="各用户申请开门次数占比",
            ),

])
DoorTimeSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "Time",
                required=True,
                location="form",# form
                schema=coreschema.Object(),
                # schema=coreschema.String(),
                description="各用户开门总时间占比",
            ),

])