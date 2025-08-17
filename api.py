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