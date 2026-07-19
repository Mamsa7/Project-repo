from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional, NumberRange
from app.models import User

class LoginForm(FlaskForm):
    """User login form"""
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    """User registration form (admin only)"""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('staff', 'Sales Staff'), ('admin', 'Administrator')])
    submit = SubmitField('Create User')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken.')

class ProductForm(FlaskForm):
    """Product creation/edit form"""
    name = StringField('Product Name', validators=[DataRequired()])
    sku = StringField('SKU', validators=[DataRequired()])
    description = TextAreaField('Description')
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    supplier_id = SelectField('Supplier', coerce=int, validators=[Optional()])
    unit_price = FloatField('Unit Price', validators=[DataRequired(), NumberRange(min=0)])
    reorder_level = IntegerField('Reorder Level', validators=[DataRequired(), NumberRange(min=0)])
    reorder_quantity = IntegerField('Reorder Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Save Product')

class CategoryForm(FlaskForm):
    """Category creation/edit form"""
    name = StringField('Category Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Save Category')

class SupplierForm(FlaskForm):
    """Supplier creation/edit form"""
    name = StringField('Supplier Name', validators=[DataRequired()])
    contact_person = StringField('Contact Person')
    phone = StringField('Phone')
    email = StringField('Email', validators=[Optional(), Email()])
    address = TextAreaField('Address')
    average_lead_time_days = IntegerField('Average Lead Time (Days)', 
                                         validators=[DataRequired(), NumberRange(min=1)],
                                         default=7)
    submit = SubmitField('Save Supplier')

class StockInForm(FlaskForm):
    """Stock receipt form"""
    product_id = SelectField('Product', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    unit_cost = FloatField('Unit Cost', validators=[DataRequired(), NumberRange(min=0)])
    reference = StringField('Reference (PO Number)', validators=[Optional()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Record Stock In')

class SaleItemForm(FlaskForm):
    """Individual sale item form"""
    product_id = SelectField('Product', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    unit_price = FloatField('Unit Price', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add to Sale')

class DateRangeForm(FlaskForm):
    """Date range selection for reports"""
    start_date = StringField('Start Date', validators=[DataRequired()], render_kw={"type": "date"})
    end_date = StringField('End Date', validators=[DataRequired()], render_kw={"type": "date"})
    submit = SubmitField('Filter')