from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

class TransactionResponse(BaseModel):
    id: int
    card_number: Optional[str]
    amount: float
    # Veritabanında işlem tarihi varsa buraya eklenebilir, şimdilik temel tipleri alıyoruz.

    class Config:
        from_attributes = True

class AccountResponse(BaseModel):
    id: int
    iban: str
    balance: float
    status: str
    transactions: List[TransactionResponse] = []

    class Config:
        from_attributes = True

class CustomerResponse(BaseModel):
    id: int
    tckn: str
    first_name: str
    last_name: str
    birth_date: date
    risk_score: int
    accounts: List[AccountResponse] = []

    class Config:
        from_attributes = True