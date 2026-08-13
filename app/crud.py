import random
from sqlalchemy.orm import Session
from app.database import Customer, Account, Transaction
from app.generator import generate_synthetic_customer_data, generate_iban, generate_credit_card

def populate_database(db: Session, num_customers: int = 10):
    """Belirtilen sayıda müşteri ve onlara bağlı hesap/işlem ağacını veritabanına yazar."""
    print(f"Sisteme {num_customers} adet sentetik müşteri profili yükleniyor...")
    
    for _ in range(num_customers):
        # 1. Müşteriyi Oluştur (Parent)
        profile = generate_synthetic_customer_data()
        db_customer = Customer(
            tckn=profile["tckn"],
            first_name=profile["first_name"],
            last_name=profile["last_name"],
            birth_date=profile["birth_date"],
            risk_score=profile["risk_score"]
        )
        db.add(db_customer)
        # flush(): Veriyi veritabanına gönderir, ID'sini (Primary Key) alır ama işlemi henüz mühürlemez.
        db.flush() 

        # 2. Müşteriye Rastgele Sayıda Hesap (1-3) Oluştur (Child)
        for _ in range(random.randint(1, 3)):
            db_account = Account(
                customer_id=db_customer.id, # Üstte flush ile oluşan müşteri ID'sini buraya bağlıyoruz
                iban=generate_iban(),
                balance=round(random.uniform(100.0, 50000.0), 2),
                status=random.choice(["ACTIVE", "ACTIVE", "CLOSED"]) # %66 ihtimalle aktif hesap
            )
            db.add(db_account)
            db.flush()

            # 3. O Hesaba Rastgele Sayıda Kredi Kartı İşlemi (1-5) Oluştur (Grandchild)
            for _ in range(random.randint(1, 5)):
                db_transaction = Transaction(
                    account_id=db_account.id,
                    card_number=generate_credit_card("RANDOM"),
                    amount=round(random.uniform(10.0, 5000.0), 2)
                )
                db.add(db_transaction)
                
    # Tüm döngü bittikten sonra verileri tek seferde kalıcı olarak kaydet (Performans için)
    db.commit()
    print("Tüm veriler PostgreSQL ağacına başarıyla yazıldı!")