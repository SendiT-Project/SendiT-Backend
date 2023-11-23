
from flask import Flask
from flask_migrate import Migrate
from models import db, User,Tracking,Order
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"]= os.environ("DATABASE_URI")
app.config["SQLACHEMY_TRACK_MODIFICATIONS"]=False

migrate = Migrate(app,db)
db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)

