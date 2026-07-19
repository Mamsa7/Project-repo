from datetime import datetime, timedelta
import numpy as np
from app.models import Product, PredictionLog, db
from app.ml.feature_engineering import FeatureEngineer
from app.ml.model_training import ModelTrainer

class PredictionEngine:
    """Generate sales predictions using trained models"""
    
    def __init__(self, model_type='random_forest'):
        self.trainer = ModelTrainer(model_type)
        self.trainer.load_model()
        self.feature_engineer = FeatureEngineer()
    
    def predict_for_product(self, product_id, forecast_days=30):
        """Generate sales forecast for a product"""
        
        if self.trainer.model is None:
            return None
        
        # Get historical sales data
        df = self.feature_engineer.get_daily_sales_for_product(product_id, days_back=180)
        
        if len(df) < 50:  # Insufficient data
            return None
        
        # Engineer features
        df = self.feature_engineer.engineer_features(df)
        X, y, feature_cols = self.feature_engineer.prepare_for_training(df)
        self.trainer.feature_cols = feature_cols
        
        predictions_7d = None
        predictions_30d = None
        
        try:
            # Predict next 7 days
            X_future_7d = self._create_future_features(df, feature_cols, 7)
            if X_future_7d is not None:
                pred_7d = self.trainer.predict(X_future_7d)
                predictions_7d = max(0, np.mean(pred_7d))
            
            # Predict next 30 days
            X_future_30d = self._create_future_features(df, feature_cols, 30)
            if X_future_30d is not None:
                pred_30d = self.trainer.predict(X_future_30d)
                predictions_30d = max(0, np.mean(pred_30d))
            
        except Exception as e:
            print(f"Error generating predictions: {str(e)}")
            return None
        
        if predictions_7d is None or predictions_30d is None:
            return None
        
        return {
            'product_id': product_id,
            'predicted_qty_7d': round(predictions_7d, 2),
            'predicted_qty_30d': round(predictions_30d, 2),
            'confidence_score': 0.85
        }
    
    def _create_future_features(self, df, feature_cols, days_ahead):
        """Create feature matrix for future predictions"""
        if df.empty or days_ahead <= 0:
            return None
        
        # Use last known values and recent patterns
        last_row = df.iloc[-1]
        X_future = []
        
        for i in range(1, days_ahead + 1):
            future_date = df['date'].max() + timedelta(days=i)
            
            features = {
                'day_of_week': future_date.dayofweek,
                'week_of_month': (future_date.day - 1) // 7 + 1,
                'month_of_year': future_date.month,
                'quarter': (future_date.month - 1) // 3 + 1,
                'is_weekend': int(future_date.dayofweek in [5, 6]),
                'lag_1': last_row.get('quantity', 0),
                'lag_7': last_row.get('rolling_7d_mean', 0),
                'lag_14': last_row.get('rolling_7d_mean', 0),
                'lag_30': last_row.get('rolling_30d_mean', 0),
                'rolling_7d_mean': last_row.get('rolling_7d_mean', 0),
                'rolling_7d_std': last_row.get('rolling_7d_std', 0),
                'rolling_30d_mean': last_row.get('rolling_30d_mean', 0),
                'rolling_30d_std': last_row.get('rolling_30d_std', 0)
            }
            
            X_future.append([features.get(col, 0) for col in feature_cols])
        
        return np.array(X_future) if X_future else None
    
    def generate_reorder_recommendation(self, product):
        """Generate reorder recommendation based on prediction"""
        prediction = self.predict_for_product(product.id)
        
        if not prediction:
            return None
        
        supplier = product.supplier
        lead_time_days = supplier.average_lead_time_days if supplier else 7
        
        # Calculate days of supply remaining
        daily_sales_forecast = prediction['predicted_qty_7d'] / 7
        days_until_stockout = product.current_stock / daily_sales_forecast if daily_sales_forecast > 0 else float('inf')
        
        # Determine urgency
        if days_until_stockout < lead_time_days:
            urgency = 'URGENT'
        elif days_until_stockout < lead_time_days * 1.5:
            urgency = 'HIGH'
        else:
            urgency = 'NORMAL'
        
        # Calculate recommended quantity
        demand_during_lead_time = daily_sales_forecast * lead_time_days
        safety_stock = daily_sales_forecast * 7  # 7 days of safety stock
        recommended_qty = max(
            product.reorder_quantity,
            int(demand_during_lead_time + safety_stock - product.current_stock)
        )
        
        return {
            'product_id': product.id,
            'product_name': product.name,
            'current_stock': product.current_stock,
            'predicted_7d_demand': round(prediction['predicted_qty_7d'], 0),
            'predicted_30d_demand': round(prediction['predicted_qty_30d'], 0),
            'lead_time_days': lead_time_days,
            'recommended_quantity': recommended_qty,
            'urgency': urgency,
            'days_until_stockout': round(days_until_stockout, 1)
        }
    
    def generate_all_recommendations(self):
        """Generate recommendations for all products"""
        products = Product.query.all()
        recommendations = []
        
        for product in products:
            rec = self.generate_reorder_recommendation(product)
            if rec:
                recommendations.append(rec)
        
        # Sort by urgency and days until stockout
        urgency_order = {'URGENT': 0, 'HIGH': 1, 'NORMAL': 2}
        recommendations.sort(
            key=lambda x: (urgency_order[x['urgency']], x['days_until_stockout'])
        )
        
        return recommendations
    
    def save_predictions_to_db(self):
        """Persist predictions to database for audit trail"""
        products = Product.query.all()
        
        for product in products:
            prediction = self.predict_for_product(product.id)
            if prediction:
                log_entry = PredictionLog(
                    product_id=product.id,
                    prediction_date=datetime.now().date(),
                    predicted_qty_7d=prediction['predicted_qty_7d'],
                    predicted_qty_30d=prediction['predicted_qty_30d'],
                    confidence_score=prediction.get('confidence_score', 0.85),
                    model_version='rf_v1'
                )
                db.session.add(log_entry)
        
        db.session.commit()
