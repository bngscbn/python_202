# api.py
from __future__ import annotations
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from typing import List
from library.storage import Library
from library.models import Book
from library.validators import validate_isbn, normalize_isbn

app = FastAPI(title="Py202 Library API", version="1.0.0")

@app.get("/")
def root():
    return {
        "message": "Py202 Library API çalışıyor. Dokümantasyon için /docs",
        "endpoints": ["GET /books", "POST /books", "DELETE /books/{isbn}", "PUT /books/{isbn}"]
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

@app.delete("/books/{isbn}", response_model=BookOut)
def delete_book(isbn: str, lib: Library = Depends(get_library)):
    # Sadece normalize et (tire/boşlukları kaldır) — checksum doğrulaması yapma
    norm = normalize_isbn(isbn)

    # Önce normalize edilmiş hâliyle ara; bulunmazsa ham değeri de dene (eski kayıtlar için)
    b = lib.find_book(norm) or lib.find_book(isbn)
    if not b:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı")

    # Bulunan kayda göre doğru anahtarla sil
    key = b.isbn
    lib.remove_book(key)
    return BookOut(title=b.title, author=b.author, isbn=b.isbn)

# Güncelleme isteği gövdesi: title/author opsiyonel
class BookUpdateIn(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None

@app.put("/books/{isbn}", response_model=BookOut)
def update_book(isbn: str, payload: BookUpdateIn, lib: Library = Depends(get_library)):
    """
    Belirtilen ISBN'li kitabın title/author alanlarını günceller.
    - ISBN path param'da sabittir; değiştirilemez.
    - En az bir alan (title/author) gelmelidir; aksi halde 400 döneriz.
    - Kitap yoksa 404 döneriz.
    """
    # 1) En az bir alan kontrolü
    if payload.title is None and payload.author is None:
        raise HTTPException(status_code=400, detail="En az bir alan (title/author) güncellemelisiniz.")

    # 2) Var mı yok mu Kontrolü (normalize ederek ara)
    key = normalize_isbn(isbn)
    found = lib.find_book(key)
    if not found:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı.")
    
    # 3) Güncelle ve sonucu döndür
    try:
        updated = lib.update_book(key, title=payload.title, author=payload.author)
        return BookOut(title=updated.title, author=updated.author, isbn=updated.isbn)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e