from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__= 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    orders = db.relationship('Orders', backref='user')




class Orders(db.Model, SerializerMixin):
    __tablename__= 'users'
    Order_number = db.Column(db.Integer,primary_key=True)
    name_of_parcel = db.Column(db.String)
    destination = db.Column(db.String)
    pickup = db.Column(db.String)
    status = db.Column(db.String, default='Pending')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


