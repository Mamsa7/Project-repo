from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You must be an administrator to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def format_currency(value):
    """Format value as currency"""
    return f"₦{value:,.2f}"

def format_date(date):
    """Format datetime object as string"""
    if isinstance(date, str):
        return date
    return date.strftime('%Y-%m-%d %H:%M') if date else ''

def generate_receipt_number():
    """Generate unique receipt number"""
    import uuid
    timestamp = datetime.now().strftime('%Y%m%d')
    unique = uuid.uuid4().hex[:6].upper()
    return f"RCP-{timestamp}-{unique}"

def calculate_stock_value(products):
    """Calculate total inventory value"""
    return sum(p.current_stock * p.unit_price for p in products)

def calculate_turnover_ratio(product, days=30):
    """Calculate product turnover ratio"""
    from app.models import SaleItem, SaleTransaction
    from sqlalchemy import func
    from app import db
    from datetime import timedelta
    
    start_date = datetime.now() - timedelta(days=days)
    
    qty_sold = db.session.query(func.sum(SaleItem.quantity)).join(
        SaleTransaction
    ).filter(
        SaleItem.product_id == product.id,
        SaleTransaction.created_at >= start_date
    ).scalar() or 0
    
    avg_stock = product.current_stock if product.current_stock > 0 else 1
    return qty_sold / avg_stock if avg_stock > 0 else 0

def get_alert_badge_class(alert_type):
    """Get Bootstrap badge class for alert type"""
    badge_map = {
        'low_stock': 'warning',
        'forecast': 'info',
        'stockout': 'danger',
        'success': 'success'
    }
    return f"badge bg-{badge_map.get(alert_type, 'secondary')}"

def log_activity(user_id, action, details):
    """Log user activity (extensible for audit trail)"""
    logger.info(f"User {user_id}: {action} - {details}")

def safe_divide(numerator, denominator, default=0):
    """Safely divide two numbers"""
    return numerator / denominator if denominator != 0 else default

def round_to(value, decimals=2):
    """Round value to specified decimals"""
    return round(float(value), decimals)