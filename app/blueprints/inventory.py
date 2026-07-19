from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import desc
from app import db
from app.models import Product, Category, Supplier, StockTransaction, AlertLog
from app.utils import admin_required
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
    
    # Active alerts
    active_alerts = AlertLog.query.filter_by(is_resolved=False).order_by(desc(AlertLog.created_at)).limit(5).all()
    
    return render_template('inventory/dashboard.html',
                         total_products=total_products,
                         low_stock_items=low_stock_items,
                         total_stock_value=total_stock_value,
                         recent_transactions=recent_transactions,
                         active_alerts=active_alerts)

@bp.route('/products')
def products():
    """Product listing with search and pagination"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category_id = request.args.get('category_id', type=int)
    
    query = Product.query
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%') | Product.sku.ilike(f'%{search}%'))
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    products = query.paginate(page=page, per_page=20)
    categories = Category.query.all()
    
    return render_template('inventory/products.html',
                         products=products,
                         categories=categories,
                         search=search,
                         category_id=category_id)

@bp.route('/products/create', methods=['GET', 'POST'])
@admin_required
def create_product():
    """Create new product"""
    if request.method == 'POST':
        try:
            # Check SKU uniqueness
            if Product.query.filter_by(sku=request.form.get('sku')).first():
                flash('SKU already exists.', 'danger')
                return redirect(url_for('inventory.create_product'))
            
            product = Product(
                name=request.form.get('name'),
                sku=request.form.get('sku'),
                description=request.form.get('description'),
                category_id=request.form.get('category_id', type=int),
                supplier_id=request.form.get('supplier_id', type=int) or None,
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
            reference = request.form.get('reference')
            
            if quantity <= 0:
                flash('Quantity must be greater than 0.', 'danger')
                return redirect(url_for('inventory.stock_in'))
            
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
            
            flash(f'Stock receipt recorded: +{quantity} units of {product.name}', 'success')
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
        'category': product.category.name if product.category else None,
        'is_low_stock': product.is_low_stock()
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

@bp.route('/categories', methods=['GET', 'POST'])
@admin_required
def categories():
    """Manage product categories"""
    if request.method == 'POST':
        try:
            category = Category(
                name=request.form.get('name'),
                description=request.form.get('description')
            )
            db.session.add(category)
            db.session.commit()
            flash(f'Category {category.name} created successfully!', 'success')
            return redirect(url_for('inventory.categories'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating category: {str(e)}', 'danger')
    
    categories = Category.query.all()
    return render_template('inventory/categories.html', categories=categories)

@bp.route('/suppliers', methods=['GET', 'POST'])
@admin_required
def suppliers():
    """Manage suppliers"""
    if request.method == 'POST':
        try:
            supplier = Supplier(
                name=request.form.get('name'),
                contact_person=request.form.get('contact_person'),
                phone=request.form.get('phone'),
                email=request.form.get('email'),
                address=request.form.get('address'),
                average_lead_time_days=request.form.get('average_lead_time_days', type=int, default=7)
            )
            db.session.add(supplier)
            db.session.commit()
            flash(f'Supplier {supplier.name} created successfully!', 'success')
            return redirect(url_for('inventory.suppliers'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating supplier: {str(e)}', 'danger')
    
    suppliers = Supplier.query.all()
    return render_template('inventory/suppliers.html', suppliers=suppliers)
