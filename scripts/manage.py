"""Database initialization and management commands"""
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from app import create_app, db
from app.models import User, Product, Category, Supplier
import click

app = create_app('development')

@app.cli.command()
def create_db():
    """Create database tables"""
    db.create_all()
    print('Database tables created.')

@app.cli.command()
def drop_db():
    """Drop all database tables"""
    if click.confirm('Are you sure you want to drop all tables?'):
        db.drop_all()
        print('Database tables dropped.')

@app.cli.command()
@click.argument('username')
@click.argument('password')
@click.option('--email', default='', help='User email')
@click.option('--admin', is_flag=True, help='Create admin user')
def create_user(username, password, email, admin):
    """Create a new user"""
    if User.query.filter_by(username=username).first():
        print(f'User {username} already exists.')
        return
    
    user = User(
        username=username,
        email=email or None,
        role='admin' if admin else 'staff'
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    role_desc = 'Admin' if admin else 'Staff'
    print(f'{role_desc} user {username} created successfully.')

@app.cli.command()
def seed_data():
    """Seed database with sample data"""
    from scripts.init_db import init_database
    init_database()

if __name__ == '__main__':
    app.cli()
