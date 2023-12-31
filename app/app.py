
from flask import Flask, make_response, jsonify, session, request
from flask_restful import Api, Resource
from datetime import timedelta
from flask_migrate import Migrate
from flask_cors import CORS
from flask_session import Session
from models import db, User,Order
from werkzeug.exceptions import NotFound
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*', allow_headers=["Content-Type", "Authorization"])
app.secret_key = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"]= os.environ["DATABASE_URI"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config['SESSION_TYPE'] = 'filesystem'
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=1)
app.config['SESSION_COOKIE_SAMESITE'] = "Lax"
app.config['SESSION_FILE_DIR'] = 'session_dir'
app.config['JSONIFY_PRETTYPRINT_REGULAR']= True

app.config['MAIL_SERVER']='smtp.elasticemail.com'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'medrine.mulindi@gmail.com'
app.config['MAIL_PASSWORD'] = '246C83BBDD60962335267E5FFBB38D143CD4'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False



migrate = Migrate(app,db)
db.init_app(app)
mail = Mail(app)

api = Api(app)
app.config.from_object(__name__)
Session(app)



def send_welcome_email(user_email, username):
    
    
    message = Message(
        subject='Welcome to Your App',
        recipients=[user_email],
        sender='medrine.mulindi@gmail.com',  
    )
    message.body = f'Hello {username},\n\nWelcome to Your App! Thank you for signing up.'
    print(message.body)


    mail.send(message)


def send_login_email(email, username):
    message = Message(
        subject= 'Login successful',
        recipients=[email],
        sender='medrine.mulindi@gmail.com'
    )
    message.body = f'Hello {username},\n\nYou have successfully logged in.'

    mail.send(message)
    

def send_status_update_email(user_email, username, order):
    message = Message(
        subject='Order Status Update',
        recipients=[user_email],
        sender='medrine.mulindi@gmail.com'
    )
    message.body = f'Hello {username},\n\nYour order status has been updated to {order.status}.Thank you for choosing us.'

    mail.send(message)

def send_location_update_email(user_email, username, order):
    message = Message(
        subject='Order Location Update',
        recipients=[user_email],
        sender='medrine.mulindi@gmail.com'
    )
    message.body = f'Hello {username},\n\nThe current location of your order has been updated to {order.current_location}. Thank you for choosing us.'

    mail.send(message)

@app.before_request
def check_if_logged_in():
    if request.method == 'OPTIONS':
        return
        

    if 'user_id' not in session and request.endpoint not in ["login", "signup", "session", "index"]:
        return make_response(jsonify({"error": "unauthorized"}), 401
)
    

class Index(Resource):
    def get(self):
        response_body = "Hello, World"
        status =200
        headers ={}
        return make_response(response_body, status, headers)


class Signup(Resource):
    def post(self):
        username = request.get_json().get("username")
        email = request.get_json().get("email")
        password = request.get_json().get("password")
        admin = request.get_json().get("admin")

        if username and email and password:
            new_user = User(username=username, email=email, admin=admin)
            new_user.password_hash = password

            db.session.add(new_user)
            db.session.commit()

            session["user_id"] = new_user.id

            send_welcome_email(email, username)

            return make_response(jsonify(new_user.to_dict()), 201)
        
        return make_response(jsonify({"error": "user details must be added"}), 422)
        

class Login(Resource):
    def post(self):
        if "user_id" in session:
            return make_response(jsonify({"error": "User is already logged in"}), 400  )
          
        username = request.get_json().get("username")
        password = request.get_json().get("password")
        user = User.query.filter(User.username==username).first()

        if user:
            
            if user.authenticate(password):
                session['user_id'] = user.id

                user_dict = user.to_dict()

                # send_login_email(user.email, user.username)
                
                print("Login successful. user ID:", user.id) 
                
                return make_response(jsonify(user_dict), 201)
            else:
                print("Invalid password.")  
                return make_response(jsonify({"error": "Invalid password"}), 401)
        
        print("User not registered.") 
        return make_response(jsonify({"error": "User not Registered"}), 404)
    


class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id'] = None
            session.pop('user_id')
            print("User logged out succssfully")
            return make_response(jsonify({'info': 'user logged out successfully'}), 200)
        else:
            return make_response(jsonify({'error': 'You are not logged in. Please log in.'}), 401)

class Users(Resource):
    def get(self):
            user = [user.to_dict() for user in User.query.all()]
            response = make_response(jsonify(user), 200)
            return response

class Orders(Resource):
    def get(self):
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
            return make_response(jsonify({'error': 'User not authenticated'}), 401)

        db.session.add(new_order)
        db.session.commit()

        return make_response(jsonify(new_order.to_dict()), 201)
    
@app.route("/orders", methods=["OPTIONS"])
def handle_options_request():
    response = make_response()
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

    
class Order_by_id(Resource):
    def get(self, order_number):
        order_by_id = Order.query.filter_by(order_number=order_number).first()

        if order_by_id is None:
            error_message = {'error': 'No order found with the specified ID'}
            response = make_response(jsonify(error_message), 404)  
        else:
            response_dict = order_by_id.to_dict()
            response = make_response(jsonify(response_dict), 200)

        return response

 

    def patch(self, order_number):
        order = Order.query.filter_by(order_number=order_number).first()

        if not order:
            return make_response(jsonify({'error': 'Order not found'}), 404)

        data = request.get_json()


        if 'destination' in data:
            order.destination = data['destination']

        if 'status' in data:
            old_status = order.status
            order.status = data['status']

            if old_status != data['status']:
                user = User.query.get(order.user_id)
                if user:
                    send_status_update_email(user.email, user.username, order)

    
        if 'current_location' in data:
            old_current_location = order.current_location
            order.current_location = data['current_location']

            if old_current_location != data['current_location']:
                user = User.query.get(order.user_id)
                if user:
                    send_location_update_email(user.email, user.username, order)

        db.session.commit()

        return make_response(jsonify(order.to_dict()), 200)


        
    def delete(self, order_number):
        order = Order.query.get(order_number)
        if order:
            db.session.delete(order)
            db.session.commit()
            return make_response(jsonify({'info': 'Order deleted successfully'}), 200)
        else:
            return make_response(jsonify({'error': 'Order not found'}), 404)
        
        
    
class CheckSession(Resource):
    def get(self):
        print("Received request to /session")
        if session.get('user_id'):
            user = User.query.filter(User.id==session['user_id']).first()

            print(f"User authenticated: {user}")
            return make_response(jsonify(user.to_dict()), 200)
        
        print("User not authenticated")
        return make_response(jsonify({'error': 'No user in session'}), 401)


        

api.add_resource(CheckSession, "/session", endpoint="session")
api.add_resource(Index, "/", endpoint="index") 
api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(Login, "/login", endpoint="login")       
api.add_resource(Logout, "/logout", endpoint="logout")
api.add_resource(Users, "/users", endpoint="users")
api.add_resource(Orders, "/orders", endpoint = "orders")
api.add_resource(Order_by_id, "/orders/<int:order_number>", endpoint="order_by_id")


@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(jsonify({"message": "Resource not found in the server"}), 404)
    
    return response


if __name__ == '__main__':
    app.run(port=5005, debug=True)
