from pydantic import BaseModel
import datetime
    
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class Department(BaseModel):
    id:int
    name:str
    
    class Config:
        orm_mode = True
class Profile(BaseModel):
    first_name:str
    last_name: str 
    phone: int
    address: str | None=None
    dob: datetime.date
    class Config:
        orm_mode = True
class User(BaseModel):
    email: str
    is_active: bool
    deleted: bool = False
    deleted_at: datetime.datetime | None = None
    deleted_by: int | None = None
    created_at: datetime.datetime
    created_by: int|None=None
    updated_at: datetime.datetime|None=None
    updated_by: int|None=None

class CreateUser(User):
    hashed_password: str
    
class UserDetails(User):
    id: int
    avatar: str | None = None
    preference: str | None = None
    profile: Profile|None=None
    department: Department | None = None
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

class Role(BaseModel):
    title:str
    description:str
    class Config:
        orm_mode = True

class RoleDetails(Role):
    id:int
    class Config:
        orm_mode = True
        
class RolePermission(BaseModel):
    role:int
    permission:int
    class Config:
        orm_mode = True

class RolePermissionDetails(RolePermission):
    id:int
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
class GroupRole(BaseModel):
    group:int
    role:int
    class Config:
        orm_mode = True

class GroupRoleDetails(GroupRole):
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
    