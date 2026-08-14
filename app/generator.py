import random
from datetime import datetime, timedelta

def generate_tckn() -> str:
    """Mod11 algoritmasına uygun geçerli ve rastgele TCKN üretir."""
    # İlk hane 0 olamaz
    d = [random.randint(1, 9)] + [random.randint(0, 9) for _ in range(8)]
    
    # 10. hanenin hesaplanması: (Tek haneler toplamı * 7 - Çift haneler toplamı) % 10
    d10 = ((sum(d[0:9:2]) * 7) - sum(d[1:9:2])) % 10
    d.append(d10)
    
    # 11. hanenin hesaplanması: İlk 10 hanenin toplamı % 10
    d11 = sum(d) % 10
    d.append(d11)
    
    return "".join(map(str, d))

def generate_credit_card(brand: str = "RANDOM") -> str:
    """Luhn algoritmasına uygun geçerli Visa, Mastercard veya Troy kart numarası üretir."""
    if brand == "RANDOM":
        brand = random.choice(["VISA", "MASTERCARD", "TROY"])
    
    # Markaya göre başlangıç BIN (Bank Identification Number) kodları
    if brand == "VISA":
        prefix = "4"
    elif brand == "MASTERCARD":
        prefix = str(random.randint(51, 55))
    elif brand == "TROY":
        prefix = "9792"
    
    length = 16
    
    # Kontrol hanesi (son hane) hariç geri kalan rakamları rastgele doldur
    cc_num = prefix + "".join([str(random.randint(0, 9)) for _ in range(length - len(prefix) - 1)])
    
    # Luhn algoritması ile son haneyi (Check Digit) hesapla
    total = 0
    reverse_digits = cc_num[::-1]
    
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 0:
            n *= 2
            if n > 9:
                n -= 9
        total += n
        
    check_digit = (10 - (total % 10)) % 10
    return cc_num + str(check_digit)

def generate_iban() -> str:
    """Mod97-10 algoritmasına uygun geçerli TR IBAN üretir."""
    # 5 haneli banka kodu ve 17 haneli hesap numarası (Toplam 22 hane temel hesap)
    bban = "".join([str(random.randint(0, 9)) for _ in range(22)])
    
    # TR harflerinin sayısal karşılığı: T=29, R=27 -> 292700
    numeric_iban = bban + "292700"
    
    # Mod97 hesaplaması
    check_digits = 98 - (int(numeric_iban) % 97)
    check_str = str(check_digits).zfill(2)
    
    return f"TR{check_str}{bban}"

import random
from datetime import datetime, timedelta
# Kendi yazdığın generate_tckn, generate_iban, generate_credit_card fonksiyonlarının import edildiğini varsayıyorum.

def generate_customer_profile(
    min_age: int = 18, 
    max_age: int = 100, 
    min_risk_score: int = 0, 
    max_risk_score: int = 100
):
    """Belirli yaş ve risk skoru kıstaslarına göre müşteri profili üretir."""
    
    # 1. Yaşa göre doğum tarihi hesaplama
    selected_age = random.randint(min_age, max_age)
    birth_date = datetime.today() - timedelta(days=(selected_age * 365 + random.randint(0, 364)))
    
    # 2. Belirlenen aralıkta risk skoru üretme
    risk_score = random.randint(min_risk_score, max_risk_score)
    
    tckn = generate_tckn()
    cc_brand = random.choice(["VISA", "MASTERCARD", "TROY"])
    cc_number = generate_credit_card(cc_brand)
    iban = generate_iban()
    
    first_names = ["Ahmet", "Ayşe", "Mehmet", "Fatma", "Can", "Zeynep", "Ali", "Elif"]
    last_names = ["Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Yıldız", "Öztürk", "Aydın"]
    
    return {
        "tckn": tckn,
        "first_name": random.choice(first_names),
        "last_name": random.choice(last_names),
        "birth_date": birth_date,
        "risk_score": risk_score,
        "accounts": [
            {
                "iban": iban,
                "balance": round(random.uniform(100.0, 50000.0), 2),
                "status": "Aktif",
                "transactions": [
                    {
                        "card_number": cc_number,
                        "amount": round(random.uniform(10.0, 1000.0), 2)
                    }
                ]
            }
        ]
    }