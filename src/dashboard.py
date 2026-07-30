import streamlit as st
import plotly.express as px
import requests
import pandas as pd

st.set_page_config(page_title="Zensoft Sales Forecast", layout="wide")

st.title("🏪 Zensoft Satış Tahmin Dashboard'u")

# API'den tahmin çek
st.subheader("📈 Satış Tahmini")

months = st.slider("Kaç aylık tahmin?", min_value=1, max_value=12, value=6)

if st.button("Tahmin Al"):
    response = requests.get(f"http://127.0.0.1:8000/predict/{months}")
    data = response.json()
    df = pd.DataFrame(data)
    
    fig = px.line(df, x='ds', y='yhat', title=f'Önümüzdeki {months} Aylık Satış Tahmini',
                  labels={'ds': 'Tarih', 'yhat': 'Tahmin'})
    fig.add_scatter(x=df['ds'], y=df['yhat_lower'], name='Alt Sınır', 
                    line=dict(dash='dash', color='gray'))
    fig.add_scatter(x=df['ds'], y=df['yhat_upper'], name='Üst Sınır',
                    line=dict(dash='dash', color='gray'))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df)

# Geçmiş tahminler
st.subheader("📊 Geçmiş Tahminler")
if st.button("Geçmişi Göster"):
    response = requests.get("http://127.0.0.1:8000/predictions/history")
    data = response.json()
    df_history = pd.DataFrame(data)
    st.dataframe(df_history)