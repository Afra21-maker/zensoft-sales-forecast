import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import requests
import pandas as pd
API_URL = "https://zensoft-sales-forecast-production.up.railway.app"
st.set_page_config(
    page_title="Zensoft Sales Forecast",
    page_icon="assets/icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/combo-chart.png", width=80)
    st.title("Zensoft")
    st.markdown("**Satış Tahmin Modülü**")
    st.divider()
    st.markdown("###  Ayarlar")
    months = st.slider("Tahmin süresi (ay)", min_value=1, max_value=12, value=6)
    st.divider()
    st.markdown("###  Model Bilgisi")
    st.success(" Prophet Modeli")
    st.metric("MAPE", "22.7%")
    st.metric("MAE", "17,421")

# Ana başlık
st.title("Zensoft Satış Tahmin Dashboard'u")
st.markdown("ERP verilerine dayalı yapay zeka destekli satış tahmini")
st.divider()

# Üst metrikler
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Tahmin Dönemi", f"{months} Ay")
with col2:
    st.metric("Model", "Prophet")
with col3:
    st.metric("Doğruluk", "%77.3")
with col4:
    st.metric("Veri Boyutu", "9,800 Satır")

st.divider()

# Tahmin bölümü
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Satış Tahmini")
    if st.button(" Tahmin Al", type="primary", use_container_width=True):
        with st.spinner("Model tahmin yapıyor..."):
            try:
                response = requests.get(f"{API_URL}/predict/{months}")
                data = response.json()
                df = pd.DataFrame(data)

                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df['ds'], y=df['yhat'],
                    name='Tahmin', line=dict(color='#2E86AB', width=3)
                ))
                fig.add_trace(go.Scatter(
                    x=df['ds'], y=df['yhat_upper'],
                    name='Üst Sınır', line=dict(dash='dash', color='#A8DADC'),
                    fill=None
                ))
                fig.add_trace(go.Scatter(
                    x=df['ds'], y=df['yhat_lower'],
                    name='Alt Sınır', line=dict(dash='dash', color='#A8DADC'),
                    fill='tonexty', fillcolor='rgba(168,218,220,0.2)'
                ))
                fig.update_layout(
                    title=f'Önümüzdeki {months} Aylık Satış Tahmini',
                    xaxis_title='Tarih',
                    yaxis_title='Satış ($)',
                    hovermode='x unified',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                )
                st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"API bağlantı hatası: {e}")

with col_right:
    st.subheader("Tahmin Tablosu")
    if st.button(" Veriyi Getir", use_container_width=True):
        try:
            response = requests.get(f"{API_URL}/predictions/history")
            data = response.json()
            df = pd.DataFrame(data)
            df['yhat'] = df['yhat'].round(0).astype(int)
            df['yhat_lower'] = df['yhat_lower'].round(0).astype(int)
            df['yhat_upper'] = df['yhat_upper'].round(0).astype(int)
            df.columns = ['Tarih', 'Tahmin', 'Alt Sınır', 'Üst Sınır']
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Hata: {e}")

st.divider()

# Geçmiş tahminler
st.subheader("Geçmiş Tahminler")
if st.button(" Geçmişi Göster", use_container_width=True):
    try:
        response = requests.get(f"{API_URL}/predictions/history")
        data = response.json()
        df_history = pd.DataFrame(data)
        st.dataframe(df_history, use_container_width=True)
    except Exception as e:
        st.error(f"Hata: {e}")