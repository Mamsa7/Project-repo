# Test Configuration
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app, db

app = create_app('testing')

with app.app_context():
    db.create_all()
