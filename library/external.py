# library/external.py
from __future__ import annotations
import httpx

class OpenLibraryError(Exception):
    pass

def fetch_book_by_isbn(isbn: str) -> tuple[str, str]:
    """
    Open Library'den ISBN ile (title, author) döndürür.
    404 veya ağ hatasında OpenLibraryError fırlatır.
    """
    url = f"https://openlibrary.org/isbn/{isbn}.json"
    try:
        resp = httpx.get(url, timeout=10)
    except httpx.HTTPError as e:
        raise OpenLibraryError(f"Ağ hatası: {e}") from e

    if resp.status_code == 404:
        raise OpenLibraryError("Kitap bulunamadı (404).")

    resp.raise_for_status()
    data = resp.json()

    title = data.get("title")
    author = "Bilinmiyor"
    if "authors" in data and isinstance(data["authors"], list) and data["authors"]:
        # Basit yaklaşım: bazı yanıtlarda 'name' olmayabilir; yoksa 'Bilinmiyor'
        author = data["authors"][0].get("name") or "Bilinmiyor"

    if not title:
        raise OpenLibraryError("Geçersiz veri: başlık yok.")

    return title, author