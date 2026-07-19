"""Unit tests for database models"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app, db
from app.models import User, Product, Category, Supplier, SaleTransaction, SaleItem
import unittest

class ModelTestCase(unittest.TestCase):
    """Test database models"""
    
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_user_password_hashing(self):
        """Test user password hashing"""
        user = User(username='testuser')
        user.set_password('testpass123')
        self.assertFalse(user.check_password('wrongpass'))
        self.assertTrue(user.check_password('testpass123'))
    
    def test_product_creation(self):
        """Test product creation"""
        category = Category(name='Test Category')
        db.session.add(category)
        db.session.commit()
        
        product = Product(
            name='Test Product',
            sku='TEST001',
            category_id=category.id,
            unit_price=100.0
        )
        db.session.add(product)
        db.session.commit()
        
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.sku, 'TEST001')
        self.assertEqual(product.unit_price, 100.0)
    
    def test_product_low_stock_check(self):
        """Test low stock check"""
        category = Category(name='Test')
        product = Product(
            name='Test',
            sku='T001',
            category_id=1,
            unit_price=50.0,
            current_stock=5,
            reorder_level=10
        )
        db.session.add(category)
        db.session.add(product)
        db.session.commit()
        
        self.assertTrue(product.is_low_stock())
    
    def test_sale_transaction(self):
        """Test sale transaction creation"""
        user = User(username='testuser', role='staff')
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()
        
        sale = SaleTransaction(
            receipt_number='RCP-001',
            total_amount=100.0,
            user_id=user.id
        )
        db.session.add(sale)
        db.session.commit()
        
        self.assertEqual(sale.receipt_number, 'RCP-001')
        self.assertEqual(sale.total_amount, 100.0)

if __name__ == '__main__':
    unittest.main()
