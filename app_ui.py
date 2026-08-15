import streamlit as st
import requests
import pandas as pd
import json

API_URL = "https://synthetic-data-api-gz7t.onrender.com"
API_KEY = "thalesoft-secure-2026-key"
HEADERS = {"access_token": API_KEY}

st.set_page_config(page_title="Sentetik Veri Motoru", page_icon="⚙️", layout="wide")

st.title("Sentetik Veri Motoru Kontrol Paneli")
st.markdown("Bu panel, kurumsal testler için kıstaslara uygun anlık sentetik müşteri verisi üretmenizi sağlar.")

if 'veri_var' not in st.session_state:
    st.session_state.veri_var = False
    st.session_state.uretilen_veri = None

# --- SOL KONTROL MENÜSÜ (FİLTRELER) ---
st.sidebar.header("Üretim Kıstasları")
count = st.sidebar.number_input("Veri Adedi", min_value=1, max_value=5000, value=10)

st.sidebar.subheader("Müşteri Profili Filtreleri")
# Yaş Aralığı Seçimi (Min, Max)
age_range = st.sidebar.slider("Yaş Aralığı", 18, 100, (18, 65))

# Risk Skoru Aralığı Seçimi (Min, Max)
risk_range = st.sidebar.slider("Risk Skoru Aralığı", 0, 100, (0, 100))

# ÜRET BUTONU
if st.sidebar.button("Kıstaslara Göre Veri Üret"):
    with st.spinner(f"Sistem belirlenen kıstaslara uygun {count} adet profil üretiyor..."):
        try:
            # Seçilen filtre değerlerini API'ye query param olarak gönderiyoruz
            params = {
                "count": count,
                "min_age": age_range[0],
                "max_age": age_range[1],
                "min_risk_score": risk_range[0],
                "max_risk_score": risk_range[1]
            }
            
            response = requests.post(f"{API_URL}/api/v1/generate", headers=HEADERS, params=params)
            
            if response.status_code == 200:
                st.session_state.uretilen_veri = response.json()
                st.session_state.veri_var = True 
                st.success(f"Başarıyla {count} adet filtrelenmiş profil üretildi ve kaydedildi!")
            else:
                st.error(f"Sunucu Hatası: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("API'ye ulaşılamıyor. Terminalde 'uvicorn' sunucusunun çalıştığından emin olun.")

# --- TABLO VE İNDİRME ALANI ---
if st.session_state.veri_var and st.session_state.uretilen_veri is not None:
    data = st.session_state.uretilen_veri
    df = pd.DataFrame(data)
    df['accounts'] = df['accounts'].apply(lambda x: json.dumps(x, ensure_ascii=False))
    st.dataframe(df, use_container_width=False)

    st.markdown("### 📥 Test Verilerini İndir")
    col1, col2 = st.columns(2)
    
    csv_data = df.to_csv(index=False, sep=';').encode('utf-8-sig')
    col1.download_button("📄 CSV Olarak İndir", data=csv_data, file_name="sentetik_veriler.csv", mime="text/csv")
    
    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    col2.download_button("📦 JSON Olarak İndir", data=json_data, file_name="sentetik_veriler.json", mime="application/json")