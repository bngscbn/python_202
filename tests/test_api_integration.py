# tests/test_api_integration.py
import pytest
from library.storage import Library, Book

def test_add_by_isbn_success(monkeypatch, tmp_path):
    # 1) mock: fetch_book_by_isbn sabit değer döndürsün
    from library import external
    def fake_fetch(isbn: str):
        assert isbn == "9780306406157"
        return ("Fake Title", "Fake Author")
    monkeypatch.setattr(external, "fetch_book_by_isbn", fake_fetch)

    # 2) Library ile deneyelim
    lib = Library(tmp_path / "lib.json")
    lib.add_book_by_isbn("9780306406157")

    b = lib.find_book("9780306406157")
    assert b is not None
    assert b.title == "Fake Title"
    assert b.author == "Fake Author"

def test_add_by_isbn_duplicate(monkeypatch, tmp_path):
    from library import external
    monkeypatch.setattr(external, "fetch_book_by_isbn", lambda isbn: ("T", "A"))

    lib = Library(tmp_path / "lib.json")
    lib.add_book(Book("T", "A", "1"))
    with pytest.raises(ValueError):
        lib.add_book_by_isbn("1")

def test_add_by_isbn_not_found(monkeypatch, tmp_path):
    from library import external
    class FakeErr(Exception): pass
    # OpenLibraryError mesajını ValueError olarak bubble ediyoruz; mesajı da test edelim
    def fake_fetch(isbn: str):
        raise external.OpenLibraryError("Kitap bulunamadı (404).")
    monkeypatch.setattr(external, "fetch_book_by_isbn", fake_fetch)

    lib = Library(tmp_path / "lib.json")
    with pytest.raises(ValueError) as e:
        lib.add_book_by_isbn("9780140449136")
    assert "Kitap bulunamadı" in str(e.value)

# tests/test_api_integration.py içine ek

def test_add_by_isbn_rejects_bad_isbn(tmp_path):
    lib = Library(tmp_path / "lib.json")
    with pytest.raises(ValueError):
        lib.add_book_by_isbn("not-an-isbn")