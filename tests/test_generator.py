import pytest
from app.generator import generate_tckn, generate_credit_card, generate_iban, generate_synthetic_customer_data

def test_generate_tckn_validity():
    """Üretilen TCKN'nin 11 haneli olmasını ve Mod11 kuralına uymasını test eder."""
    tckn = generate_tckn()
    
    assert len(tckn) == 11
    assert tckn.isdigit()
    
    # Mod11 Sağlaması (Doğrulama)
    d = [int(x) for x in tckn]
    d10 = ((sum(d[0:9:2]) * 7) - sum(d[1:9:2])) % 10
    d11 = sum(d[0:10]) % 10
    
    assert d[9] == d10
    assert d[10] == d11

def test_generate_credit_card_luhn():
    """Üretilen Kredi Kartının doğru uzunlukta, doğru prefix'te ve Luhn geçerli olmasını test eder."""
    cc = generate_credit_card("TROY")
    
    assert cc.startswith("9792")
    assert len(cc) == 16
    
    # Standart Luhn Doğrulama Testi
    total = 0
    # Kart numarasını ters çevirip indeksliyoruz
    for i, digit in enumerate(cc[::-1]):
        n = int(digit)
        # Check digit 0. indekste kalır, biz 1, 3, 5... (çift sıralı) rakamları 2 ile çarparız
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
        
    # Toplamın 10'a tam bölünmesi gerekir
    assert total % 10 == 0

def test_generate_iban_mod97():
    """Üretilen IBAN'ın 26 haneli olmasını ve resmi ISO 7064 Mod97-10 testini geçmesini kontrol eder."""
    iban = generate_iban()
    
    assert iban.startswith("TR")
    assert len(iban) == 26
    
    # Resmi Mod97 Doğrulama Testi: 
    # İlk 4 karakteri (TR + Check Digits) alıp sona atarız. Harfleri sayıya çeviririz (TR = 2927).
    bban = iban[4:]
    check_digits = iban[2:4]
    
    numeric_string = bban + "2927" + check_digits
    
    # Ortaya çıkan devasa sayının 97'ye bölümünden kalan kesinlikle 1 olmalıdır
    assert int(numeric_string) % 97 == 1

def test_generate_synthetic_customer_profile():
    """Tüm motorun eksiksiz bir müşteri profili sözlüğü (dict) üretip üretmediğini test eder."""
    profile = generate_synthetic_customer_data()
    
    assert "tckn" in profile
    assert "account_iban" in profile
    assert "card_number" in profile
    assert profile["risk_score"] >= 0 and profile["risk_score"] <= 100