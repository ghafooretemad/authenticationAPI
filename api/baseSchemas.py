from pydantic import BaseModel 
import datetime

class BaseSchema(BaseModel):
    deleted: bool = False
    deleted_at: datetime.datetime | None = None
    deleted_by: int | None = None
    created_at: datetime.datetime|None = None
    created_by: int|None=None
    updated_at: datetime.datetime|None=None
    updated_by: int|None=None