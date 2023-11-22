# app.py
from flask import Flask, render_template, redirect, url_for, flash, jsonify, request, make_response
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' 
app.config['SECRET_KEY'] = 'your_secret_key_here'
db.init_app(app)
bcrypt = Bcrypt(app)
api = Api(app)
migrate = Migrate(app, db)

# User Resource
class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        response_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
        return make_response(jsonify(response_data), 200)


if __name__ == '__main__':
    app.run(debug=True)
