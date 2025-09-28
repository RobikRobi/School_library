from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.db import Base

class Author(Base):
    __tablename__ = "author_table"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str]

    # связь
    books: Mapped[list["Book"]] = relationship(secondary="author_book", back_populates="authors", uselist=True)


class Book(Base):
    __tablename__ = "book_table"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titel: Mapped[str]
    
    # связь
    authors: Mapped[list["Author"]] = relationship(secondary="author_book", back_populates="books", uselist=True)

class AuthorBook(Base):
    __tablename__ = "author_book"

    user_id: Mapped[int] = mapped_column(ForeignKey("author_table.id"),primary_key=True)
    book_id:Mapped[int] = mapped_column(ForeignKey("book_table.id"),primary_key=True)