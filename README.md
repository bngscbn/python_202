# 📚 Py202 Library

Basit bir komut satırı tabanlı kütüphane yönetim sistemi.  
Kitapları ISBN numarası ile ekleyebilir, silebilir, listeleyebilir ve arayabilirsiniz.  

## 🚀 Özellikler
- **ISBN ile kitap ekleme** → Başlık ve yazar bilgisi otomatik olarak [Open Library API](https://openlibrary.org/dev/docs/api/books) üzerinden alınır.
- Kitapları listeleme, silme, arama
- Veriler **JSON dosyasında (library.json)** kalıcı olarak saklanır
- **ISBN doğrulama** (ISBN-10 ve ISBN-13)
- Pytest ile kapsamlı testler (**20/20 passed ✅**)

## 🛠 Kurulum

### 1. Depoyu Klonla
```bash
git clone https://github.com/bngscbn/python_202.git
cd python_202