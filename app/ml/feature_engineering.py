import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import func
from app.models import SaleItem, SaleTransaction, db

class FeatureEngineer:
    """Extract features from sales data for ML model"""
    
    @staticmethod
    def get_daily_sales_for_product(product_id, days_back=180):
        """Get daily sales aggregates for a product"""
        data = db.session.query(
            func.date(SaleTransaction.created_at).label('date'),
            func.sum(SaleItem.quantity).label('quantity')
        ).join(SaleItem.transaction).filter(
            SaleItem.product_id == product_id,
            SaleTransaction.created_at >= datetime.now() - timedelta(days=days_back)
        ).group_by(func.date(SaleTransaction.created_at)).all()
        
        dates = []
        quantities = []
        for row in data:
            dates.append(row.date)
            quantities.append(row.quantity or 0)
        
        if not dates:
            return pd.DataFrame({'date': [], 'quantity': []})
        
        return pd.DataFrame({
            'date': dates,
            'quantity': quantities
        })
    
    @staticmethod
    def engineer_features(df):
        """Engineer features from daily sales dataframe"""
        if df.empty:
            return df
        
        df = df.sort_values('date').reset_index(drop=True)
        df['date'] = pd.to_datetime(df['date'])
        
        # Temporal features
        df['day_of_week'] = df['date'].dt.dayofweek
        df['week_of_month'] = (df['date'].dt.day - 1) // 7 + 1
        df['month_of_year'] = df['date'].dt.month
        df['quarter'] = df['date'].dt.quarter
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        # Lag features
        for lag in [1, 7, 14, 30]:
            df[f'lag_{lag}'] = df['quantity'].shift(lag)
        
        # Rolling window statistics
        df['rolling_7d_mean'] = df['quantity'].rolling(window=7, min_periods=1).mean()
        df['rolling_7d_std'] = df['quantity'].rolling(window=7, min_periods=1).std()
        df['rolling_30d_mean'] = df['quantity'].rolling(window=30, min_periods=1).mean()
        df['rolling_30d_std'] = df['quantity'].rolling(window=30, min_periods=1).std()
        
        # Fill NaN values (from lags)
        df = df.fillna(0)
        
        return df
    
    @staticmethod
    def prepare_for_training(df):
        """Prepare dataframe for model training"""
        feature_cols = [
            'day_of_week', 'week_of_month', 'month_of_year', 'quarter', 'is_weekend',
            'lag_1', 'lag_7', 'lag_14', 'lag_30',
            'rolling_7d_mean', 'rolling_7d_std', 'rolling_30d_mean', 'rolling_30d_std'
        ]
        
        X = df[feature_cols].values
        y = df['quantity'].values
        
        return X, y, feature_cols
