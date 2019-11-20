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


ActiveUpdateSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "User_active",
                required=True,
                location="form",# form
                schema=coreschema.Object(),
                # schema=coreschema.String(),
                description="用户冻结",
            ),

])