from sqlalchemy.orm import Session
from app.database import Customer, Account, Transaction

def create_customer_with_relations(db: Session, profile_data: dict):
    # 1. Müşteriyi Oluştur
    new_customer = Customer(
        tckn=profile_data["tckn"],
        first_name=profile_data["first_name"],
        last_name=profile_data["last_name"],
        birth_date=profile_data["birth_date"],
        risk_score=profile_data["risk_score"]
    )
    db.add(new_customer)
    db.flush() 

    # 2. Hesapları Oluştur
    for acc in profile_data.get("accounts", []):
        new_account = Account(
            customer_id=new_customer.id,
            iban=acc["iban"],
            balance=acc["balance"],
            status=acc["status"]
        )
        db.add(new_account)
        db.flush()

        # 3. İşlemleri Oluştur
        for trans in acc.get("transactions", []):
            new_transaction = Transaction(
                account_id=new_account.id,
                card_number=trans["card_number"],
                amount=trans["amount"]
            )
            db.add(new_transaction)

    db.commit()
    
    # BU SATIRI EKLİYORUZ: İlişkili tabloları veritabanından tekrar belleğe çek!
    db.refresh(new_customer)
    
    return new_customer