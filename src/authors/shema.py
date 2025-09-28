from pydantic import BaseModel
from typing import List, Optional


class CreateAuthor(BaseModel):
    
    name: str
    book_ids: Optional[List[int]] = None


class ThisAuthor(BaseModel):
    
    name: str
    book_ids: Optional[List[int]] = None


class AuthorBookCreate(BaseModel):
    author_name: str
    book_title: str