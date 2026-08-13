import streamlit as st
import requests
import pandas as pd
import json

# --- API YAPILANDIRMASI ---
API_URL = "http://127.0.0.1:8000"
API_KEY = "thalesoft-secure-2026-key"
HEADERS = {"access_token": API_KEY}

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Sentetik Veri Motoru", page_icon="⚙️", layout="wide")

st.title("⚙️ Sentetik Veri Motoru Kontrol Paneli")
st.markdown("Bu panel, kurumsal testler için anlık sentetik müşteri verisi üretmenizi sağlar.")

# =======================================================
# --- HAFIZA (SESSION STATE) İLKLEME ---
# Eğer hafızada 'veri_var' diye bir bilgi yoksa, oluştur ve False yap
if 'veri_var' not in st.session_state:
    st.session_state.veri_var = False
    st.session_state.uretilen_veri = None
# =======================================================

# --- SOL KONTROL MENÜSÜ (SIDEBAR) ---
st.sidebar.header("🛠️ Üretim Parametreleri")
count = st.sidebar.number_input("Veri Adedi", min_value=1, max_value=5000, value=10)

# ÜRET BUTONU
if st.sidebar.button("🚀 Veri Üret ve Kaydet"):
    with st.spinner(f"Sistem {count} adet benzersiz profil üretiyor, lütfen bekleyin..."):
        try:
            response = requests.post(f"{API_URL}/api/v1/generate?count={count}", headers=HEADERS)
            
            if response.status_code == 200:
                # Veriyi hafızaya (session_state) kaydediyoruz
                st.session_state.uretilen_veri = response.json()
                st.session_state.veri_var = True 
                st.success(f"✅ Başarıyla {count} adet profil üretildi ve PostgreSQL'e yazıldı!")
            else:
                st.error(f"Sunucu Hatası: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("API'ye ulaşılamıyor. Terminalde 'uvicorn' sunucusunun çalıştığından emin olun.")

# =======================================================
# --- TABLO VE İNDİRME BUTONLARI (HAFIZADAN OKUMA) ---
# Eğer hafızada veri varsa (sayfa yenilense bile), bunları ekranda göstermeye devam et
if st.session_state.veri_var and st.session_state.uretilen_veri is not None:
    
    data = st.session_state.uretilen_veri
    
    # --- TABLO DÜZENLEMESİ ---
    df = pd.DataFrame(data)
    df['accounts'] = df['accounts'].apply(lambda x: json.dumps(x, ensure_ascii=False))
    st.dataframe(df, use_container_width=False)

    # --- DIŞA AKTARMA (EXPORT) MODÜLLERİ ---
    st.markdown("### 📥 Test Verilerini İndir")
    st.markdown("Üretilen verileri test ortamlarınızda kullanmak için indirebilirsiniz.")
    
    col1, col2 = st.columns(2)
    
    # 1. CSV Butonu
    csv_data = df.to_csv(index=False, sep=';').encode('utf-8-sig')
    col1.download_button(
        label="📄 CSV Olarak İndir",
        data=csv_data,
        file_name="sentetik_veriler.csv",
        mime="text/csv"
    )
    
    # 2. JSON Butonu
    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    col2.download_button(
        label="📦 JSON Olarak İndir",
        data=json_data,
        file_name="sentetik_veriler.json",
        mime="application/json"
    )