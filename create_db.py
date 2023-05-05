from app import app, db
from models import Credentials, InventoryInfo, Reviews
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()

    # Initial loading of sizes
    # sizes = ['XS', 'S', 'M', 'L', 'XL']
    # for each_size in sizes:
    #     print(f'{each_size} inserted into size')
    #     a_size = Size(size=each_size)
    #     db.session.add(a_size)
    #     db.session.commit()

    # Initial loading of users
    users = [
        {'username': 'student', 'password': generate_password_hash('studentpw', method='sha256'),
         'first_name':'Student', 'last_name':'Student', 'email': 'student@umd.edu', 'role':'STUDENT'},
        {'username': 'employee', 'password': generate_password_hash('employeepw', method='sha256'),
         'first_name': 'Employee', 'last_name': 'Employee', 'email': 'employee@umd.edu', 'role': 'EMPLOYEE'},
        {'username': 'admin', 'password': generate_password_hash('adminpw', method='sha256'),
         'first_name': 'Admin', 'last_name': 'Admin', 'email': 'admin@umd.edu', 'role': 'ADMIN'},
    ]

    for each_user in users:
        print(f'{each_user["username"]} inserted into user')
        a_user = Credentials(username=each_user["username"], password=each_user["password"], first_name=each_user["first_name"],
                             last_name=each_user["last_name"], email=each_user["email"], role=each_user["role"])
        db.session.add(a_user)
        db.session.commit()

    # Initial loading of inventory
    products = [
        {'collection_id': 1, 'item_name': 'Quarter-Zip', 'xsmall': 10, 'small': 10, 'medium': 10, 'large': 10,
         'xlarge': 10, 'xxlarge': 10, 'price': 45.00, 'desc': 'ATB warm and comfy Quarter-Zip',
         'product_image': 'Shop_QuarterZip.png'},
        {'collection_id': 3, 'item_name': 'Crewneck', 'xsmall': 10, 'small': 10, 'medium': 10, 'large': 10,
         'xlarge': 10, 'xxlarge': 10, 'price': 40.00, 'desc': 'ATB warm and comfy crewneck',
         'product_image': 'Shop_Crewneck.png'},
        {'collection_id': 1, 'item_name': 'Long Sleeve', 'xsmall': 10, 'small': 10, 'medium': 10, 'large': 10,
         'xlarge': 10, 'xxlarge': 10, 'price': 36.00, 'desc': 'ATB comfy long sleeve',
         'product_image': 'Shop_LongSleeve.png'},
        {'collection_id': 2, 'item_name': 'Original Tee', 'xsmall': 10, 'small': 10, 'medium': 10, 'large': 10,
         'xlarge': 10, 'xxlarge': 10, 'price': 28.00, 'desc': 'ATB comfy original tee',
         'product_image': 'Shop_OriginalTee.png'},
        {'collection_id': 3, 'item_name': 'T-Shirt', 'xsmall': 10, 'small': 10, 'medium': 10, 'large': 10,
         'xlarge': 10, 'xxlarge': 10, 'price': 28.00, 'desc': 'ATB comfy t-shirt',
         'product_image': 'Shop_tshirt.png'},
    ]

    for each_product in products:
        print(f'{each_product["item_name"]} inserted into product')
        a_product = InventoryInfo(collection_id=each_product['collection_id'], item_name=each_product['item_name'],
                                  xsmall=each_product['xsmall'], small=each_product['small'],
                                  medium=each_product['medium'], large=each_product['large'],
                                  xlarge=each_product['xlarge'],
                                  xxlarge=each_product['xxlarge'], price=each_product['price'],
                                  desc=each_product['desc'],
                                  product_image=each_product['product_image'])
        db.session.add(a_product)
        db.session.commit()

    reviews = [
        {'account_id': None, 'first_name': 'John', 'last_name': 'Green', 'email': 'jgreen@gmail.com', 'rating': '5/5', 'message': 'Great product!', 'posted': True},
        {'account_id': None, 'first_name': 'Kate', 'last_name': 'Richards', 'email': 'krichards@gmail.com', 'rating': '4/5', 'message': 'I like my crewneck!',
         'posted': True},
        {'account_id': None, 'first_name': 'Billy', 'last_name': 'Stevenson', 'email': 'bsteve23@gmail.com', 'rating': '3/5', 'message': 'Not as good as I thought',
         'posted': False},
        {'account_id': None, 'first_name': 'Samantha', 'last_name': 'Smith', 'email': 'ss3456@gmail.com', 'rating': '5/5', 'message': 'Incredible products!',
         'posted': True},
        {'account_id': None, 'first_name': 'Mark', 'last_name': 'Greenberg', 'email': 'markgb354@gmail.com', 'rating': '2/5', 'message': 'Terrible!',
         'posted': False},
    ]

    for each_review in reviews:
        print(f'{each_review["rating"]} inserted into table.')
        a_review = Reviews(account_id=each_review['account_id'], first_name=each_review['first_name'], email=each_review['email'], last_name=each_review['last_name'],
                            rating=each_review['rating'], message=each_review['message'],
                            posted=each_review['posted'])

        db.session.add(a_review)
        db.session.commit()