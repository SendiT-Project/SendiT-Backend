
from flask import Flask, make_response, jsonify, session, request
from flask_restful import Api, Resource
from flask_migrate import Migrate
from models import db, User,Order
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"]= os.environ["DATABASE_URI"]
app.config["SQLACHEMY_TRACK_MODIFICATIONS"]=False

migrate = Migrate(app,db)
db.init_app(app)

api = Api(app)

@app.before_request
def check_if_logged_in():

    if 'user_id' not in session and request.endpoint not in ["login", "signup","index"]:
        return {"error": "unauthorized"}, 401

class CheckSession(Resource):
    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id==session['user_id']).first()
            return user.to_dict(), 200
        
        return {'error': 'Resource unavailable'}
    

class Index(Resource):
    def get(self):
        response_body = "<h1>Hello, World</h1>"
        status =200
        headers ={}
        return make_response(response_body, status, headers)


class Signup(Resource):
    def post(self):
        username = request.get_json().get("username")
        email = request.get_json().get("email")
        password = request.get_json().get("password")

        if username and email and password:
            new_user = User(username=username, email=email)
            new_user.password_hash = password

            db.session.add(new_user)
            db.session.commit()

            session["user_id"] = new_user.id
            return new_user.to_dict(), 201
        
        return {"error": "user details must be added"}, 422
        

class Login(Resource):
    def post(self):
        username = request.get_json().get("username")
        password = request.get_json().get("password")
        user = User.query.filter(User.username==username).first()

        if user:
            if user.authenticate(password):
                session['user_id'] = user.id

                user_dict = user.to_dict()
                print("Login successful. user ID:", user.id)  
                return make_response(jsonify(user_dict), 201)
            else:
                print("Invalid password.")  
                return {"error": "Invalid password"}, 401
        
        print("Customer not registered.") 
        return {"error": "User not Registered"}, 404
        

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id'] = None
            return {'info': 'user logged out successfully'}
        else:
            return {'error': 'unauthorized'}, 401
        

api.add_resource(CheckSession, "/session", endpoint="session")
api.add_resource(Index, "/", endpoint="index") 
api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(Login, "/login", endpoint="login")       
api.add_resource(Logout, "/logout", endpoint="logout")


application = app

if __name__ == '__main__':
    app.run(debug=True)

