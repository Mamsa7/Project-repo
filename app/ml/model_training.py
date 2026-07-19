from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error
from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib
import os
from datetime import datetime
from app.ml.feature_engineering import FeatureEngineer

class ModelTrainer:
    """Train and evaluate ML models for sales prediction"""
    
    def __init__(self, model_type='random_forest'):
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.feature_cols = None
        self.model_path = 'app/ml/models/'
        
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
    
    def build_model(self):
        """Initialize the selected model"""
        if self.model_type == 'random_forest':
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=15,
                min_samples_leaf=5,
                min_samples_split=2,
                n_jobs=-1,
                random_state=42
            )
        elif self.model_type == 'gradient_boosting':
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                min_samples_leaf=5,
                random_state=42
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def train(self, X, y):
        """Train model on data"""
        if self.model is None:
            self.build_model()
        
        # Split data chronologically (preserve time series structure)
        split_idx = int(len(X) * 0.7)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        # Train
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        
        metrics = {
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mae': mean_absolute_error(y_test, y_pred),
            'mape': mean_absolute_percentage_error(y_test, y_pred),
            'r2': r2_score(y_test, y_pred),
            'test_size': len(X_test),
            'train_size': len(X_train)
        }
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X_train, y_train, cv=5, scoring='r2')
        metrics['cv_mean'] = cv_scores.mean()
        metrics['cv_std'] = cv_scores.std()
        
        return metrics
    
    def predict(self, X):
        """Generate predictions"""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        return self.model.predict(X)
    
    def save_model(self):
        """Persist model to disk"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        model_file = os.path.join(self.model_path, f'{self.model_type}_model_{timestamp}.joblib')
        joblib.dump(self.model, model_file)
        
        # Also save as latest
        latest_file = os.path.join(self.model_path, f'{self.model_type}_model.joblib')
        joblib.dump(self.model, latest_file)
        
        return model_file
    
    def load_model(self):
        """Load model from disk"""
        latest_file = os.path.join(self.model_path, f'{self.model_type}_model.joblib')
        if os.path.exists(latest_file):
            self.model = joblib.load(latest_file)
            return True
        return False
    
    def get_feature_importance(self):
        """Get feature importance scores"""
        if self.model is None or not hasattr(self.model, 'feature_importances_'):
            return None
        
        importances = self.model.feature_importances_
        return {
            col: float(imp) for col, imp in zip(self.feature_cols, importances)
        }
