
from pydantic import BaseModel
from api.baseSchemas import BaseSchema

class Role(BaseModel):
    title:str
    description:str
    class Config:
        orm_mode = True

class RoleDetails(Role, BaseSchema):
    id:int
    class Config:
        orm_mode = True

class RoleList(BaseModel):
    data:list[RoleDetails] = []
    total_records:int = 0