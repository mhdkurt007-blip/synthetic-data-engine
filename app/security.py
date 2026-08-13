from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

# İstek atılırken Header içinde aranacak anahtarın ismi
API_KEY_NAME = "access_token"

# Şirkete vereceğimiz gizli VIP anahtarımız
API_KEY = "thalesoft-secure-2026-key"

# auto_error=True sayesinde anahtar gönderilmezse FastAPI otomatik olarak 403 döner
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def get_api_key(api_key: str = Security(api_key_header)):
    """Gelen isteğin header kısmındaki anahtarı kontrol eder."""
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Geçersiz veya Eksik API Anahtarı! Bu veriyi çekmeye yetkiniz yok."
        )
    return api_key