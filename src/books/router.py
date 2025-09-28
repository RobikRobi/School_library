from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from src.models.model import Author, Book
from src.books.shema import CreateBook
from src.db import get_session

app = APIRouter(prefix="/books", tags=["Books"])

# Добавление книги
@app.post("/")
async def add_books(book_data:CreateBook, session:AsyncSession = Depends(get_session)):
 # проверка существует ли автор в базе данных
    ThisBookIs = await session.scalar(select(Book).where(Book.titel == book_data.titel))

    if ThisBookIs:
        raise HTTPException(status_code=411, detail={
        "status":411,
        "details":"This book is"
        })
    new_book = Book(titel=book_data.titel)
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    
    return {
        "id": new_book.id,
        "title": new_book.titel
    }

