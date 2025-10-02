from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from src.models.model import Author, Book
from src.authors.shema import CreateAuthor, AuthorBookCreate, ThisAuthor, AddBookToAuthor, UpdateAuthor
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

# Получение всех авторов c книгами
@app.get("/")
async def get_authors(session:AsyncSession = Depends(get_session)):
    stmt = select(Author).options(selectinload(Author.books))
    result = await session.execute(stmt)
    authors = result.scalars().all() 
    
    return authors


# Добавление книги к существующему автору
@app.post("/add-book-to-author")
async def add_book_to_author(data: AddBookToAuthor, session: AsyncSession = Depends(get_session)):
    # ищем автора
    author = await session.scalar(
        select(Author).options(selectinload(Author.books)).where(Author.id == data.author_id)
    )
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    # проверяем, есть ли уже такая книга
    book = await session.scalar(select(Book).where(Book.titel == data.book_title))
    if not book:
        book = Book(titel=data.book_title)
        session.add(book)
        await session.flush()  # чтобы получить id книги до commit

    # проверка на дубликат связи
    if book in author.books:
        raise HTTPException(status_code=400, detail="This book is already linked to the author")

    # связываем
    author.books.append(book)

    await session.commit()
    await session.refresh(author)

    return {
        "author": {
            "id": author.id,
            "name": author.name
        },
        "book": {
            "id": book.id,
            "title": book.titel
        }
    }

# Получение автора по id
@app.get("/{author_id}", response_model=ThisAuthor)
async def get_author_id(author_id: int, session: AsyncSession = Depends(get_session)):
    author = await session.scalar(select(Author).where(Author.id == author_id))

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


# Изменения данных автора
@app.put("/update/{author_id}")
async def update_author(author_id: int, data: UpdateAuthor, session: AsyncSession = Depends(get_session)):
    # Находим автора по id
    author = await session.scalar(select(Author).where(Author.id == author_id))
    
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    # Обновляем только имя
    if data.name is not None:
        author.name = data.name
    
    await session.commit()
    await session.refresh(author)
    
    return {
        "id": author.id,
        "name": author.name,
        "message": "Author updated successfully"
    }



# Удаление автора по id
@app.delete("/{author_id}")
async def delete_author(author_id: int, session: AsyncSession = Depends(get_session)):
    # Находим автора по id вместе с его книгами
    author = await session.scalar(
        select(Author)
        .options(selectinload(Author.books))
        .where(Author.id == author_id)
    )
    
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    # Сохраняем информацию об авторе для ответа
    author_info = {
        "id": author.id,
        "name": author.name,
        "books_count": len(author.books)
    }
    
    # Удаляем автора
    await session.delete(author)
    await session.commit()
    
    return {
        "message": "Author deleted successfully",
        "deleted_author": author_info
    }