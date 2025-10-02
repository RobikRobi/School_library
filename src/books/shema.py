from pydantic import BaseModel
from typing import List, Optional


class CreateBook(BaseModel):
    
    titel: str
    author_ids: Optional[List[int]] = None


class BookResponse(BaseModel):

    id: int
    titel: str
    
    class Config:
        from_attributes = True


class UpdateBook(BaseModel):

    titel: str | None = None
    authors_ids: List[int] | None = None