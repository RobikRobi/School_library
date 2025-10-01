from pydantic import BaseModel
from typing import List, Optional
from src.books.shema import BookResponse


class CreateAuthor(BaseModel):
    
    name: str
    book_ids: Optional[List[int]] = None


class ThisAuthor(BaseModel):
    
    name: str
    book_ids: Optional[List[int]] = None


class AuthorBookCreate(BaseModel):

    author_name: str
    book_title: str


class AuthorShema(BaseModel):

    name: str

class AuthorResponse(BaseModel):
    id: int
    name: str
    books: List[BookResponse]
    
    class Config:
        from_attributes = True


class AddBookToAuthor(BaseModel):
    author_id: int
    book_title: str