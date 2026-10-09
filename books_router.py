from fastapi import APIRouter, HTTPException, Path, status
from typing import List

books_router = APIRouter(prefix="/books", tags=["Библиотечный каталог"])
library_db = []
DEV = "Михаил"

@books_router.post("", status_code=status.HTTP_201_CREATED, response_model=BookResponse)
async def create_book(book: BookCreate):
    for item in library_db:
        if item.id == book.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"[{DEV}] Книга с инвентарным номером {book.id} уже числится в библиотеке."
            )
    library_db.append(book)
    return book

@books_router.get("", response_model=BookListResponse)
async def get_books():
    return BookListResponse(
        total=len(library_db),
        developer=DEV,
        books=library_db
    )


@books_router.get("/{book_id}", response_model=BookResponse)
async def get_book_by_id(book_id: int = Path(..., gt=0)):
    for book in library_db:
        if book.id == book_id:
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"[{DEV}] Книга с ID {book_id} не найдена в библиотечном фонде."
    )

@books_router.put("/{book_id}", response_model=BookResponse)
async def update_book(book_data: BookUpdate, book_id: int = Path(..., gt=0)):
    for book in library_db:
        if book.id == book_id:
            if book_data.title: book.title = book_data.title
            if book_data.author: book.author = book_data.author
            if book_data.year: book.year = book_data.year
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"[{DEV}] Ошибка обновления: книга с ID {book_id} не найдена."
    )

@books_router.delete("/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int = Path(..., gt=0)):
    for index, book in enumerate(library_db):
        if book.id == book_id:
            library_db.pop(index)
            return {"message": f"[{DEV}] Книга #{book_id} успешно списана."}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"[{DEV}] Ошибка списания: книга #{book_id} отсутствует в фонде."
    )