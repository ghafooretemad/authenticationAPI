from sqlalchemy.orm import Session
from .database import SessionLocal
class CommonQueryParams:
    def __init__(self, skip: int = 0, limit: int = 100):
        self.skip = skip
        self.limit = limit
        
     
# DB Coonection Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()