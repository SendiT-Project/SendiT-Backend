from faker import Faker
from app import app
from models import db, User, Tracking, Orders
from passlib.hash import sha256_crypt

fake = Faker()

with app.app_context():
    
        User.query.delete()
        Orders.query.delete()
        Tracking.query.delete()

        users = []
        for n in range(10):
            email = fake.email()
            password = fake.password(length=10, special_chars=True)
            hashed_pass = sha256_crypt.hash(password)

            user = User(username=fake.name(), email=email, password=hashed_pass)
            users.append(user)

        db.session.add_all(users)
        db.session.commit()

        orders = []
        for n in range(10):
            
            name_of_parcel = fake.word()
            destination = fake.city()
            pickup = fake.city()
            weight = fake.random_digit()
            user = fake.random_element(elements=users)

            order = Orders(
                name_of_parcel=name_of_parcel,
                destination=destination,
                pickup=pickup,
                weight=weight,
                user=user,
            )
            orders.append(order)

        db.session.add_all(orders)
        db.session.commit()

        trackers = []
        for i in range (10):
             order = fake.random_element(elements=orders)
            #  status = fake.word()
             user = fake.random_element(elements=users)
             tracker = Tracking(order=order,user=user)
             trackers.append(tracker)
        db.session.add_all(trackers)
        db.session.commit()



    



    
print("Seeding success")


