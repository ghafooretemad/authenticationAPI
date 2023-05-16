from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship
import datetime
from api.database import Base
from api.baseModel import BaseModel


class User(Base, BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    last_login = Column(String, default= None, nullable=True )
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    profile = relationship("Profile", back_populates="user")
    preference = Column(String, default=None, nullable=True)
    avatar = Column(String, default=None, nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    department = relationship("Department", back_populates="users")
    group = relationship("UserGroup", back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=True)
    dob = Column(Date, nullable=False)
    user = relationship("User", back_populates="profile")
    

class Permission(Base, BaseModel):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

class Role(Base, BaseModel):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    role_permission = relationship("RolePermission", back_populates="roles") 
class RolePermission(Base):
    __tablename__ = "role_permissions"
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    roles = relationship("Role", back_populates="role_permission")
    permissions = relationship("Permission")
    permission_id = Column(Integer, ForeignKey("permissions.id"))
class Group(Base, BaseModel):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_group = relationship("UserGroup", back_populates="group")
   
class GroupRole(Base, BaseModel):
    __tablename__ = "group_roles"
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))



class UserGroup(Base):
    __tablename__ = "user_groups"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))

    group = relationship("Group", back_populates="user_group")
    user = relationship("User", back_populates="group")

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    users = relationship("User", back_populates="department")

