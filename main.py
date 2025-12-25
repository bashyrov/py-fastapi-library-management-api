from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


@app.get("/authors/")
def read_authors_list(db: Session = Depends(get_db),
                      skip: int = 0,
                      limit: int = 0
                      ) -> list[schemas.AuthorRead]:
    return crud.get_authors_list(
        db=db,
        skip=skip,
        limit=limit
    )


@app.post("/authors/", response_model=schemas.AuthorRead)
def create_author(author: schemas.AuthorCreate,
                  db: Session = Depends(get_db)
                  ):
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def retrieve_author(author_id: int,
                    db: Session = Depends(get_db)
                    ):
    return crud.get_author_by_id(
        db=db,
        author_id=author_id
    )


@app.get("/books/")
def read_books_list(db: Session = Depends(get_db),
                    author_id: int | None = None,
                    skip: int = 0, limit: int = 0
                    ) -> list[schemas.BookRead]:
    return crud.get_books_list(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit
    )


@app.post("/books/", response_model=schemas.BookRead)
def create_book(book: schemas.BookCreate,
                db: Session = Depends(get_db)
                ):
    return crud.create_book(
        db=db,
        book=book
    )


@app.get("/books/{books_id}", response_model=schemas.BookRead)
def retrieve_book(book_id: int,
                  db: Session = Depends(get_db)
                  ):
    return crud.get_book_by_id(
        db=db,
        book_id=book_id
    )
