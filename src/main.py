from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import pandas as pd
from src.preprocess import load_data, preprocess, get_monthly_sales, train_test_split
from src.model import train_prophet, predict_prophet
from src.database import SessionLocal, Prediction, create_tables

app = FastAPI(title="Zensoft Sales Forecast API")

# Tabloları oluştur
create_tables()

# Veriyi yükle ve modeli eğit
DATA_PATH = "data/raw/train.csv"
df = load_data(DATA_PATH)
df = preprocess(df)
monthly_sales = get_monthly_sales(df)
train, test = train_test_split(monthly_sales)
model = train_prophet(train)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Zensoft Sales Forecast API çalışıyor!"}

@app.get("/predict/{months}")
def predict(months: int = 6, db: Session = Depends(get_db)):
    forecast = predict_prophet(model, periods=months)
    result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(months)
    
    # Veritabanına kaydet
    for _, row in result.iterrows():
        prediction = Prediction(
            ds=str(row['ds']),
            yhat=row['yhat'],
            yhat_lower=row['yhat_lower'],
            yhat_upper=row['yhat_upper']
        )
        db.add(prediction)
    db.commit()
    
    result['ds'] = result['ds'].astype(str)
    return result.to_dict(orient='records')

@app.get("/predictions/history")
def get_history(db: Session = Depends(get_db)):
    predictions = db.query(Prediction).all()
    return predictions