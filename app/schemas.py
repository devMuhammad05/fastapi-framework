from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: str
    content: Optional[str]
    published: Optional[bool] = True