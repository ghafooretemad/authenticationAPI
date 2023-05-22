
from pydantic import BaseModel
from api.baseSchemas import BaseSchema

class Permission(BaseSchema):
    title:str
    description:str
    class Config:
        orm_mode = True
        
class PermissionDetails(Permission):
    id:int
    class Config:
        orm_mode = True
class PermissionList(BaseModel):
    data:list[PermissionDetails] = []
    total_records:int = 0