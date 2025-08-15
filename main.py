# main.py
from library.storage import Library
from library.models import Book

MENU = """
--- Kütüphane ---
1. Kitap Ekle
2. Kitap Sil
3. Kitapları Listele
4. Kitap Ara
5. Çıkış
"""

def prompt_book() -> Book:
    title = input("Başlık: ").strip()
    author = input("Yazar: ").strip()
    isbn = input("ISBN: ").strip()
    return Book(title=title, author=author, isbn=isbn)

def main() -> None:
    lib = Library("library.json")
    while True:
        print(MENU)
        choice = input("Seçim: ").strip()
        if choice == "1":
            try:
                book = prompt_book()
                lib.add_book(book)
                print("✅ Kitap eklendi.")
            except ValueError as e:
                print(f"⚠️  Hata: {e}")
        elif choice == "2":
            isbn = input("Silinecek ISBN: ").strip()
            if lib.remove_book(isbn):
                print("🗑️  Kitap silindi.")
            else:
                print("Bulunamadı.")
        elif choice == "3":
            books = lib.list_books()
            if not books:
                print("Kütüphane boş.")
            for b in books:
                print("-", b)
        elif choice == "4":
            isbn = input("Aranan ISBN: ").strip()
            book = lib.find_book(isbn)
            print(book if book else "Bulunamadı.")
        elif choice == "5":
            print("Görüşürüz!")
            break
        else:
            print("Geçersiz seçim.")

if __name__ == "__main__":
    main()