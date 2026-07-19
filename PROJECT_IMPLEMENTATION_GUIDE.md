# Integrated Inventory and Sales Analytics System - Implementation Guide

**Project**: Design and Implementation of an Integrated Inventory and Sales Analytics with Decision Support for SMEs  
**Author**: Umar Bala Abdulmumin (FCP/CIT/22/1033)  
**Supervisor**: Mal. A.H Galadima  
**Institution**: Federal University Dutse, Department of Information Technology  
**Academic Year**: 2025

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Project Structure](#project-structure)
3. [Technology Stack Details](#technology-stack-details)
4. [Implementation Phases](#implementation-phases)
5. [Database Schema](#database-schema)
6. [API Endpoints](#api-endpoints)
7. [ML Pipeline](#ml-pipeline)
8. [Testing Strategy](#testing-strategy)
9. [Deployment Guide](#deployment-guide)

---

## Executive Summary

This implementation guide provides detailed technical specifications for building an SME-focused inventory and sales analytics system with ML-based decision support. The system integrates:

- **Real-time inventory management** with automated low-stock alerts
- **Sales transaction recording** with automatic receipt generation
- **Advanced analytics dashboards** for sales performance tracking
- **ML-powered demand forecasting** using Random Forest/Gradient Boosting
- **Prescriptive decision support** with reorder recommendations

### Key Features
✅ Three-tier architecture (Frontend, Backend, Database)  
✅ Role-based access control (Admin, Sales Staff)  
✅ Mobile-responsive UI using Bootstrap 5  
✅ Interactive dashboards with Chart.js  
✅ Random Forest ML model for sales prediction  
✅ Weekly model retraining pipeline  
✅ Production-ready with PostgreSQL backend

---

## Project Structure

```
Project-repo/
├── README.md                          # Project overview
├── PROJECT_IMPLEMENTATION_GUIDE.md    # This file
├── requirements.txt                   # Python dependencies
├── config.py                          # Configuration management
├── run.py                             # Application entry point
│
├── app/                               # Main application package
│   ├── __init__.py                    # Flask app factory
│   ├── models.py                      # Database models (SQLAlchemy)
│   ├── forms.py                       # WTForms form definitions
│   ├── utils.py                       # Utility functions
│   │
│   ├── blueprints/
│   │   ├── auth.py                    # Authentication & user management
│   │   ├── inventory.py               # Inventory management routes
│   │   ├── sales.py                   # Sales transaction routes
│   │   ├── analytics.py               # Reporting & dashboards
│   │   ├── predictions.py             # ML predictions & decision support
│   │   └── admin.py                   # Admin panel
│   │
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── preprocessing.py           # Data preprocessing pipeline
│   │   ├── feature_engineering.py     # Feature extraction
│   │   ├── model_training.py          # Model training & evaluation
│   │   ├── model_serving.py           # Prediction serving
│   │   └── models/                    # Trained model storage
│   │       ├── random_forest_model.joblib
│   │       ├── gradient_boosting_model.joblib
│   │       └── feature_scaler.joblib
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── custom.css             # Custom styling
│   │   ├── js/
│   │   │   ├── charts.js              # Chart.js configurations
│   │   │   └── utils.js               # Utility JavaScript functions
│   │   └── images/                    # Logo, icons
│   │
│   └── templates/
│       ├── base.html                  # Base template with navbar
│       ├── auth/
│       │   ├── login.html
│       │   ├── register.html
│       │   └── profile.html
│       ├── inventory/
│       │   ├── products.html          # Product listing & management
│       │   ├── categories.html        # Category management
│       │   ├── suppliers.html         # Supplier management
│       │   └── stock_transactions.html # Stock movement records
│       ├── sales/
│       │   ├── new_sale.html          # Point of sale interface
│       │   ├── sales_history.html     # Sales transaction history
│       │   └── receipt.html           # Receipt template
│       ├── analytics/
│       │   ├── dashboard.html         # Main analytics dashboard
│       │   ├── sales_report.html      # Detailed sales reports
│       │   ├── product_performance.html # Product metrics
│       │   └── trends.html            # Trend analysis
│       └── predictions/
│           ├── forecast.html          # Demand forecast view
│           └── recommendations.html   # Reorder recommendations
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py                 # Database model tests
│   ├── test_inventory.py              # Inventory module tests
│   ├── test_sales.py                  # Sales module tests
│   ├── test_ml.py                     # ML pipeline tests
│   └── test_integration.py            # End-to-end tests
│
├── migrations/                         # Alembic database migrations
│   ├── versions/
│   └── env.py
│
├── scripts/
│   ├── init_db.py                     # Database initialization
│   ├── seed_data.py                   # Sample data generation
│   ├── train_model.py                 # ML model training
│   └── retrain_scheduler.py           # Automated retraining scheduler
│
├── docs/
│   ├── API_DOCUMENTATION.md           # REST API specs
│   ├── DATABASE_SCHEMA.md             # Database documentation
│   ├── ML_PIPELINE.md                 # ML model documentation
│   └── USER_GUIDE.md                  # End-user documentation
│
└── .gitignore                         # Git ignore rules

```

---

## Technology Stack Details

### Backend: Python Flask Architecture

#### Core Dependencies
```
Flask==3.0.0                    # Web framework
Flask-SQLAlchemy==3.1.1         # ORM integration
Flask-Login==0.6.3              # Session management
Flask-WTF==1.2.1                # Form handling
Flask-Migrate==4.0.5            # Database migrations (Alembic)
Werkzeug==3.0.1                 # WSGI utilities & hashing
```

#### Machine Learning Stack
```
scikit-learn==1.4.0             # RF, GB implementations
pandas==2.2.0                   # Data manipulation
numpy==1.26.0                   # Numerical operations
joblib==1.4.0                   # Model serialization
python-dateutil==2.8.2          # Date/time utilities
```

#### Database
```
SQLAlchemy==2.0.25              # ORM
psycopg2-binary==2.9.9          # PostgreSQL adapter
```

#### Additional Tools
```
python-dotenv==1.0.0            # Environment variables
requests==2.31.0                # HTTP library
gunicorn==21.2.0                # Production WSGI server
```

### Frontend Stack
- **HTML5** with Jinja2 templating
- **Bootstrap 5.3** for responsive UI
- **Chart.js 4** for interactive visualizations
- **Vanilla JavaScript** (no framework required)

### Database
- **Development**: SQLite 3
- **Production**: PostgreSQL 15+

---

## Implementation Phases

### Phase 1: Foundation & Setup (Weeks 1-2)

#### 1.1 Project Initialization
```bash
# Create project structure
mkdir Project-repo
cd Project-repo

# Initialize git
git init
git remote add origin https://github.com/Mamsa7/Project-repo.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 1.2 Flask App Factory Setup
Create `app/__init__.py`:
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load configuration
    if config_name == 'production':
        from config import ProductionConfig
        app.config.from_object(ProductionConfig)
    else:
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.blueprints import auth, inventory, sales, analytics, predictions
    app.register_blueprint(auth.bp)
    app.register_blueprint(inventory.bp)
    app.register_blueprint(sales.bp)
    app.register_blueprint(analytics.bp)
    app.register_blueprint(predictions.bp)
    
    # Context processor for template globals
    @app.context_processor
    def inject_globals():
        return {
            'app_name': 'SME Analytics & Inventory System',
            'current_year': datetime.now().year
        }
    
    return app
```

#### 1.3 Configuration Management
Create `config.py`:
```python
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    
    # ML Configuration
    ML_MODEL_PATH = 'app/ml/models/'
    RETRAIN_INTERVAL_DAYS = 7
    MIN_DATA_POINTS_FOR_TRAINING = 50

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sme_analytics_dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_ECHO = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
```

#### 1.4 Application Entry Point
Create `run.py`:
```python
import os
from dotenv import load_dotenv
from app import create_app, db

load_dotenv()

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    return {'db': db}

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Database initialized.")

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
```

---

### Phase 2: Database Design & Models (Weeks 3-4)

#### 2.1 SQLAlchemy Models
Create `app/models.py`:

```python
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    """User accounts with role-based access"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='staff', nullable=False)  # admin, staff
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    stock_transactions = db.relationship('StockTransaction', backref='user', lazy=True)
    sale_transactions = db.relationship('SaleTransaction', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Category(db.Model):
    """Product categories"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Supplier(db.Model):
    """Supplier/Vendor records"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    contact_person = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    average_lead_time_days = db.Column(db.Integer, default=7)  # Days to delivery
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='supplier', lazy=True)
    
    def __repr__(self):
        return f'<Supplier {self.name}>'


class Product(db.Model):
    """Core product and inventory records"""
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
    
    def __repr__(self):
        return f'<Product {self.sku}: {self.name}>'


class StockTransaction(db.Model):
    """Stock movements (in/out/adjustment)"""
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # stock_in, stock_out, adjustment
    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Float)
    reference = db.Column(db.String(100))  # PO number, receipt ID, etc.
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<StockTransaction {self.transaction_type} {self.quantity} of Product {self.product_id}>'


class SaleTransaction(db.Model):
    """Sales session/invoice header"""
    id = db.Column(db.Integer, primary_key=True)
    receipt_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    total_amount = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    items = db.relationship('SaleItem', backref='transaction', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<SaleTransaction {self.receipt_number}>'


class SaleItem(db.Model):
    """Individual line items within a sale"""
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale_transaction.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<SaleItem {self.quantity}x Product {self.product_id}>'


class PredictionLog(db.Model):
    """ML forecast outputs and audit trail"""
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
```

#### 2.2 Database Initialization Script
Create `scripts/init_db.py`:

```python
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app, db
from app.models import Category, Supplier, Product, User

def init_database():
    """Initialize database with tables and seed data"""
    app = create_app('development')
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        # Create default admin user
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@smeanalytics.local', role='admin')
            admin.set_password('admin123')  # CHANGE IN PRODUCTION
            db.session.add(admin)
            print("Created admin user: admin / admin123")
        
        # Create sample categories
        categories = ['Electronics', 'Clothing', 'Food & Beverage', 'Household']
        for cat_name in categories:
            if not Category.query.filter_by(name=cat_name).first():
                cat = Category(name=cat_name, description=f'{cat_name} products')
                db.session.add(cat)
        
        # Create sample supplier
        if not Supplier.query.filter_by(name='ABC Wholesalers').first():
            supplier = Supplier(
                name='ABC Wholesalers',
                contact_person='John Doe',
                phone='+1-555-0100',
                email='sales@abcwholesalers.com',
                average_lead_time_days=7
            )
            db.session.add(supplier)
        
        db.session.commit()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()
```

Run initialization:
```bash
python scripts/init_db.py
```

---

### Phase 3: Authentication & User Management (Weeks 5-6)

#### 3.1 Auth Blueprint
Create `app/blueprints/auth.py`:

```python
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from app.models import User
from app.forms import LoginForm, RegistrationForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to access this page.', 'warning')
    return redirect(url_for('auth.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('inventory.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        
        if not user.is_active:
            flash('Your account has been deactivated.', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_has_no_scheme(next_page):
            next_page = url_for('inventory.dashboard')
        return redirect(next_page)
    
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    """Admin-only user registration"""
    if current_user.role != 'admin':
        flash('Only administrators can register new users.', 'danger')
        return redirect(url_for('inventory.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('auth.register'))
        
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash(f'User {user.username} created successfully!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

def url_has_no_scheme(url):
    return url.startswith('/')
```

#### 3.2 Login Template
Create `app/templates/auth/login.html`:

```html
{% extends "base.html" %}

{% block title %}Login{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card shadow">
                <div class="card-body p-5">
                    <h1 class="card-title text-center mb-4">SME Analytics System</h1>
                    <h5 class="text-center text-muted mb-4">Login</h5>
                    
                    {% with messages = get_flashed_messages(with_categories=true) %}
                        {% if messages %}
                            {% for category, message in messages %}
                                <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                                    {{ message }}
                                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                                </div>
                            {% endfor %}
                        {% endif %}
                    {% endwith %}
                    
                    <form method="POST" novalidate>
                        {{ form.hidden_tag() }}
                        
                        <div class="mb-3">
                            {{ form.username.label }}
                            {% if form.username.errors %}
                                {{ form.username(class="form-control is-invalid") }}
                                <div class="invalid-feedback d-block">
                                    {% for error in form.username.errors %}{{ error }}{% endfor %}
                                </div>
                            {% else %}
                                {{ form.username(class="form-control") }}
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            {{ form.password.label }}
                            {% if form.password.errors %}
                                {{ form.password(class="form-control is-invalid") }}
                                <div class="invalid-feedback d-block">
                                    {% for error in form.password.errors %}{{ error }}{% endfor %}
                                </div>
                            {% else %}
                                {{ form.password(class="form-control") }}
                            {% endif %}
                        </div>
                        
                        <div class="mb-3 form-check">
                            {{ form.remember_me(class="form-check-input") }}
                            {{ form.remember_me.label(class="form-check-label") }}
                        </div>
                        
                        {{ form.submit(class="btn btn-primary w-100") }}
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

### Phase 4: Inventory Management Module (Weeks 7-8)

Create `app/blueprints/inventory.py`:

```python
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import desc
from app import db
from app.models import Product, Category, Supplier, StockTransaction, AlertLog
from datetime import datetime, timedelta

bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@bp.before_request
@login_required
def before_request():
    pass

@bp.route('/')
@bp.route('/dashboard')
def dashboard():
    """Main inventory dashboard"""
    total_products = Product.query.count()
    low_stock_items = Product.query.filter(Product.current_stock <= Product.reorder_level).all()
    total_stock_value = db.session.query(db.func.sum(Product.current_stock * Product.unit_price)).scalar() or 0
    
    # Recent transactions
    recent_transactions = StockTransaction.query.order_by(desc(StockTransaction.created_at)).limit(10).all()
    
    return render_template('inventory/dashboard.html',
                         total_products=total_products,
                         low_stock_items=low_stock_items,
                         total_stock_value=total_stock_value,
                         recent_transactions=recent_transactions)

@bp.route('/products')
def products():
    """Product listing with search and pagination"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Product.query
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%') | Product.sku.ilike(f'%{search}%'))
    
    products = query.paginate(page=page, per_page=20)
    categories = Category.query.all()
    
    return render_template('inventory/products.html',
                         products=products,
                         categories=categories,
                         search=search)

@bp.route('/products/create', methods=['GET', 'POST'])
def create_product():
    """Create new product"""
    if current_user.role != 'admin':
        flash('Only administrators can create products.', 'danger')
        return redirect(url_for('inventory.products'))
    
    if request.method == 'POST':
        try:
            product = Product(
                name=request.form.get('name'),
                sku=request.form.get('sku'),
                description=request.form.get('description'),
                category_id=request.form.get('category_id', type=int),
                supplier_id=request.form.get('supplier_id', type=int),
                unit_price=request.form.get('unit_price', type=float),
                reorder_level=request.form.get('reorder_level', type=int),
                reorder_quantity=request.form.get('reorder_quantity', type=int)
            )
            db.session.add(product)
            db.session.commit()
            
            flash(f'Product {product.name} created successfully!', 'success')
            return redirect(url_for('inventory.products'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating product: {str(e)}', 'danger')
    
    categories = Category.query.all()
    suppliers = Supplier.query.all()
    return render_template('inventory/product_form.html', categories=categories, suppliers=suppliers)

@bp.route('/stock-in', methods=['GET', 'POST'])
def stock_in():
    """Record stock receipt from supplier"""
    if request.method == 'POST':
        try:
            product_id = request.form.get('product_id', type=int)
            quantity = request.form.get('quantity', type=int)
            unit_cost = request.form.get('unit_cost', type=float)
            reference = request.form.get('reference')  # PO number
            
            product = Product.query.get_or_404(product_id)
            
            # Create transaction
            transaction = StockTransaction(
                product_id=product_id,
                transaction_type='stock_in',
                quantity=quantity,
                unit_cost=unit_cost,
                reference=reference,
                user_id=current_user.id
            )
            db.session.add(transaction)
            
            # Update product stock
            product.current_stock += quantity
            product.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            flash(f'Stock receipt recorded: +{quantity} {product.name}', 'success')
            return redirect(url_for('inventory.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error recording stock: {str(e)}', 'danger')
    
    products = Product.query.all()
    return render_template('inventory/stock_in.html', products=products)

@bp.route('/api/products/<int:product_id>')
def get_product_api(product_id):
    """API endpoint for product details (AJAX)"""
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'sku': product.sku,
        'current_stock': product.current_stock,
        'unit_price': product.unit_price,
        'reorder_level': product.reorder_level,
        'category': product.category.name if product.category else None
    })

@bp.route('/api/low-stock-alerts')
def get_low_stock_alerts():
    """API endpoint for low stock alerts"""
    low_stock = Product.query.filter(
        Product.current_stock <= Product.reorder_level
    ).all()
    
    return jsonify({
        'count': len(low_stock),
        'items': [{
            'id': p.id,
            'name': p.name,
            'current_stock': p.current_stock,
            'reorder_level': p.reorder_level,
            'shortage': p.reorder_level - p.current_stock
        } for p in low_stock]
    })
```

---

### Phase 5: Sales Management Module (Weeks 9-10)

Create `app/blueprints/sales.py`:

```python
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import desc
from app import db
from app.models import Product, SaleTransaction, SaleItem, AlertLog
from datetime import datetime
import uuid

bp = Blueprint('sales', __name__, url_prefix='/sales')

@bp.before_request
@login_required
def before_request():
    pass

@bp.route('/new', methods=['GET', 'POST'])
def new_sale():
    """Point of Sale (POS) interface"""
    if request.method == 'POST':
        try:
            items_data = request.json.get('items', [])
            
            if not items_data:
                return jsonify({'error': 'No items in sale'}), 400
            
            # Create sale transaction
            receipt_number = f"RCP-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
            total_amount = 0
            
            sale = SaleTransaction(
                receipt_number=receipt_number,
                user_id=current_user.id,
                total_amount=0  # Will update after items
            )
            db.session.add(sale)
            db.session.flush()  # Get the sale ID
            
            # Process sale items
            low_stock_products = []
            for item_data in items_data:
                product = Product.query.get(item_data['product_id'])
                if not product:
                    db.session.rollback()
                    return jsonify({'error': f'Product {item_data["product_id"]} not found'}), 404
                
                quantity = item_data['quantity']
                unit_price = item_data['unit_price']
                subtotal = quantity * unit_price
                
                # Create sale item
                sale_item = SaleItem(
                    sale_id=sale.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=unit_price,
                    subtotal=subtotal
                )
                db.session.add(sale_item)
                
                # Update product stock
                product.current_stock -= quantity
                product.updated_at = datetime.utcnow()
                
                total_amount += subtotal
                
                # Check for low stock
                if product.current_stock <= product.reorder_level:
                    low_stock_products.append(product)
                    
                    # Create alert
                    alert = AlertLog(
                        alert_type='low_stock',
                        product_id=product.id,
                        title=f'Low Stock: {product.name}',
                        message=f'{product.name} is low on stock. Current: {product.current_stock}, Reorder level: {product.reorder_level}'
                    )
                    db.session.add(alert)
            
            # Update total amount
            sale.total_amount = total_amount
            db.session.commit()
            
            return jsonify({
                'success': True,
                'receipt_number': receipt_number,
                'total_amount': total_amount,
                'low_stock_alerts': len(low_stock_products)
            })
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    products = Product.query.all()
    return render_template('sales/new_sale.html', products=products)

@bp.route('/history')
def history():
    """Sales transaction history"""
    page = request.args.get('page', 1, type=int)
    sales = SaleTransaction.query.order_by(desc(SaleTransaction.created_at)).paginate(page=page, per_page=20)
    return render_template('sales/history.html', sales=sales)

@bp.route('/receipt/<receipt_number>')
def view_receipt(receipt_number):
    """View/print receipt"""
    sale = SaleTransaction.query.filter_by(receipt_number=receipt_number).first_or_404()
    return render_template('sales/receipt.html', sale=sale)

@bp.route('/api/sales-summary')
def get_sales_summary():
    """API endpoint for sales summary (AJAX/Dashboard)"""
    from sqlalchemy import func
    
    # Today's sales
    today_sales = db.session.query(func.sum(SaleTransaction.total_amount)).filter(
        func.date(SaleTransaction.created_at) == datetime.now().date()
    ).scalar() or 0
    
    # This week's sales
    week_ago = datetime.now() - timedelta(days=7)
    week_sales = db.session.query(func.sum(SaleTransaction.total_amount)).filter(
        SaleTransaction.created_at >= week_ago
    ).scalar() or 0
    
    # This month's sales
    month_ago = datetime.now() - timedelta(days=30)
    month_sales = db.session.query(func.sum(SaleTransaction.total_amount)).filter(
        SaleTransaction.created_at >= month_ago
    ).scalar() or 0
    
    return jsonify({
        'today': today_sales,
        'week': week_sales,
        'month': month_sales
    })
```

---

### Phase 6: ML Pipeline & Decision Support (Weeks 11-14)

#### 6.1 Feature Engineering
Create `app/ml/feature_engineering.py`:

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import func
from app.models import SaleItem, db

class FeatureEngineer:
    """Extract features from sales data for ML model"""
    
    @staticmethod
    def get_daily_sales_for_product(product_id, days_back=180):
        """Get daily sales aggregates for a product"""
        data = db.session.query(
            func.date(SaleItem.created_at).label('date'),
            func.sum(SaleItem.quantity).label('quantity')
        ).join(SaleItem.sale_transaction).filter(
            SaleItem.product_id == product_id
        ).filter(
            SaleItem.created_at >= datetime.now() - timedelta(days=days_back)
        ).group_by(func.date(SaleItem.created_at)).all()
        
        dates = []
        quantities = []
        for row in data:
            dates.append(row.date)
            quantities.append(row.quantity or 0)
        
        return pd.DataFrame({
            'date': dates,
            'quantity': quantities
        })
    
    @staticmethod
    def engineer_features(df):
        """Engineer features from daily sales dataframe"""
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
```

#### 6.2 Model Training
Create `app/ml/model_training.py`:

```python
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
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
```

#### 6.3 Model Serving (Predictions)
Create `app/ml/model_serving.py`:

```python
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
        
        # Generate future dates
        last_date = df['date'].max()
        future_dates = [last_date + timedelta(days=i) for i in range(1, forecast_days + 1)]
        
        predictions_7d = None
        predictions_30d = None
        
        try:
            # Predict next 7 days
            X_future_7d = self._create_future_features(df, feature_cols, 7)
            pred_7d = self.trainer.predict(X_future_7d)
            predictions_7d = max(0, np.mean(pred_7d))  # Average prediction for 7 days
            
            # Predict next 30 days
            X_future_30d = self._create_future_features(df, feature_cols, 30)
            pred_30d = self.trainer.predict(X_future_30d)
            predictions_30d = max(0, np.mean(pred_30d))  # Average prediction for 30 days
            
        except Exception as e:
            print(f"Error generating predictions: {str(e)}")
            return None
        
        return {
            'product_id': product_id,
            'predicted_qty_7d': round(predictions_7d, 2),
            'predicted_qty_30d': round(predictions_30d, 2),
            'confidence_score': 0.85  # Placeholder; could be calculated from model uncertainty
        }
    
    def _create_future_features(self, df, feature_cols, days_ahead):
        """Create feature matrix for future predictions"""
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
        
        return np.array(X_future)
    
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
                    model_version='rf_v1'  # Update version as models change
                )
                db.session.add(log_entry)
        
        db.session.commit()
```

#### 6.4 Predictions Blueprint
Create `app/blueprints/predictions.py`:

```python
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app.ml.model_serving import PredictionEngine
from app.models import Product, PredictionLog, db
from sqlalchemy import desc
from datetime import datetime, timedelta

bp = Blueprint('predictions', __name__, url_prefix='/predictions')

@bp.before_request
@login_required
def before_request():
    pass

@bp.route('/forecast')
def forecast():
    """Display demand forecast for all products"""
    engine = PredictionEngine()
    recommendations = engine.generate_all_recommendations()
    
    return render_template('predictions/forecast.html', recommendations=recommendations)

@bp.route('/recommendations')
def recommendations():
    """Display reorder recommendations"""
    engine = PredictionEngine()
    recommendations = engine.generate_all_recommendations()
    
    # Filter by urgency if requested
    urgency_filter = request.args.get('urgency')
    if urgency_filter:
        recommendations = [r for r in recommendations if r['urgency'] == urgency_filter]
    
    return render_template('predictions/recommendations.html', recommendations=recommendations)

@bp.route('/product/<int:product_id>')
def product_forecast(product_id):
    """Forecast for a specific product with historical data"""
    product = Product.query.get_or_404(product_id)
    
    engine = PredictionEngine()
    prediction = engine.predict_for_product(product_id)
    recommendation = engine.generate_reorder_recommendation(product)
    
    # Get historical predictions
    history = PredictionLog.query.filter_by(product_id=product_id).order_by(
        desc(PredictionLog.created_at)
    ).limit(30).all()
    
    return render_template('predictions/product_forecast.html',
                         product=product,
                         prediction=prediction,
                         recommendation=recommendation,
                         history=history)

@bp.route('/api/retrain', methods=['POST'])
def trigger_retrain():
    """Admin endpoint to trigger model retraining (ADMIN ONLY)"""
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        from app.ml.model_training import ModelTrainer
        from app.ml.feature_engineering import FeatureEngineer
        
        trainer = ModelTrainer('random_forest')
        feature_engineer = FeatureEngineer()
        
        # Retrain on all products
        products = Product.query.all()
        X_all = []
        y_all = []
        
        for product in products:
            df = feature_engineer.get_daily_sales_for_product(product.id)
            if len(df) >= 50:
                df = feature_engineer.engineer_features(df)
                X, y, feature_cols = feature_engineer.prepare_for_training(df)
                X_all.extend(X)
                y_all.extend(y)
        
        if X_all:
            import numpy as np
            X_all = np.array(X_all)
            y_all = np.array(y_all)
            
            metrics = trainer.train(X_all, y_all)
            trainer.save_model()
            
            return jsonify({
                'success': True,
                'metrics': metrics,
                'message': f'Model retrained with {len(X_all)} data points'
            })
        else:
            return jsonify({'error': 'Insufficient data for retraining'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

---

### Phase 7: Analytics & Reporting Module (Weeks 15-17)

Create `app/blueprints/analytics.py`:

```python
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from app.models import SaleTransaction, SaleItem, Product, Category, db

bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@bp.before_request
@login_required
def before_request():
    pass

@bp.route('/dashboard')
def dashboard():
    """Main analytics dashboard"""
    # Date range from request
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Calculate metrics
    query = SaleTransaction.query.filter(
        SaleTransaction.created_at >= start_date,
        SaleTransaction.created_at <= end_date
    )
    
    total_revenue = db.session.query(func.sum(SaleTransaction.total_amount)).filter(
        SaleTransaction.created_at >= start_date,
        SaleTransaction.created_at <= end_date
    ).scalar() or 0
    
    total_transactions = query.count()
    average_transaction = total_revenue / total_transactions if total_transactions > 0 else 0
    
    # Top products
    top_products = db.session.query(
        Product.name,
        func.sum(SaleItem.quantity).label('qty_sold'),
        func.sum(SaleItem.subtotal).label('revenue')
    ).join(SaleItem).join(SaleTransaction).filter(
        SaleTransaction.created_at >= start_date,
        SaleTransaction.created_at <= end_date
    ).group_by(Product.id).order_by(desc('revenue')).limit(10).all()
    
    # Daily sales trend
    daily_sales = db.session.query(
        func.date(SaleTransaction.created_at).label('date'),
        func.sum(SaleTransaction.total_amount).label('revenue'),
        func.count(SaleTransaction.id).label('transactions')
    ).filter(
        SaleTransaction.created_at >= start_date,
        SaleTransaction.created_at <= end_date
    ).group_by(func.date(SaleTransaction.created_at)).all()
    
    return render_template('analytics/dashboard.html',
                         total_revenue=total_revenue,
                         total_transactions=total_transactions,
                         average_transaction=average_transaction,
                         top_products=top_products,
                         daily_sales=daily_sales,
                         start_date=start_date,
                         end_date=end_date)

@bp.route('/api/sales-trend')
def get_sales_trend():
    """API endpoint for sales trend data (AJAX)"""
    days = request.args.get('days', 30, type=int)
    start_date = datetime.now() - timedelta(days=days)
    
    data = db.session.query(
        func.date(SaleTransaction.created_at).label('date'),
        func.sum(SaleTransaction.total_amount).label('revenue')
    ).filter(
        SaleTransaction.created_at >= start_date
    ).group_by(func.date(SaleTransaction.created_at)).all()
    
    return jsonify({
        'dates': [str(row.date) for row in data],
        'revenues': [float(row.revenue) for row in data]
    })

@bp.route('/api/top-products')
def get_top_products():
    """API endpoint for top selling products"""
    days = request.args.get('days', 30, type=int)
    start_date = datetime.now() - timedelta(days=days)
    
    data = db.session.query(
        Product.name,
        func.sum(SaleItem.quantity).label('qty'),
        func.sum(SaleItem.subtotal).label('revenue')
    ).join(SaleItem).join(SaleTransaction).filter(
        SaleTransaction.created_at >= start_date
    ).group_by(Product.id).order_by(desc('revenue')).limit(10).all()
    
    return jsonify({
        'products': [row[0] for row in data],
        'quantities': [int(row[1]) for row in data],
        'revenues': [float(row[2]) for row in data]
    })

@bp.route('/api/category-breakdown')
def get_category_breakdown():
    """API endpoint for category sales breakdown"""
    days = request.args.get('days', 30, type=int)
    start_date = datetime.now() - timedelta(days=days)
    
    data = db.session.query(
        Category.name,
        func.sum(SaleItem.subtotal).label('revenue')
    ).join(Product).join(SaleItem).join(SaleTransaction).filter(
        SaleTransaction.created_at >= start_date
    ).group_by(Category.id).all()
    
    return jsonify({
        'categories': [row[0] for row in data],
        'revenues': [float(row[1]) for row in data]
    })
```

---

## Database Schema

```sql
-- Users
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'staff',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories
CREATE TABLE category (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

-- Suppliers
CREATE TABLE supplier (
    id INTEGER PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(120),
    address TEXT,
    average_lead_time_days INTEGER DEFAULT 7,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products
CREATE TABLE product (
    id INTEGER PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    sku VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    category_id INTEGER NOT NULL,
    supplier_id INTEGER,
    unit_price FLOAT NOT NULL,
    reorder_level INTEGER DEFAULT 10,
    reorder_quantity INTEGER DEFAULT 50,
    current_stock INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (supplier_id) REFERENCES supplier(id)
);

-- Stock Transactions
CREATE TABLE stock_transaction (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_cost FLOAT,
    reference VARCHAR(100),
    notes TEXT,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    CHECK (quantity >= 0)
);

-- Sale Transactions
CREATE TABLE sale_transaction (
    id INTEGER PRIMARY KEY,
    receipt_number VARCHAR(50) UNIQUE NOT NULL,
    total_amount FLOAT NOT NULL,
    notes TEXT,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Sale Items
CREATE TABLE sale_item (
    id INTEGER PRIMARY KEY,
    sale_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price FLOAT NOT NULL,
    subtotal FLOAT NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES sale_transaction(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);

-- Prediction Log
CREATE TABLE prediction_log (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    prediction_date DATE NOT NULL,
    predicted_qty_7d FLOAT NOT NULL,
    predicted_qty_30d FLOAT NOT NULL,
    confidence_score FLOAT,
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product(id),
    UNIQUE (product_id, prediction_date, model_version)
);

-- Alerts
CREATE TABLE alert_log (
    id INTEGER PRIMARY KEY,
    alert_type VARCHAR(50) NOT NULL,
    product_id INTEGER,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    is_resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product(id)
);
```

---

## API Endpoints

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| **Auth** | | | |
| POST | `/auth/login` | User login | No |
| POST | `/auth/logout` | User logout | Yes |
| POST | `/auth/register` | Create new user (admin only) | Yes |
| **Inventory** | | | |
| GET | `/inventory/` | Dashboard | Yes |
| GET | `/inventory/products` | List products | Yes |
| POST | `/inventory/products/create` | Create product | Yes (Admin) |
| POST | `/inventory/stock-in` | Record stock receipt | Yes |
| GET | `/inventory/api/products/<id>` | Get product details (JSON) | Yes |
| GET | `/inventory/api/low-stock-alerts` | Get low stock items (JSON) | Yes |
| **Sales** | | | |
| GET | `/sales/new` | POS interface | Yes |
| POST | `/sales/new` | Process sale | Yes |
| GET | `/sales/history` | Sales history | Yes |
| GET | `/sales/receipt/<receipt_no>` | View receipt | Yes |
| GET | `/sales/api/sales-summary` | Sales summary (JSON) | Yes |
| **Analytics** | | | |
| GET | `/analytics/dashboard` | Analytics dashboard | Yes |
| GET | `/analytics/api/sales-trend` | Sales trend (JSON) | Yes |
| GET | `/analytics/api/top-products` | Top products (JSON) | Yes |
| GET | `/analytics/api/category-breakdown` | Category breakdown (JSON) | Yes |
| **Predictions** | | | |
| GET | `/predictions/forecast` | Demand forecast | Yes |
| GET | `/predictions/recommendations` | Reorder recommendations | Yes |
| GET | `/predictions/product/<id>` | Product-specific forecast | Yes |
| POST | `/predictions/api/retrain` | Retrain model | Yes (Admin) |

---

## Testing Strategy

### Unit Tests
```bash
pytest tests/test_models.py       # Database model tests
pytest tests/test_ml.py            # ML pipeline tests
pytest tests/test_inventory.py     # Inventory logic
pytest tests/test_sales.py         # Sales logic
```

### Integration Tests
```bash
pytest tests/test_integration.py   # End-to-end workflows
```

### Run All Tests with Coverage
```bash
pytest --cov=app tests/
```

---

## Deployment Guide

### Production Setup

#### 1. Environment Variables (.env)
```bash
FLASK_ENV=production
SECRET_KEY=your-production-secret-key-change-this
DATABASE_URL=postgresql://user:password@localhost/sme_analytics_prod
LOG_LEVEL=INFO
```

#### 2. PostgreSQL Database
```bash
createdb sme_analytics_prod
psql sme_analytics_prod < docs/database_schema.sql
```

#### 3. Application Server (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:8000 --timeout 120 run:app
```

#### 4. Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name sme-analytics.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/app/static/;
        expires 30d;
    }
}
```

#### 5. Automated Model Retraining (Cron)
```bash
0 2 * * 0 /usr/bin/python /path/to/scripts/train_model.py
```

---

## Next Steps

1. **Clone the repository** and set up the development environment
2. **Install dependencies** from requirements.txt
3. **Initialize the database** with `python scripts/init_db.py`
4. **Run the application** with `python run.py`
5. **Access the system** at `http://localhost:5000`
6. **Login** with default credentials (admin/admin123)
7. **Create sample data** and test each module
8. **Implement remaining templates** and refine UI/UX
9. **Deploy to production** following the deployment guide

---

**Good luck with your project!** This is a comprehensive system that aligns with your thesis. Proceed methodically through each phase, test thoroughly, and iterate based on user feedback.

