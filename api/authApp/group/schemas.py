
from pydantic import BaseModel
import datetime
from api.baseSchemas import BaseSchema

class Group(BaseModel):
    title:str
    description:str
    class Config:
        orm_mode = True

class GroupDetails(Group):
    id:int
    class Config:
        orm_mode = True

class GroupList(BaseModel):
    data:list[GroupDetails] = []
    total_records:int = 0