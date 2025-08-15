from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

from library.models import Book

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
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def add_book(self, book: Book) -> None:
        if self.find_book(book.isbn):
            raise ValueError("Bu ISBN zaten kayıtlı.")
        self.books.append(book)
        self.save_books()
    
    def remove_book(self, isbn: str) -> bool:
        target = self.find_book(isbn)
        if not target:
            return False
        self.books = [b for b in self.books if b.isbn != isbn]
        self.save_books()
        return True