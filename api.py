# api.py
from __future__ import annotations
from fastapi import FastAPI, Depends
from pydantic import BaseModel

from typing import List

from library.storage import Library
from library.models import Book

app = FastAPI(title="Py202 Library API", version="1.0.0")

@app.get("/")
def root():
    return {
        "message": "Py202 Library API çalışıyor. Dokümantasyon için /docs",
        "endpoints": ["GET /books", "POST /books", "DELETE /books/{isbn}"]
    }

@app.get("/health")
def health():
    return {"status": "ok"}


# ---- Pydantic çıkış modeli ----
class BookOut(BaseModel):
    title: str
    author: str
    isbn: str

# ---- Library dependency ----
def get_library() -> Library:
    return Library("library.json")

# ---- GET /books ----
@app.get("/books", response_model=List[BookOut])
def list_books(lib: Library = Depends(get_library)):
    books = lib.list_books()
    return [BookOut(title=b.title, author=b.author, isbn=b.isbn) for b in books]

# --- Pydantic giriş modeli ---
class ISBNIn(BaseModel):
    isbn: str

# --- POST /books ---
from fastapi import HTTPException

@app.post("/books", response_model=BookOut, status_code=201)
def add_book(payload: ISBNIn, lib: Library = Depends(get_library)):
    try:
        # Stage-2: add_book artık ISBN (str) da kabul ediyor
        lib.add_book(payload.isbn)
        b = lib.find_book(payload.isbn)
        assert b is not None 
        return BookOut(title=b.title, author=b.author, isbn=b.isbn)
    except ValueError as e:
         # Geçersiz ISBN, bulunamadı(404), ağ hatası vb. durumlar ValueError mesajıyla gelir
         raise HTTPException(status_code=400, detail=str(e)) from e