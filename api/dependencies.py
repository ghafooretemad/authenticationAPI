from sqlalchemy.orm import Session
from .database import SessionLocal
from pydantic import BaseModel
class CommonQueryParams:
    def __init__(self, skip: int = 0, limit: int = 100):
        self.skip = skip
        self.limit = limit
        
class FilterTemplate:
    def __init__(self, key, value):
        self.key = key
        self.value = value     
# DB Coonection Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
class UserFilterDependency:
    def __init__(self, name:str='', email:str='', phone:str='', department:int = 0):
        self.name = name
        self.email = email
        self.phone = phone
        self.department = department