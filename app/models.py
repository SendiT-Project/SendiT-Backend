from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-orders.user','-trackers.user',)
    role=db.Column(db.String, default='user')
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    orders = db.relationship('Orders', backref='user')
    trackers = db.relationship('Trackeing', backref='user')
    


class Orders(db.Model, SerializerMixin):
    __tablename__ = 'orders'  
    serialize_rules = ('-users.order','-trackers.order',)
    order_number = db.Column(db.Integer, primary_key=True)
    name_of_parcel = db.Column(db.String)
    destination = db.Column(db.String)
    pickup = db.Column(db.String)
    weight = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    trackers = db.relationship('Tracking', backref='order')

class Tracking(db.Model, SerializerMixin):

    __tablename__ = 'trackers'
    serialize_rules =('-orders.tracker','-users.tracker',)
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_number'))
    status = db.Column(db.String, default='pending')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
# class Admin(db.Model, SerializerMixin):
#     __tablename__ = 'admins'
#     serialize_rules = ('-users.admin')
#     id = db.Column(db.Integer, primary_key=True)
#     admin_name = db.Column(db.String)
#     admin_email = db.Column(db.String)
#     password = db.Column(db.String)
#     users = db.relationship('User', backref='admin')
