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



RoleCreateSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "role",
                required=True,
                location="form",  # from,query,url
                schema=coreschema.Object(),
                # schema=coreschema.String(),
                description="角色",
            ),
])

PermissionUpdateSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "permission",
                required=True,
                location="form",  # from,query,url
                schema=coreschema.Object(),
                # schema=coreschema.String(),
                description="权限",
            ),
])

UserUpdateSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "user",
                required=True,
                location="form",  # from,query,url
                schema=coreschema.Object(),
                # schema=coreschema.String(),
                description="用户",
            ),
])

RoleDeleteSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "role_id",
                required=True,
                location="query",  # from,query,url
                schema=coreschema.Integer,
                # schema=coreschema.String(),
                description="角色id",
            ),
])