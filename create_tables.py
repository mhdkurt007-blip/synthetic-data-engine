from app.database import engine, Base
# Modelleri içeri aktarıyoruz ki SQLAlchemy hangi tabloları üreteceğini bilsin
from app.database import Customer, Account, Transaction

print("Veritabanına bağlanılıyor ve tablolar oluşturuluyor...")

# Bu komut, veritabanına gidip eksik olan tabloları otomatik olarak yaratır
Base.metadata.create_all(bind=engine)

print("İşlem tamam! Tablolar veritabanına başarıyla yazıldı.")