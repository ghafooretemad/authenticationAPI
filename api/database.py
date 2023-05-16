from sqlalchemy import create_engine,  Boolean, Column, ForeignKey, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime


SQLALCHEMY_DATABASE_URL = "postgresql://authUser:admin@localhost:5432/auth_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class BaseModel:
    deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=True )
    deleted_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
