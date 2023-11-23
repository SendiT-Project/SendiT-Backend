
from flask import Flask
from flask_migrate import Migrate
from models import db, User,Tracking,Order


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///app.db'
app.config["SQLACHEMY_TRACK_MODIFICATIONS"]=False

migrate = Migrate(app,db)
db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)

