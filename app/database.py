import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# .env dosyasındaki gizli değişkenleri (veritabanı şifresi vb.) yükle
load_dotenv()

# Veritabanı bağlantı adresi (Eğer .env okunamazsa varsayılan Docker adresini kullan)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:mysecretpassword@localhost:5432/synthetic_db")

# SQLAlchemy Motoru (Engine) ve Oturum (Session) ayarları
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- ORM MODELLERİ (VERİTABANI TABLOLARI) ---

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    tckn = Column(String(11), unique=True, index=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birth_date = Column(Date, nullable=False)
    risk_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Bire-Çok (One-to-Many) İlişkisi: Bir müşterinin birden fazla hesabı olabilir
    accounts = relationship("Account", back_populates="owner", cascade="all, delete-orphan")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    iban = Column(String(34), unique=True, index=True, nullable=False)
    balance = Column(Float, default=0.0)
    status = Column(String(20), default="ACTIVE") # ACTIVE, CLOSED, BLOCKED
    created_at = Column(DateTime, default=datetime.utcnow)

    # İlişki Bağlantıları (Hesabın kime ait olduğu ve hesabın işlemleri)
    owner = relationship("Customer", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    card_number = Column(String(19), nullable=True) 
    amount = Column(Float, nullable=False)
    transaction_date = Column(DateTime, default=datetime.utcnow)

    # İlişki Bağlantısı (İşlemin hangi hesaba ait olduğu)
    account = relationship("Account", back_populates="transactions")