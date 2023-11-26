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


# -i https://pypi.org/simple
# alembic==1.12.1; python_version >= '3.7'
# aniso8601==9.0.1
# blinker==1.7.0; python_version >= '3.8'
# click==8.1.7; python_version >= '3.7'
# flask==3.0.0; python_version >= '3.8'
# flask-migrate==4.0.5; python_version >= '3.6'
# flask-restful==0.3.10
# flask-sqlalchemy==3.1.1; python_version >= '3.8'
# greenlet==3.0.1; platform_machine == 'aarch64' or (platform_machine == 'ppc64le' or (platform_machine == 'x86_64' or (platform_machine == 'amd64' or (platform_machine == 'AMD64' or (platform_machine == 'win32' or platform_machine == 'WIN32')))))
# gunicorn==21.2.0; python_version >= '3.5'
# itsdangerous==2.1.2; python_version >= '3.7'
# jinja2==3.1.2; python_version >= '3.7'
# mako==1.3.0; python_version >= '3.8'
# markupsafe==2.1.3; python_version >= '3.7'
# packaging==23.2; python_version >= '3.7'
# psycopg2-binary==2.9.9; python_version >= '3.7'
# pytz==2023.3.post1
# six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'
# sqlalchemy==2.0.23; python_version >= '3.7'
# sqlalchemy-serializer==1.4.1
# typing-extensions==4.8.0; python_version >= '3.8'
# werkzeug==3.0.1; python_version >= '3.8'
