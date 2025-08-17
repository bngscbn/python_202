from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional, Union
from fastapi import HTTPException, Depends
from library.models import Book

from library import external

from library.validators import validate_isbn, normalize_isbn

class Library:
    def __init__(self, storage_path: str = "library.json") -> None:
        self.storage = Path(storage_path)
        self.books: List[Book] = []
        self.load_books()
    
    def load_books(self) -> None:
        if self.storage.exists():
            try:
                data = json.loads(self.storage.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                data = []
            
        else:
            data = []
            # dosya yoksa boş listeyle oluştur
            self.storage.write_text("[]", encoding="utf-8")
        
        self.books = [Book.from_dict(item) for item in data]

    def save_books(self) -> None:
        payload = [b.to_dict() for b in self.books]
        self.storage.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def list_books(self) -> List[Book]:
        return list(self.books)
    
    def find_book(self, isbn: str) -> Optional[Book]:
        target = normalize_isbn(isbn)
        for b in self.books:
            if normalize_isbn(b.isbn) == target:
                return b
        return None

    def add_book(self, book: Union[Book, str]) -> None:
        if isinstance(book, Book):
            if self.find_book(book.isbn):
                raise ValueError("Bu ISBN zaten kayıtlı.")
            self.books.append(book)
            self.save_books()
        elif isinstance(book, str):
            isbn = validate_isbn(book)
            if self.find_book(isbn):
                raise ValueError("Bu ISBN zaten kayıtlı.")
            try:
                title, author = external.fetch_book_by_isbn(isbn)
            except external.OpenLibraryError as e:
                raise ValueError(str(e)) from e
            self.books.append(Book(title=title, author=author, isbn=isbn))
            self.save_books()
        else:
            raise TypeError("add_book expects a Book instance or an ISBN string.")
    
    def remove_book(self, isbn: str) -> bool:
        target = normalize_isbn(isbn)
        before = len(self.books)
        self.books = [b for b in self.books if normalize_isbn(b.isbn) != target]
        if len(self.books) < before:
            self.save_books()
            return True
        return False

    def add_book_by_isbn(self, raw_isbn: str) -> None:
        isbn = validate_isbn(raw_isbn)  # önce doğrula + normalize et
        if self.find_book(isbn):
            raise ValueError("Bu ISBN zaten kayıtlı.")
        try:
            title, author = external.fetch_book_by_isbn(isbn)
        except external.OpenLibraryError as e:
            raise ValueError(str(e)) from e
        self.add_book(Book(title=title, author=author, isbn=isbn))
    
    def update_book(self, isbn: str, title: Optional[str] = None, author: Optional[str] = None):

        # 1) Boş payload kontrolü
        if title is None and author is None:
            raise ValueError("Güncelleme için en az bir alan (title/author) göndermelisin.")
        
        # 2) Hedefi normalize ederek bul (tire/boşluk farkları önemli olmasın)
        target = normalize_isbn(isbn)
        book = self.find_book(target)
        if book is None:
            raise ValueError("Kitap bulunamadı.")

        # 3) Değerleri kırp ve uygula
        if isinstance(title, str):
            title = title.strip()
            if title:
                book.title = title
        if isinstance(author, str):
            author = author.strip()
            if author:
                book.author = author
        
        # 4) Diske yaz ve güncellenmiş nesneyi döndür
        self.save_books()
        return book
        
        