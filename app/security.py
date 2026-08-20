from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

# İstek atılırken Header içinde aranacak anahtarın ismi
API_KEY_NAME = "access_token"

# Şifreleri ve onlara ait rolleri sözlük (dictionary) olarak tanımlıyoruz
API_KEYS = {
    "thalesoft-secure-2026-key": "admin",       # Streamlit'in de kullandığı yetkili anahtar
    "thalesoft-read-only-key": "analyst"        # Sadece okuma yapabilecek yeni anahtar
}

# auto_error=True sayesinde anahtar gönderilmezse FastAPI otomatik olarak hata döner
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def get_current_role(api_key: str = Security(api_key_header)):
    """Gelen isteğin header kısmındaki anahtarı kontrol eder ve yetki rolünü döndürür."""
    # Gelen şifreyi API_KEYS sözlüğünde arıyoruz
    role = API_KEYS.get(api_key)
    
    # Şifre sözlükte yoksa (yanlışsa) 401 hatası ver
    if not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Geçersiz API Anahtarı! Bu sisteme erişim yetkiniz bulunmuyor."
        )
    
    # Şifre doğruysa kullanıcının rolünü (admin veya analyst) döndür
    return role