
from flask import Flask, make_response, jsonify, session, request
from flask_restful import Api, Resource
from flask_migrate import Migrate
from models import db, User,Order, Admin
import os
from dotenv import load_dotenv

load_dotenv()

# testing
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
        
        print("User not registered.") 
        return {"error": "User not Registered"}, 404
    

    # Order routes
    

class Orders(Resource):
    def get(self,order_number=None):#the none will make getting by order_number optional
        if order_number:
            orders = Order.query.get(order_number)
            if orders:
                return orders.to_dict(), 200
            else:
                return {"error": "order not found"}, 400
        else:
            orders = [n.to_dict() for n in Order.query.all()]
            response = make_response(jsonify(orders), 200)
            return response
   
        
    
    def post(self):
        name_of_parcel = request.get_json().get('name_of_parcel')
        destination = request.get_json().get('destination')
        current_location = request.get_json().get('current_location')
        pickup = request.get_json().get('pickup')
        weight = request.get_json().get('weight')

        new_order = Order(
            name_of_parcel=name_of_parcel,
            destination=destination,
            current_location=current_location,
            pickup=pickup,
            weight=weight,
        )
        user_id = session.get('user_id')
        if user_id:
            new_order.user_id = user_id
        else:
            return {'error': 'User not authenticated'}, 401

        db.session.add(new_order)
        db.session.commit()

        return new_order.to_dict(), 201
    
    def patch(self, order_number):
        order = Order.query.get(order_number)
        updated_order = request.get_json().get('destination')

        if updated_order:
            order.destination=updated_order
            db.session.commit()

            return order.to_dict(),200
        else:
            return {"error": "you did not update the order"}
        
    def delete(self, order_number):
        order = Order.query.get(order_number)
        if order:
            db.session.delete(order)
            db.session.commit()
            return {'info': 'Order deleted successfully'}, 200
        else:
            return {'error': 'Order not found'}, 404
        

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id'] = None
            return {'info': 'user logged out successfully'}
        else:
            return {'error': 'unauthorized'}, 401
        


        #Admin routes starts here
        
        
@app.before_request
def check_if_logged_in():
    if 'admin_id' not in session and request.endpoint not in ["admin_login", "admin_signup", "index"]:
        return {"error": "unauthorized"}, 401

class CheckSession(Resource):
    def get(self):
        if session.get('admin_id'):
            admin = Admin.query.filter(Admin.id == session['admin_id']).first()
            return admin.to_dict(), 200

        return {'error': 'Resource unavailable'}, 401



    # we dont need an admin signing up

#class AdminSignup(Resource):
    # def post(self):
    #     username = request.get_json().get("username")
    #     password = request.get_json().get("password")

    #     if username and password:
    #         new_admin = Admin(username=username)
    #         new_admin.password_hash = password  

    #         db.session.add(new_admin)
    #         db.session.commit()

    #         session['admin_id'] = new_admin.id
    #         return new_admin.to_dict(), 201

    #     return {"error": "admin details must be provided"}, 422

class AdminLogin(Resource):
    def post(self):
        username = request.get_json().get("username")
        password = request.get_json().get("password")
        admin = Admin.query.filter(Admin.username == username).first()

        if admin:
            if admin.authenticate(password):
                session['admin_id'] = admin.id
                admin_dict = admin.to_dict()
                return make_response(jsonify(admin_dict), 201)
            else:
                return {"error": "Invalid password"}, 401

        return {"error": "Admin not found"}, 404

class AdminLogout(Resource):
    def delete(self):
        if session.get('admin_id'):
            session.pop('admin_id', None)  
            return {'info': 'admin logged out successfully'}
        else:
            return {'error': 'unauthorized'}, 401
        

api.add_resource(CheckSession, "/session", endpoint="session")
api.add_resource(Index, "/", endpoint="index") 
api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(Login, "/login", endpoint="login")       
api.add_resource(Logout, "/logout", endpoint="logout")
api.add_resource(Orders, "/orders", "/orders/<int:order_number>")
# api.add_resource(AdminSignup, "/admin/signup", endpoint="admin_signup")
api.add_resource(AdminLogin, "/admin/login", endpoint="admin_login")
api.add_resource(AdminLogout, "/admin/logout", endpoint="admin_logout")



application = app

if __name__ == '__main__':
    app.run(debug=True)

