from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from src.models.model import Author, Book
from src.authors.shema import CreateAuthor, AuthorBookCreate, ThisAuthor
from src.db import get_session

app = APIRouter(prefix="/authors", tags=["Authors"])

# Добавление автора и книги
@app.post("/add-author-book")
async def add_author_and_book(data: AuthorBookCreate, session: AsyncSession = Depends(get_session)):
    # создаём автора
    new_author = Author(name=data.author_name)
    # создаём книгу
    new_book = Book(title=data.book_title)

    # связываем Many-to-Many
    new_author.books.append(new_book)

    session.add(new_author)
    session.add(new_book)

    await session.commit()
    await session.refresh(new_author)
    await session.refresh(new_book)

    return {
        "author": {
            "id": new_author.id,
            "name": new_author.name
        },
        "book": {
            "id": new_book.id,
            "title": new_book.title
        }
    }


# Добавление автора
@app.post("/")
async def add_authors(author_data:CreateAuthor, session:AsyncSession = Depends(get_session)):
    # проверка существует ли автор в базе данных
    isAuthorEx = await session.scalar(select(Author).where(Author.name == author_data.name))

    if isAuthorEx:
        raise HTTPException(status_code=411, detail={
        "status":411,
        "details":"author is exists"
        })
    new_author = Author(name=author_data.name)
    session.add(new_author)
    await session.commit()
    await session.refresh(new_author)
    
    return {
        "id": new_author.id,
        "name": new_author.name,
    }

# Получение всех авторов
@app.get("/")
async def get_authors(session:AsyncSession = Depends(get_session)):
    profiles = await session.scalars(select(Author))
    return profiles.all()

# Получение автора по id
@app.get("/{author_id}", response_model=ThisAuthor)
async def get_author_id(author_id: int, session: AsyncSession = Depends(get_session)):
    author = await session.scalar(select(Author).where(Author.id == author_id))

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author