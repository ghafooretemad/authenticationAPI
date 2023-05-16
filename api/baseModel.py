

from sqlalchemy import Boolean, Column, ForeignKey, Integer, DateTime
import datetime
        
class BaseModel:
    deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, default=None, nullable=True )
    deleted_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)