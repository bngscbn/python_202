# tests/test_library.py
from library.models import Book
import pytest
from library.storage import Library

def test_book_str():
    b = Book("Ulysses", "James Joyce", "978-0199535675")
    assert "Ulysses by James Joyce" in str(b)
    assert "978-0199535675" in str(b)

def test_book_dict_conversion():
    b = Book("T", "Y", "123")
    d = b.to_dict()
    assert d == {"title": "T", "author": "Y", "isbn": "123"}
    b2 = Book.from_dict(d)
    assert b2 == b

def test_add_and_find(tmp_path):
    lib = Library(tmp_path / "lib.json")
    b = Book("Test", "Yazar", "123")
    lib.add_book(b)
    found = lib.find_book("123")
    assert found is not None
    assert found.title == "Test"

def test_duplicate_isbn_raises(tmp_path):
    lib = Library(tmp_path / "lib.json")
    lib.add_book(Book("T", "Y", "1"))
    with pytest.raises(ValueError):
        lib.add_book(Book("T2", "Y2", "1"))

def test_remove(tmp_path):
    lib = Library(tmp_path / "lib.json")
    lib.add_book(Book("T", "Y", "1"))
    assert lib.remove_book("1") is True
    assert lib.find_book("1") is None
    # tekrar silmeye çalışırsak False dönmeli
    assert lib.remove_book("1") is False

def test_persistence(tmp_path):
    path = tmp_path / "lib.json"
    lib = Library(path)
    lib.add_book(Book("T", "Y", "1"))
    # yeni obje ile yükleme
    lib2 = Library(path)
    assert len(lib2.list_books()) == 1
    assert lib2.find_book("1") is not None