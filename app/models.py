
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask_bcrypt import Bcrypt 
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()
bcrypt = Bcrypt()

# we need to review Tracker/Order relationship
#User ----Order ---One user many orders


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-orders.user',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    _password_hash = db.Column(db.String)
    

    #relationship
    orders = db.relationship('Order', backref='user')

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
            self.password_hash, password.encode('utf-8')
        )
    


class Admin(db.Model, SerializerMixin):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    _password_hash = db.Column(db.String)




class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'  

    serialize_rules = ('-user.orders',)

    order_number = db.Column(db.Integer, primary_key=True)
    name_of_parcel = db.Column(db.String)
    destination = db.Column(db.String)
    current_location = db.Column(db.String)
    status = db.Column(db.String, default='pending')
    pickup = db.Column(db.String)
    weight = db.Column(db.String)

     #relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

