
from pydantic import BaseModel
import datetime
from api.baseSchemas import BaseSchema


class GroupRole(BaseModel):
    group_id:int
    role_id:int
    class Config:
        orm_mode = True

class GroupRoleDetails(GroupRole):
    id:int
    class Config:
        orm_mode = True
class Group(BaseModel):
    title:str
    description:str
    class Config:
        orm_mode = True
class GroupListForUser(BaseModel):
    id:int
    title:str
    description:str
    class Config:
        orm_mode = True
        
class GroupDetails(Group):
    id:int
    group_roles:list[GroupRoleDetails]
    class Config:
        orm_mode = True

class GroupList(BaseModel):
    data:list[GroupDetails] = []
    total_records:int = 0
    
