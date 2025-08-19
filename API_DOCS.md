

# 📚 Library API Documentation

Bu doküman, **Stage 3: FastAPI ile Kendi API'nizi Oluşturma** aşamasında geliştirdiğimiz REST API’nin uç noktalarını ve kullanım detaylarını açıklar.

---

## 🔗 Base URL
```
http://127.0.0.1:8000
```

---

## 📖 Endpoints

### 1. GET `/books`
- **Açıklama**: Kütüphanedeki tüm kitapların listesini JSON formatında döndürür.
- **Response (200)**:
```json
[
  {
    "isbn": "9780306406157",
    "title": "Theoretical Physics",
    "author": "Albert Einstein"
  },
  {
    "isbn": "9780679783272",
    "title": "Pride and Prejudice",
    "author": "Jane Austen"
  }
]
```

---

### 2. POST `/books`
- **Açıklama**: ISBN alır, Open Library API’den kitap bilgilerini çeker ve kütüphaneye ekler.
- **Request Body**:
```json
{
  "isbn": "9780306406157"
}
```
- **Response (200)**:
```json
{
  "isbn": "9780306406157",
  "title": "Theoretical Physics",
  "author": "Albert Einstein"
}
```
- **Response (400/404)**:
```json
{
  "detail": "Kitap bulunamadı."
}
```

---

### 3. DELETE `/books/{isbn}`
- **Açıklama**: Belirtilen ISBN’e sahip kitabı kütüphaneden siler.
- **Örnek İstek**:
```
DELETE /books/9780306406157
```
- **Response (200)**:
```json
{
  "detail": "Kitap silindi."
}
```
- **Response (404)**:
```json
{
  "detail": "Kitap bulunamadı."
}
```

---

### 4. PUT `/books/{isbn}`
- **Açıklama**: Var olan bir kitabın başlık veya yazar bilgilerini günceller.
- **Request Body**:
```json
{
  "title": "Updated Title",
  "author": "Updated Author"
}
```
- **Response (200)**:
```json
{
  "isbn": "9780306406157",
  "title": "Updated Title",
  "author": "Updated Author"
}
```

---

## ⚡ Test ve Dokümantasyon
- API çalıştırıldığında, otomatik oluşturulmuş interaktif dokümantasyona şu adreslerden erişebilirsiniz:
  - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
  - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)