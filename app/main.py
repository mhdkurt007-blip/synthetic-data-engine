from fastapi import FastAPI, Depends, Security, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal, Customer
from app.schemas import CustomerResponse
from app.security import get_api_key
from app.generator import generate_customer_profile
from app.crud import create_customer_with_relations

app = FastAPI(
    title="Sentetik Veri Motoru API",
    description="Matematiksel olarak doğrulanmış, isteğe bağlı ve kalıcı sentetik veri üretir.",
    version="2.0.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["Sistem"])
def root():
    return {"mesaj": "Sentetik Veri Motoru API Sistemine Hoş Geldiniz", "durum": "Aktif"}

# 1. UÇ NOKTA: İstendiği Kadar Taze Veri Üret ve Veritabanına Kaydet (POST)
@app.post("/api/v1/generate", response_model=List[CustomerResponse], tags=["Sentetik Motor"])
def generate_and_save_data(
    count: int = 10, 
    db: Session = Depends(get_db), 
    api_key: str = Security(get_api_key)
):
    """
    Belirtilen adet kadar tamamen yeni ve farklı sentetik müşteri profili üretir,
    veritabanına kalıcı olarak kaydeder ve sonuç olarak anında dışarıya sunar.
    """
    if count <= 0 or count > 5000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tek seferde en az 1, en fazla 5000 adet veri üretebilirsiniz."
        )

    generated_profiles = []
    
    for _ in range(count):
        # 1. Generator ile yeni profil üret
        profile_data = generate_customer_profile()
        
        # 2. CRUD fonksiyonu ile veritabanına kalıcı olarak kaydet
        db_customer = create_customer_with_relations(db, profile_data)
        generated_profiles.append(db_customer)

    return generated_profiles

# 2. UÇ NOKTA: Veritabanında Kayıtlı Olanları Listele (GET)
@app.get("/api/v1/customers", response_model=List[CustomerResponse], dependencies=[Depends(get_api_key)], tags=["Müşteriler"])
def get_customers(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """Veritabanında önceden üretilmiş ve saklanan müşterileri sayfalama (pagination) ile getirir."""
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers