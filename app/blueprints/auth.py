from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from app.models import User
from app.forms import LoginForm, RegistrationForm
from app.utils import admin_required

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
    """User login"""
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
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
@login_required
@admin_required
def register():
    """Create new user (admin only)"""
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash(f'User {user.username} created successfully!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

def url_has_no_scheme(url):
    """Check if URL is safe for redirect"""
    return url.startswith('/')
