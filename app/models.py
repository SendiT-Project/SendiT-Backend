
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask_bcrypt import Bcrypt 
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-orders.user',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String,nullable=False, unique=True)
    email = db.Column(db.String, unique=True,nullable=False )
    _password_hash = db.Column(db.String, nullable=False)
    
    @validates("email")
    def validate_email(self, key, email):
        if "@" not in email:
            raise ValueError("email must contain @")

    #relationship
    orders = db.relationship('Order', backref='user',)

    @hybrid_property
    def password_hash(self):
        raise AttributeError("password hash cannot be veiwed")
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8')
        )
        self._password_hash = password_hash.decode('utf-8')
    
    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8')
        )



class Admin(db.Model, SerializerMixin):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    
    @hybrid_property
    def password_hash(self):
        raise AttributeError("password hash cannot be veiwed")
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8')
        )
        self._password_hash = password_hash.decode('utf-8')
    
    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8')
        )

    
class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'  

    serialize_rules = ('-user.orders',)

    order_number = db.Column(db.Integer, primary_key=True)
    name_of_parcel = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    current_location = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default='pending')
    pickup = db.Column(db.String, default='Pick from office')
    weight = db.Column(db.String, nullable=True)

     #relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

