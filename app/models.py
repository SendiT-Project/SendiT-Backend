
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()
# models added
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-orders.user','-trackers.user',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    role=db.Column(db.String, default='user')

    #relationship
    orders = db.relationship('Order', backref='user')
    trackers = db.relationship('Tracking', backref='user')

class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'  

    serialize_rules = ('-users.order','-trackers.order',)

    order_number = db.Column(db.Integer, primary_key=True)
    name_of_parcel = db.Column(db.String)
    destination = db.Column(db.String)
    pickup = db.Column(db.String)
    weight = db.Column(db.String)

     #relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    trackers = db.relationship('Tracking', backref='order')

class Tracking(db.Model, SerializerMixin):

    __tablename__ = 'trackers'

    serialize_rules =('-orders.tracker','-users.tracker',)

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, default='pending')

    #relationship
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_number'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    






 


