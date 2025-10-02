from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from src.models.model import Book
from src.books.shema import CreateBook, UpdateBook
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
        "titel": new_book.titel
    }


# Получение всех книг с авторами
@app.get("/books_authors")
async def get_books(session:AsyncSession = Depends(get_session)):
    stmt = select(Book).options(selectinload(Book.authors))
    result = await session.execute(stmt)
    books = result.scalars().all()

    return books


# Изменение книги
@app.put("/update/{book_id}")
async def update_author(book_id: int, data: UpdateBook, session: AsyncSession = Depends(get_session)):
    # Находим автора по id
    book = await session.scalar(select(Book).where(Book.id == book_id))
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Обновляем только имя
    if data.titel is not None:
        book.titel = data.titel
    
    await session.commit()
    await session.refresh(book)
    
    return {
        "id": book.id,
        "titel": book.titel,
        "message": "Book updated successfully"
    }


# Удаление книги по id
@app.delete("/{book_id}")
async def delete_author(book_id: int, session: AsyncSession = Depends(get_session)):
    # Находим книгу по id вместе с его аторами
    book = await session.scalar(
        select(Book)
        .options(selectinload(Book.authors))
        .where(Book.id == book_id)
    )
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Сохраняем информацию о книге
    book_info = {
        "id": book.id,
        "titel": book.titel,
        "books_count": len(book.authors)
    }
    
    # Удаляем книгу
    await session.delete(book)
    await session.commit()
    
    return {
        "message": "Book deleted successfully",
        "deleted_book": book_info
    }