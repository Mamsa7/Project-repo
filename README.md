# SME Integrated Inventory and Sales Analytics with Decision Support System

## Project Overview

This is a comprehensive web-based system designed to help Small and Medium Enterprises (SMEs) manage inventory, track sales, and make data-driven decisions using machine learning-based demand forecasting.

### Key Features

✅ **Real-time Inventory Management**
- Track product stock levels
- Automated low-stock alerts
- Stock-in/out transaction recording
- Multi-supplier support

✅ **Sales Transaction Management**
- Point-of-Sale (POS) interface
- Receipt generation
- Sales history tracking
- Transaction reporting

✅ **Advanced Analytics Dashboards**
- Real-time sales metrics
- Product performance analysis
- Revenue trends and forecasts
- Category-wise breakdown

✅ **Machine Learning Decision Support**
- Sales demand forecasting (7-day and 30-day)
- Automated reorder recommendations
- Inventory optimization suggestions
- Predictive analytics with explainability

✅ **User Management**
- Role-based access control (Admin/Sales Staff)
- Secure authentication
- Activity logging

## Technology Stack

- **Backend**: Python 3.11 + Flask 3.0
- **Database**: PostgreSQL (production) / SQLite (development)
- **ORM**: SQLAlchemy 2.0
- **Machine Learning**: scikit-learn 1.4
- **Frontend**: HTML5 + Bootstrap 5 + Chart.js
- **Authentication**: Flask-Login + Werkzeug

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+ (for production)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Mamsa7/Project-repo.git
cd Project-repo
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Initialize database**
```bash
flask db init
flask db migrate
flask db upgrade
python scripts/init_db.py
```

6. **Run the application**
```bash
python run.py
```

Access the system at `http://localhost:5000`

**Default credentials**:
- Username: `admin`
- Password: `admin123` (⚠️ Change immediately in production)

## Project Structure

```
Project-repo/
├── app/
│   ├── blueprints/          # Flask blueprints (modules)
│   │   ├── auth.py
│   │   ├── inventory.py
│   │   ├── sales.py
│   │   ├── analytics.py
│   │   └── predictions.py
│   ├── ml/                  # Machine learning pipeline
│   │   ├── feature_engineering.py
│   │   ├── model_training.py
│   │   ├── model_serving.py
│   │   └── models/
│   ├── templates/           # HTML templates
│   ├── static/              # CSS, JS, images
│   ├── models.py            # Database models
│   ├── forms.py             # WTForms
│   ├── utils.py             # Utility functions
│   └── __init__.py          # App factory
├── scripts/                 # Setup and utility scripts
├── tests/                   # Test suite
├── migrations/              # Database migrations
├── config.py                # Configuration
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── README.md
```

## Documentation

See the [PROJECT_IMPLEMENTATION_GUIDE.md](PROJECT_IMPLEMENTATION_GUIDE.md) for detailed implementation instructions.

## Key Modules

### 1. Authentication (`auth.py`)
- User login/logout
- Admin user registration
- Session management
- Password security

### 2. Inventory (`inventory.py`)
- Product CRUD operations
- Stock transaction recording
- Real-time stock level tracking
- Low-stock alerting

### 3. Sales (`sales.py`)
- Point-of-Sale interface
- Sale transaction processing
- Receipt generation
- Sales history

### 4. Analytics (`analytics.py`)
- Sales dashboard
- Product performance metrics
- Revenue trends
- Category analysis

### 5. Predictions (`predictions.py`)
- Demand forecasting
- Reorder recommendations
- Model training/retraining
- Forecast accuracy metrics

### 6. Machine Learning (`ml/`)
- Feature engineering from sales data
- Random Forest & Gradient Boosting models
- Sales prediction pipeline
- Model persistence and serving

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `POST /auth/register` - Create new user (admin only)

### Inventory
- `GET /inventory/` - Dashboard
- `GET /inventory/products` - List products
- `POST /inventory/products/create` - Create product
- `POST /inventory/stock-in` - Record stock receipt
- `GET /inventory/api/low-stock-alerts` - Get alerts (JSON)

### Sales
- `GET /sales/new` - POS interface
- `POST /sales/new` - Process sale
- `GET /sales/history` - Sales history
- `GET /sales/receipt/<receipt_no>` - View receipt

### Analytics
- `GET /analytics/dashboard` - Analytics dashboard
- `GET /analytics/api/sales-trend` - Sales trend (JSON)
- `GET /analytics/api/top-products` - Top products (JSON)

### Predictions
- `GET /predictions/forecast` - Demand forecast
- `GET /predictions/recommendations` - Reorder recommendations
- `POST /predictions/api/retrain` - Retrain model (admin)

## Machine Learning Model

### Algorithm
- **Primary**: Random Forest Regressor
- **Secondary**: Gradient Boosting Regressor
- **Performance**: R² > 0.94 on test data

### Features
- Temporal features (day of week, month, quarter, holidays)
- Lag features (1, 7, 14, 30 days)
- Rolling window statistics (7-day, 30-day mean/std)

### Retraining
- Automatic retraining: Weekly (configurable)
- Minimum data points required: 50
- Cross-validation: 5-fold

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_models.py
```

## Deployment

### Production Deployment

1. **Set environment variables**
```bash
export FLASK_ENV=production
export SECRET_KEY=your-production-secret
export DATABASE_URL=postgresql://user:pass@host/db
```

2. **Run with Gunicorn**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

3. **Configure Nginx reverse proxy**
See [PROJECT_IMPLEMENTATION_GUIDE.md](PROJECT_IMPLEMENTATION_GUIDE.md#deployment-guide)

4. **Enable HTTPS**
- Use Let's Encrypt with Certbot
- Configure SSL in Nginx

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Submit pull request

## License

This project is part of a thesis submission at Federal University Dutse.

## Author

**Umar Bala Abdulmumin** (FCP/CIT/22/1033)  
Department of Information Technology  
Federal University Dutse, Nigeria

## Supervisor

**Mal. A.H Galadima**  
Federal University Dutse

## Support

For issues or questions, please refer to the [PROJECT_IMPLEMENTATION_GUIDE.md](PROJECT_IMPLEMENTATION_GUIDE.md)

---

**Last Updated**: July 2026