from app import app, db
from models import Size, Credentials
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()

    # Initial loading of sizes
    sizes = ['XS', 'S', 'M', 'L', 'XL']
    for each_size in sizes:
        print(f'{each_size} inserted into size')
        a_size = Size(size=each_size)
        db.session.add(a_size)
        db.session.commit()

    # Initial loading of users
    users = [
        {'username': 'student', 'email': 'student@umd.edu', 'first_name':'Imma', 'last_name':'Student',
            'password': generate_password_hash('studentpw', method='sha256'), 'role':'STUDENT'},
        {'username': 'manager', 'email': 'manager@umd.edu', 'first_name':'Joe', 'last_name':'King',
            'password': generate_password_hash('managerpw', method='sha256'), 'role':'MANAGER'},
        {'username': 'admin', 'email': 'admin@umd.edu', 'first_name':'Crystal', 'last_name':'Ball',
            'password': generate_password_hash('adminpw', method='sha256'), 'role':'ADMIN'},
    ]

    for each_user in users:
        print(f'{each_user["username"]} inserted into user')
        a_user = Credentials(username=each_user["username"], password=each_user["password"], role=each_user["role"])
        db.session.add(a_user)
        db.session.commit()


