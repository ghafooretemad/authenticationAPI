from pydantic import BaseModel
import datetime
from api.baseSchemas import BaseSchema


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class Department(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Profile(BaseModel):
    first_name: str
    last_name: str
    phone: int
    address: str | None = None
    dob: datetime.date

    class Config:
        orm_mode = True


class User(BaseModel):
    email: str
    is_active: bool
    department_id: int | None = None
    preference: str | None = None


class UserCreate(User):
    hashed_password: str

class UserGroup(BaseModel):
    group_id: int

    class Config:
        orm_mode = True

class UserDetails(User, BaseSchema):
    id: int
    avatar: str | None = None
    profile: Profile | None = None
    department: Department | None = None
    group: list[UserGroup]|None = None
    class Config:
        orm_mode = True


class UserList(BaseModel):
    data: list[UserDetails] = []
    total_records: int = 0




class UserGroupDetails(UserGroup):
    id: int
    user_id: int

    class Config:
        orm_mode = True
    
class UserGroupList(BaseModel):
    id:int
    title:str
    description:str
    
    class Config:
        orm_mode = True
        

class UserPermission(BaseModel):
    id: int
    title:str
    description:str
    class Config:
        orm_mode = True