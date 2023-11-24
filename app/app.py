
from flask import Flask, make_response, jsonify, session, request
from flask_restful import Api, Resource
from flask_migrate import Migrate
from models import db, User,Order
# import os
# from dotenv import load_dotenv

# load_dotenv()

app = Flask(__name__)
app.secret_key =  "@dkfi2o1p49978vkdn5k5768iknhnlpo"
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///app.db"
app.config["SQLACHEMY_TRACK_MODIFICATIONS"]=False

migrate = Migrate(app,db)
db.init_app(app)

api = Api(app)

@app.before_request
def check_if_logged_in():
    if not session["user_id"]\
    and request.endpoint != "login" and request.endpoint != "signup":
        return {"error": "unauthorized"}, 401

class CheckSession(Resource):
    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id==session['user_id']).first()
            return user.to_dict(), 200
        
        return {'error': 'Resource unavailable'}
    
api.add_resource(CheckSession, "/session", endpoint="session")

class Index(Resource):
    def get(self):
        response_body = "<h1>Hello, World</h1>"
        status =200
        headers ={}
        return make_response(response_body, status, headers)
api.add_resource(Index, "/")


class Signup(Resource):
    def post(self):
        name = request.get_json().get("name")
        password = request.get_json().get("password")

        if name and password:
            new_user = User(name=name)
            new_user.password_hash = password

            db.session.add(new_user)
            db.session.commit()

            session["user_id"] = new_user.id
            return new_user.to_dict(), 201
        
        return {"error": "user details must be added"}, 422
        
api.add_resource(Signup, "/signup", endpoint="signup")

class Login(Resource):
    def post(self):
        name = request.get_json().get("name")
        password = request.get_json().get("password")
        user = User.query.filter(User.name==name).first()

        if user and user.authenticate(password):
            session["user_id"] = user.id

            return user.to_dict(), 200
        else:
            return {'error': 'user or password id not correct!'}, 401
        
api.add_resource(Login, "/login", endpoint="login")

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id'] = None
            return {'info': 'user logged out successfully'}
        else:
            return {'error': 'unauthorized'}, 401
        
api.add_resource(Logout, "/logout", endpoint="logout")


if __name__ == '__main__':
    app.run(debug=True)

