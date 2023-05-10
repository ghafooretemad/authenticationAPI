from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship
import datetime
from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    last_login = Column(String, default= None, nullable=True )
    deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=True )
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    created_by = relationship("User")
    profile = relationship("Profile", back_populates="user")
    preference = Column(String, default=None, nullable=True)
    avatar = Column(String, default=None, nullable=True)
    department = relationship("Department", back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(Integer, nullable=False)
    address = Column(String, nullable=True)
    dob = Column(Date, nullable=False)
    

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    group_role = relationship("GroupRole", back_populates="group")
   
class GroupRole(Base):
    __tablename__ = "group_role"
    id = Column(Integer, primary_key=True, index=True)
    role = relationship("Role")
    group = relationship("Group")
class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    role_permission = relationship("RolePermission", back_populates="group") 
class RolePermission(Base):
    __tablename__ = "role_permissions"
    id = Column(Integer, primary_key=True, index=True)
    role = relationship("Role", back_populates="role_permission")
    permissions = relationship("Permission")

class UserGroup(Base):
    __tablename__ = "user_groups"
    id = Column(Integer, primary_key=True, index=True)
    group = relationship("Group")
    user = relationship("User")
