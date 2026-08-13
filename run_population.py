from app.database import SessionLocal
from app.crud import populate_database

# Veritabanı oturumunu başlat
db = SessionLocal()

try:
    # 10 adet müşteri (ve onların onlarca alt hesabı/işlemi) üretiliyor
    populate_database(db, num_customers=10)
finally:
    # İşlem bitince bağlantıyı kapat (Memory Leak önlemi)
    db.close()