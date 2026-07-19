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
        print("\n=== System Ready ===")
        print("Access the application at: http://localhost:5000")
        print("Default credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\n⚠️  Change the admin password immediately in production!")

if __name__ == '__main__':
    init_database()
