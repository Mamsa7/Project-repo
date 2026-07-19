from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    """User accounts with role-based access"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='staff', nullable=False)  # admin, staff
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    stock_transactions = db.relationship('StockTransaction', backref='user', lazy=True, cascade='all, delete-orphan')
    sale_transactions = db.relationship('SaleTransaction', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.username}>'


class Category(db.Model):
    """Product categories"""
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Supplier(db.Model):
    """Supplier/Vendor records"""
    __tablename__ = 'supplier'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    contact_person = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    average_lead_time_days = db.Column(db.Integer, default=7)  # Days to delivery
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='supplier', lazy=True)
    
    def __repr__(self):
        return f'<Supplier {self.name}>'


class Product(db.Model):
    """Core product and inventory records"""
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    unit_price = db.Column(db.Float, nullable=False)
    reorder_level = db.Column(db.Integer, default=10)  # Threshold for alerts
    reorder_quantity = db.Column(db.Integer, default=50)  # Default reorder amount
    current_stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    stock_transactions = db.relationship('StockTransaction', backref='product', lazy=True, cascade='all, delete-orphan')
    sale_items = db.relationship('SaleItem', backref='product', lazy=True)
    predictions = db.relationship('PredictionLog', backref='product', lazy=True, cascade='all, delete-orphan')
    
    def is_low_stock(self):
        """Check if product is low on stock"""
        return self.current_stock <= self.reorder_level
    
    def stock_value(self):
        """Calculate total stock value"""
        return self.current_stock * self.unit_price
    
    def __repr__(self):
        return f'<Product {self.sku}: {self.name}>'


class StockTransaction(db.Model):
    """Stock movements (in/out/adjustment)"""
    __tablename__ = 'stock_transaction'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # stock_in, stock_out, adjustment
    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Float)
    reference = db.Column(db.String(100))  # PO number, receipt ID, etc.
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<StockTransaction {self.transaction_type} {self.quantity} of Product {self.product_id}>'


class SaleTransaction(db.Model):
    """Sales session/invoice header"""
    __tablename__ = 'sale_transaction'
    
    id = db.Column(db.Integer, primary_key=True)
    receipt_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    total_amount = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    items = db.relationship('SaleItem', backref='transaction', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<SaleTransaction {self.receipt_number}>'


class SaleItem(db.Model):
    """Individual line items within a sale"""
    __tablename__ = 'sale_item'
    
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale_transaction.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SaleItem {self.quantity}x Product {self.product_id}>'


class PredictionLog(db.Model):
    """ML forecast outputs and audit trail"""
    __tablename__ = 'prediction_log'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    prediction_date = db.Column(db.Date, nullable=False, index=True)
    predicted_qty_7d = db.Column(db.Float, nullable=False)  # Predicted demand for next 7 days
    predicted_qty_30d = db.Column(db.Float, nullable=False)  # Predicted demand for next 30 days
    confidence_score = db.Column(db.Float)  # Model confidence (0-1)
    model_version = db.Column(db.String(50))  # Version of trained model used
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        db.UniqueConstraint('product_id', 'prediction_date', 'model_version', name='unique_prediction_per_day'),
    )
    
    def __repr__(self):
        return f'<PredictionLog Product {self.product_id} on {self.prediction_date}>'


class AlertLog(db.Model):
    """System alerts and notifications"""
    __tablename__ = 'alert_log'
    
    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String(50), nullable=False)  # low_stock, forecast, etc.
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    resolved_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<AlertLog {self.alert_type}: {self.title}>'
