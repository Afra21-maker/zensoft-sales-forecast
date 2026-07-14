import pandas as pd
import numpy as np

def load_data(path):
    df = pd.read_csv(path)
    return df

def preprocess(df):
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
    df['YearMonth'] = df['Order Date'].dt.to_period('M')
    df['Sales_log'] = np.log1p(df['Sales'])
    return df

def get_monthly_sales(df):
    monthly = df.groupby('YearMonth')['Sales'].sum().reset_index()
    monthly.columns = ['ds', 'y']
    monthly['ds'] = pd.to_datetime(monthly['ds'].astype(str))
    monthly['ay'] = monthly['ds'].dt.month
    monthly['yil'] = monthly['ds'].dt.year
    monthly['ceyrek'] = monthly['ds'].dt.quarter
    return monthly

def train_test_split(monthly_sales, test_months=6):
    train = monthly_sales[:-test_months]
    test = monthly_sales[-test_months:]
    return train, test