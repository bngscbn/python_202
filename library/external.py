# library/external.py
from __future__ import annotations
from typing import Tuple
import time

import httpx

DEFAULT_TIMEOUT = httpx.Timeout(10.0, connect=5.0)
RETRY_STATUS = {429, 500, 502, 503, 504}

class OpenLibraryError(Exception):
    pass

def _backoff_sleep(attempt: int) -> None:
    # 1. deneme: 0.2s, 2.: 0.4s, 3.: 0.8s
    time.sleep(0.2 * (2 ** max(0, attempt - 1)))

def _get_with_retry(client: httpx.Client, url: str) -> httpx.Response:
    last_exc: Exception | None = None
    for attempt in range(1, 4):  # 3 deneme
        try:
            resp = client.get(url)
            if resp.status_code in RETRY_STATUS:
                _backoff_sleep(attempt)
                continue
            return resp
        except httpx.HTTPError as e:
            last_exc = e
            _backoff_sleep(attempt)
    if last_exc:
        raise OpenLibraryError(f"Ağ hatası: {last_exc}") from last_exc
    raise OpenLibraryError("Ağ hatası: tekrar denemeler başarısız.")

def fetch_book_by_isbn(isbn: str) -> Tuple[str, str]:
    """
    Open Library'den ISBN ile (title, author) döndürür.
    - 404 özel mesaj
    - Diğer HTTP hataları OpenLibraryError'a çevrilir
    - Author ismini mümkünse /authors/{key}.json üzerinden çözer
    """
    headers = {"User-Agent": "py202-library/1.0"}
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT, headers=headers) as client:
            # 1) kitap detay
            url = f"https://openlibrary.org/isbn/{isbn}.json"
            resp = _get_with_retry(client, url)
            if resp.status_code == 404:
                raise OpenLibraryError("Kitap bulunamadı (404).")
            try:
                resp.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise OpenLibraryError(f"HTTP hatası: {e.response.status_code}") from e
            data = resp.json()

            title = data.get("title")
            author_name = "Bilinmiyor"

            # 2) author çözümü
            authors = data.get("authors") or []
            if isinstance(authors, list) and authors:
                key = (authors[0] or {}).get("key")
                if key:
                    aurl = f"https://openlibrary.org{key}.json"
                    aresp = _get_with_retry(client, aurl)
                    if aresp.status_code == 200:
                        adata = aresp.json()
                        author_name = adata.get("name") or author_name

            if not title:
                raise OpenLibraryError("Geçersiz veri: başlık yok.")
            return title, author_name
    except httpx.HTTPError as e:
        # bağlantı/timeout vs.
        raise OpenLibraryError(f"Ağ hatası: {e}") from e