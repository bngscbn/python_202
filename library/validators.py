
from __future__ import annotations

def normalize_isbn(raw: str) -> str:
    """Boşluk ve tireleri temizle, sade string döndür."""
    s = (raw or "").replace("-", "").replace(" ", "").strip()
    return s

def is_isbn10(s: str) -> bool:
    if len(s) != 10:
        return False
    total = 0
    for i, ch in enumerate(s[:9], start=1):
        if not ch.isdigit():
            return False
        total += i * int(ch)
    checksum = s[9].upper()
    if checksum == "X":
        cval = 10
    elif checksum.isdigit():
        cval = int(checksum)
    else:
        return False
    total += 10 * cval
    return total % 11 == 0

def is_isbn13(s: str) -> bool:
    if len(s) != 13 or not s.isdigit():
        return False
    total = 0
    for i, ch in enumerate(s):
        coef = 1 if i % 2 == 0 else 3
        total += coef * int(ch)
    return total % 10 == 0

def validate_isbn(raw: str) -> str:
    s = normalize_isbn(raw)
    if not s:
        raise ValueError("ISBN boş olamaz.")
    if not (is_isbn10(s) or is_isbn13(s)):
        raise ValueError("Geçersiz ISBN formatı/numarası.")
    return s