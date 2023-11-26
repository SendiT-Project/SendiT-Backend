from faker import Faker
from app import app
from models import db, User,Order, Admin
from passlib.hash import sha256_crypt

fake = Faker()

with app.app_context():
    
        User.query.delete()
        Order.query.delete()
        Admin.query.delete()

        users = []
        for n in range(5):
            email = fake.email()
            _password_hash = fake.password(length=10, special_chars=True)
            hashed_pass = sha256_crypt.hash(_password_hash)

            user = User(username=fake.name(), email=email, _password_hash=hashed_pass)
            users.append(user)

        db.session.add_all(users)
        db.session.commit()

        admins = []
        for n in range(2):
            email = fake.email()
            _password_hash = fake.password(length=10, special_chars=True)
            hashed_pass = sha256_crypt.hash(_password_hash)

            admin = Admin(username=fake.name(), _password_hash=hashed_pass)
            admins.append(admin)

        db.session.add_all(admins)
        db.session.commit()

        orders = []
        for n in range(5):
            
            name_of_parcel = fake.word()
            destination = fake.city()
            current_location = fake.sentence()
            pickup = fake.city()
            weight = fake.random_digit()
            user = fake.random_element(elements=users)

            order = Order(
                name_of_parcel=name_of_parcel,
                destination=destination,
                pickup=pickup,
                weight=weight,
                user=user,
            )
            orders.append(order)

        db.session.add_all(orders)
        db.session.commit()


    
print("Seeding success")