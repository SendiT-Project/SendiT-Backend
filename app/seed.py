from app import app
from models import db, User, Order

with app.app_context():
    Order.query.delete()

    User.query.delete()

    db.session.commit()

print("Seeded data deleted successfully.")
