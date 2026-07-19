# Quick Reference Guide

## Installation (5 minutes)

```bash
git clone https://github.com/Mamsa7/Project-repo.git
cd Project-repo
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts/init_db.py
python run.py
```

**Access**: http://localhost:5000  
**Login**: admin / admin123

---

## File Organization

| Directory | Purpose |
|-----------|----------|
| `app/` | Main application code |
| `app/blueprints/` | Feature modules (auth, inventory, sales, analytics, predictions) |
| `app/ml/` | Machine learning pipeline |
| `app/templates/` | HTML templates (to create) |
| `app/static/` | CSS, JS, images (to create) |
| `scripts/` | Initialization and utility scripts |
| `tests/` | Unit and integration tests |
| `migrations/` | Database migrations (Alembic) |

---

## Key Components

### Database Models (8)
```python
- User (authentication)
- Product (inventory)
- Category (product classification)
- Supplier (vendor management)
- StockTransaction (inventory movements)
- SaleTransaction (invoice headers)
- SaleItem (sale line items)
- PredictionLog (ML forecasts)
- AlertLog (system notifications)
```

### Blueprints (5)
```python
auth.py          # Login, logout, registration
inventory.py    # Product, category, supplier, stock management
sales.py        # POS, sale transactions, receipts
analytics.py    # Dashboards, reports, metrics
predictions.py  # Demand forecasting, recommendations
```

### ML Components (3)
```python
feature_engineering.py  # Extract features from sales data
model_training.py       # Train RF and GB models
model_serving.py        # Generate predictions and recommendations
```

---

## Common Commands

### Development
```bash
# Start development server
python run.py

# Run tests
pytest

# Run tests with coverage
pytest --cov=app

# Create database
flask db init && flask db migrate && flask db upgrade

# Create admin user
flask create-user admin password --admin
```

### Production
```bash
# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app

# Collect logs
grep ERROR logs/sme_analytics.log
```

---

## API Quick Reference

### Authentication
```http
POST /auth/login
POST /auth/logout
POST /auth/register
```

### Inventory (6 endpoints)
```http
GET /inventory/
GET /inventory/products
POST /inventory/products/create
POST /inventory/stock-in
GET /inventory/api/products/<id>
GET /inventory/api/low-stock-alerts
```

### Sales (5 endpoints)
```http
GET /sales/new
POST /sales/new
GET /sales/history
GET /sales/receipt/<receipt_no>
GET /sales/api/sales-summary
```

### Analytics (4 endpoints)
```http
GET /analytics/dashboard
GET /analytics/api/sales-trend
GET /analytics/api/top-products
GET /analytics/api/category-breakdown
```

### Predictions (3 endpoints)
```http
GET /predictions/forecast
GET /predictions/recommendations
POST /predictions/api/retrain
```

---

## Database Quick Reference

### Create Product
```sql
INSERT INTO product (name, sku, category_id, unit_price, reorder_level)
VALUES ('Product Name', 'SKU001', 1, 100.0, 10);
```

### Record Stock In
```sql
INSERT INTO stock_transaction (product_id, transaction_type, quantity, user_id)
VALUES (1, 'stock_in', 50, 1);

UPDATE product SET current_stock = current_stock + 50 WHERE id = 1;
```

### Record Sale
```sql
INSERT INTO sale_transaction (receipt_number, total_amount, user_id)
VALUES ('RCP-20260719-ABC123', 150.0, 1);

INSERT INTO sale_item (sale_id, product_id, quantity, unit_price, subtotal)
VALUES (1, 1, 2, 75.0, 150.0);

UPDATE product SET current_stock = current_stock - 2 WHERE id = 1;
```

---

## Environment Variables

```bash
FLASK_ENV=development          # development/production/testing
SECRET_KEY=your-secret-key    # Change in production!
DEV_DATABASE_URL=sqlite:///sme_analytics_dev.db
DATABASE_URL=postgresql://...  # Production database
LOG_LEVEL=INFO                 # DEBUG, INFO, WARNING, ERROR
```

---

## Troubleshooting

### Database Connection Failed
```bash
# Check database URL in .env
echo $DATABASE_URL

# Test PostgreSQL connection
psql -U postgres -h localhost
```

### Import Errors
```bash
# Ensure virtual environment activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use
```bash
# Run on different port
python run.py --host=0.0.0.0 --port=5001
```

### Model Training Error
```bash
# Check if sufficient data exists
SELECT COUNT(*) FROM sale_item WHERE product_id = 1;

# Retrain model
flask retrain-models
```

---

## Performance Tips

1. **Database Indexing**: Add indexes to frequently queried columns
   ```sql
   CREATE INDEX idx_product_sku ON product(sku);
   CREATE INDEX idx_sale_date ON sale_transaction(created_at);
   ```

2. **Caching**: Use Redis for session and query caching
   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'redis'})
   ```

3. **Query Optimization**: Use eager loading for relationships
   ```python
   products = Product.query.options(joinedload(Product.category)).all()
   ```

4. **ML Model Caching**: Keep trained models in memory
   ```python
   self.model = joblib.load(model_path)
   # Model loaded once at startup
   ```

---

## Security Checklist

- [ ] Change default admin password in production
- [ ] Set strong SECRET_KEY (use `secrets.token_urlsafe()`)
- [ ] Enable HTTPS/SSL in production
- [ ] Configure CORS if needed
- [ ] Enable SQL escaping (SQLAlchemy ORM handles this)
- [ ] Validate all user inputs
- [ ] Use environment variables for secrets
- [ ] Implement rate limiting on login endpoint
- [ ] Enable security headers in Nginx
- [ ] Set up automated backups

---

## Learning Resources

### Documentation
- `PROJECT_IMPLEMENTATION_GUIDE.md` - 65+ pages
- `README.md` - Quick start
- `PROJECT_SUMMARY.md` - Project overview
- Flask documentation: https://flask.palletsprojects.com/
- SQLAlchemy docs: https://docs.sqlalchemy.org/
- scikit-learn: https://scikit-learn.org/

### Key Files to Review
1. `app/models.py` - Database structure
2. `app/blueprints/inventory.py` - Feature implementation
3. `app/ml/feature_engineering.py` - ML pipeline
4. `config.py` - Configuration management
5. `run.py` - Application entry point

---

## Next Steps

1. **Complete Frontend** (Phase 8)
   - Create HTML templates
   - Add CSS styling
   - Implement JavaScript interactions

2. **Add Tests** (Phase 9)
   - Unit tests for all modules
   - Integration tests
   - Performance tests

3. **Deploy** (Phase 11-12)
   - Set up production environment
   - Configure PostgreSQL
   - Deploy with Gunicorn + Nginx
   - Enable HTTPS

4. **Monitor** (Post-Launch)
   - Set up monitoring dashboard
   - Configure alerts
   - Track performance metrics
   - Gather user feedback

---

*Quick Reference v1.0 - July 2026*
