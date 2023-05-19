from pydantic import BaseModel
import datetime
from api.baseSchemas import BaseSchema
    
    
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
class User(BaseSchema):
    email: str
    is_active: bool
    

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

class UserList(BaseModel):
    data:list[UserDetails] = []
    total_records:int = 0
        

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
    