from api.database import SessionLocal
from fastapi import Header, HTTPException
from typing import Annotated

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
        