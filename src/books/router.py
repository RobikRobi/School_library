from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from src.models.model import Author, Book
from src.authors.shema import AuthorShema
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

# Получение всех книг
@app.get("/")
async def get_books(session:AsyncSession = Depends(get_session)):
    books = await session.scalars(select(Book))
    return books.all()


# Получение всех книг с авторами
@app.get("/books_authors", response_model=list[AuthorShema])
async def get_books(session:AsyncSession = Depends(get_session)):
    books = await session.scalar(select(Book).options(
        selectinload(Book.authors)
    ))
    return books.all()


# # Получение автора по id
# @app.get("/{author_id}", response_model=ThisAuthor)
# async def get_author_id(author_id: int, session: AsyncSession = Depends(get_session)):
#     author = await session.scalar(select(Author).where(Author.id == author_id))

#     if not author:
#         raise HTTPException(status_code=404, detail="Author not found")

#     return author