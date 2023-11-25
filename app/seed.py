from app import app
from models import db, User, Order, Admin

with app.app_context():
    Order.query.delete()

    User.query.delete()

    Admin.query.delete()

    db.session.commit()

print("Seeded data deleted successfully.")
