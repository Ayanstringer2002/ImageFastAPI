from pydantic import BaseModel
from fastapi_users import schemas
import uuid

class PostCreate(BaseModel):
    title: str
    content: str
    
class PostResponse(BaseModel):
    title: str
    content: str
    
class UserRead(schemas.BaseUer[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass
    
    
class userupdate(schemas.BaseUserUpdate):
    pass 
