from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship
import datetime
from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, max_length=200)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    last_login = Column(String, default= None, nullable=True )
    deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=True )
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    created_by = relationship("User", back_populates="id")
    profile = relationship("Profile", back_populates="user")
    preference = Column(String, default=None, nullable=True)
    avatar = Column(String, default=None, nullable=True)
    department = relationship("Department", nullable=True, back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False, max_length=100)
    last_name = Column(String, nullable=False, max_length=100)
    phone = Column(Integer, nullable=False, max_length=14)
    address = Column(String, nullable=True, max_length=255)
    dob = Column(Date, nullable=False)
    

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, max_length=100)
    description = Column(String, nullable=True, max_length=300)

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, max_length=100)
    description = Column(String, nullable=True, max_length=300)
    group_permission = relationship("GroupPermission", back_populates="group")
    
class GroupPermission(Base):
    __tablename__ = "group_permissions"
    id = Column(Integer, primary_key=True, index=True)
    group = relationship("Group")
    permissions = relationship("Permission")

class UserGroup(Base):
    __tablename__ = "user_groups"
    id = Column(Integer, primary_key=True, index=True)
    group = relationship("Group")
    user = relationship("User")
