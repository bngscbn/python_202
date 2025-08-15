from dataclasses import dataclass

@dataclass
class Book:
    title: str
    author: str
    isbn: str

    def __str__(self) -> str:
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

    
    def to_dict(self) -> dict:
        # Diskte JSON saklarken sözlüğe dönüştürmek için
        return {"title": self.title, "author": self.author, "isbn": self.isbn}

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        # JSON'dan geri nesneye dönmek için
        return cls(title=data["title"], author=data["author"], isbn=data["isbn"])