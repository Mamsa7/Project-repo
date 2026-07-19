from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import desc, func
from app import db
from app.models import Product, SaleTransaction, SaleItem, AlertLog
from datetime import datetime, timedelta
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
                
                quantity = int(item_data['quantity'])
                unit_price = float(item_data['unit_price'])
                subtotal = quantity * unit_price
                
                # Check stock
                if product.current_stock < quantity:
                    db.session.rollback()
                    return jsonify({'error': f'Insufficient stock for {product.name}'}), 400
                
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
        'today': round(today_sales, 2),
        'week': round(week_sales, 2),
        'month': round(month_sales, 2)
    })
