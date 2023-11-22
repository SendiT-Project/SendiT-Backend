from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    name_of_parcel = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    pickup = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum('pending', 'delivered'), default='pending')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('orders', lazy=True))

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=128)])
    role = StringField('Role', default='user')  


class OrderForm(FlaskForm):
    order_number = StringField('Order Number', validators=[DataRequired(), Length(min=1, max=20)])
    name_of_parcel = StringField('Parcel Name', validators=[DataRequired(), Length(min=1, max=100)])
    destination = StringField('Destination', validators=[DataRequired(), Length(min=1, max=100)])
    pickup = StringField('Pickup Location', validators=[DataRequired(), Length(min=1, max=100)])
    status = SelectField('Status', choices=[('pending', 'Pending'), ('delivered', 'Delivered')], default='pending')
    user_id = StringField('User ID', validators=[DataRequired()])




