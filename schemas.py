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

IndexAlarmSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "scene_id",
                required=True,
                location="query",# form
                schema=coreschema.Integer(),
                # schema=coreschema.String(),
                description="场景id",
            ),



])