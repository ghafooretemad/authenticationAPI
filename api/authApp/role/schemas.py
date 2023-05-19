
from pydantic import BaseModel
from api.baseSchemas import BaseSchema


class RolePermission(BaseModel):
    role_id: int = 0
    permission_id: int

    class Config:
        orm_mode = True

class RolePermissionDetails(RolePermission):
    id: int

    class Config:
        orm_mode = True

class Role(BaseModel):
    title: str
    description: str
    class Config:
        orm_mode = True


class RoleDetails(Role, BaseSchema):
    id: int
    # permission: list[RolePermissionDetails]
    role_permissions:list[RolePermissionDetails]
    class Config:
        orm_mode = True


class RoleList(BaseModel):
    data: list[RoleDetails] = []
    total_records: int = 0
