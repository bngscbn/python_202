# tests/test_validators.py
import pytest
from library.validators import normalize_isbn, is_isbn10, is_isbn13, validate_isbn

def test_normalize():
    assert normalize_isbn(" 978-0-14-044913-6 ") == "9780140449136"

@pytest.mark.parametrize("isbn,ok", [
    ("0306406152", True),        # geçerli ISBN-10
    ("0306406153", False),
])
def test_isbn10(isbn, ok):
    assert is_isbn10(isbn) is ok

@pytest.mark.parametrize("isbn,ok", [
    ("9780140449136", True),     # geçerli ISBN-13
    ("9780140449135", False),
])
def test_isbn13(isbn, ok):
    assert is_isbn13(isbn) is ok

def test_validate_ok():
    assert validate_isbn("978-0-14-044913-6") == "9780140449136"

@pytest.mark.parametrize("bad", ["", "abc", "123", "9780140449135"])
def test_validate_bad(bad):
    with pytest.raises(ValueError):
        validate_isbn(bad)