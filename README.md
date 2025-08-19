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
```

### 2. Sanal Ortam Oluştur ve Aktif Et
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3. Bağımlılıkları Yükle
```bash
pip install -r requirements.txt
```

## 🚀 Kullanım

### Komut Satırı Uygulaması (Aşama 1 ve 2)
```bash
python main.py
```
Bu komut satırı uygulaması ile kitap ekleyebilir, listeleyebilir, silebilir ve arama yapabilirsiniz.

### FastAPI API Sunucusu (Aşama 3)
```bash
uvicorn api:app --reload
```
Bu komut FastAPI tabanlı API sunucusunu başlatır. `http://localhost:8000` adresinden erişebilirsiniz.

## 🔗 Endpoint’ler

- `GET /books`  
  Tüm kitapları listeler.

- `POST /books`  
  Yeni bir kitap ekler. JSON formatında ISBN bilgisi gönderilmelidir.

- `DELETE /books/{isbn}`  
  Belirtilen ISBN numarasına sahip kitabı siler.

- `PUT /books/{isbn}`  
  Belirtilen ISBN numarasına sahip kitabın bilgilerini günceller.

## 🧪 Testler

Projede yer alan testleri çalıştırmak için aşağıdaki komutu kullanabilirsiniz:
```bash
pytest
```
Tüm testler başarılı şekilde geçmelidir.

## ⚙ Minimum Gereksinimler

- Python 3.10 veya üzeri
- İnternet bağlantısı (Open Library API için)
- `requirements.txt` dosyasındaki bağımlılıkların kurulumu

Bu adımları takip ederek projeyi kolayca kurabilir ve kullanmaya başlayabilirsiniz.