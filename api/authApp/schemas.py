from pydantic import BaseModel
import datetime
    
class User(BaseModel):
    email: str
    active: bool
    deleted: bool
    deleted_at: datetime.datetime | None = None
    deleted_by: int | None = None
    created_at: datetime.datetime
    created_by: int
    udpated_at: datetime.datetime|None=None
    udpated_by: int|None=None
    profile: int
    department: int | None = None

class createUser(User):
    hashed_password: str
    
class userDetails(User):
    id: int
    avatar: str | None = None
    preference: str | None = None
    class Config:
        orm_mode = True

class Profile(User):
    hashed_password: str
    first_name:str
    last_name: str 
    phone: int
    address: str | None=None
    dob: datetime.date
    class Config:
        orm_mode = True
    
class Group(BaseModel):
    title:str
    description:str
    class Config:
        orm_mode = True

class GroupDetails(Group):
    id:int
    class Config:
        orm_mode = True

class Permission(BaseModel):
    title:str
    description:str
    class Config:
        orm_mode = True

class PermissionDetails(Permission):
    id:int
    class Config:
        orm_mode = True

class GroupPermission(BaseModel):
    group:int
    permission:int
    class Config:
        orm_mode = True

class GroupPermissionDetails(GroupPermission):
    id:int
    class Config:
        orm_mode = True


class UserGroup(BaseModel):
    group:int
    user:int
    class Config:
        orm_mode = True

class UserGroupDetails(UserGroup):
    id:int
    class Config:
        orm_mode = True
    