Markdown
# Sentetik Veri Motoru API

Bu proje; kurumsal yazılım testleri, makine öğrenmesi modelleri ve veri analizi süreçleri için matematiksel olarak doğrulanmış, isteğe bağlı ve gerçeğe en yakın sentetik müşteri verilerini (Mock Data) üreten bir REST API servisidir.

## Temel Bağlantılar
- **API Ana Adresi (Base URL):** `https://synthetic-data-api-gz7t.onrender.com`
- **İnteraktif API Dokümantasyonu (Swagger UI):** `https://synthetic-data-api-gz7t.onrender.com/docs`
- **Kullanıcı Kontrol Paneli (Streamlit):** `https://sentetik-veri-motoru.streamlit.app/`

## Yetkilendirme (Authentication)
API uç noktalarına erişmek ve veri üretmek için yetkilendirme (API Key) zorunludur. İstek atarken şifreyi HTTP başlıklarına (Headers) eklemelisiniz.

**Header Formatı:**
- `access_token: thalesoft-secure-2026-key`

## Temel Uç Noktalar (Endpoints)

### 1. Yeni Sentetik Veri Üretme
Belirlediğiniz kıstaslara göre yeni müşteri profilleri üretir ve veritabanına kaydeder.

- **URL:** `/api/v1/generate`
- **Metot:** `POST`
- **Parametreler (Query):**
  - `count` (int): Üretilecek veri adedi (Varsayılan: 10, Maks: 5000)
  - `min_age` / `max_age` (int): Yaş aralığı
  - `min_risk_score` / `max_risk_score` (int): Risk skoru aralığı

**Örnek Python İstegi (Requests):**
```python
import requests

url = "[https://synthetic-data-api-gz7t.onrender.com/api/v1/generate?count=5&min_age=25&max_age=40](https://synthetic-data-api-gz7t.onrender.com/api/v1/generate?count=5&min_age=25&max_age=40)"
headers = {
    "access_token": "thalesoft-secure-2026-key"
}

response = requests.post(url, headers=headers)
print(response.json())
Örnek Terminal İsteği (cURL):

Bash
curl -X POST "[https://synthetic-data-api-gz7t.onrender.com/api/v1/generate?count=3&min_age=30&max_risk_score=50](https://synthetic-data-api-gz7t.onrender.com/api/v1/generate?count=3&min_age=30&max_risk_score=50)" \
-H "access_token: thalesoft-secure-2026-key" \
-H "accept: application/json"
2. Mevcut Müşterileri Listeleme
Veritabanında önceden üretilmiş ve kayıtlı olan müşterileri sayfalayarak (pagination) getirir.

URL: /api/v1/customers

Metot: GET

Parametreler (Query):

skip (int): Atlanacak kayıt sayısı (Varsayılan: 0)

limit (int): Getirilecek kayıt sayısı (Varsayılan: 50)

Örnek Python İstegi:

Python
import requests

url = "[https://synthetic-data-api-gz7t.onrender.com/api/v1/customers?skip=0&limit=10](https://synthetic-data-api-gz7t.onrender.com/api/v1/customers?skip=0&limit=10)"
headers = {
    "access_token": "thalesoft-secure-2026-key"
}

response = requests.get(url, headers=headers)
print(response.json())