# main.py
from library.storage import Library

MENU = """
--- Kütüphane ---
1. Kitap Ekle (ISBN ile otomatik)
2. Kitap Sil
3. Kitapları Listele
4. Kitap Ara
5. Çıkış
"""

def main() -> None:
    lib = Library("library.json")
    while True:
        print(MENU)
        choice = input("Seçim: ").strip()
        if choice == "1":
            isbn = input("ISBN: ").strip()
            try:
                lib.add_book_by_isbn(isbn)
                print("✅ Kitap eklendi (API).")
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