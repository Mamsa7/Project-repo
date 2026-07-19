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
    
    return render_template('analytics/dashboard.html',
                         total_revenue=round(total_revenue, 2),
                         total_transactions=total_transactions,
                         average_transaction=round(average_transaction, 2),
                         top_products=top_products,
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
        'revenues': [round(float(row.revenue), 2) for row in data]
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
        'revenues': [round(float(row[2]), 2) for row in data]
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
        'revenues': [round(float(row[1]), 2) for row in data]
    })
