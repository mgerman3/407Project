from app import app, db
from models import Credentials, InventoryInfo
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
        {'collection_id': None, 'item_name': 'Quarter-Zip', 'xsmall': 10, 'small': 10, 'medium': 10, 'large': 10,
         'xlarge': 10, 'xxlarge': 10, 'price': 45.00, 'desc': 'ATB warm and comfy Quarter-Zip',
         'product_image': 'Shop_QuarterZip.png'},
        {'collection_id': None, 'item_name': 'Crewneck', 'xsmall': 10, 'small': 10, 'medium': 10, 'large': 10,
         'xlarge': 10, 'xxlarge': 10, 'price': 40.00, 'desc': 'ATB warm and comfy crewneck',
         'product_image': 'Shop_Crewneck.png'},
        {'collection_id': None, 'item_name': 'Long Sleeve', 'xsmall': 10, 'small': 10, 'medium': 10, 'large': 10,
         'xlarge': 10, 'xxlarge': 10, 'price': 36.00, 'desc': 'ATB comfy long sleeve',
         'product_image': 'Shop_LongSleeve.png'},
        {'collection_id': None, 'item_name': 'Original Tee', 'xsmall': 10, 'small': 10, 'medium': 10, 'large': 10,
         'xlarge': 10, 'xxlarge': 10, 'price': 28.00, 'desc': 'ATB comfy original tee',
         'product_image': 'Shop_OriginalTee.png'},
        {'collection_id': None, 'item_name': 'T-Shirt', 'xsmall': 10, 'small': 10, 'medium': 10, 'large': 10,
         'xlarge': 10, 'xxlarge': 10, 'price': 28.00, 'desc': 'ATB comfy t-shirt',
         'product_image': 'Shop_tshirt.png'},
    ]

    # for each_product in products:
    #     print(f'{each_product["item_name"]} inserted into product')
    # a_product = InventoryInfo(collection_id=each_product['collection_id'], item_name=each_product['item_name'], xsmall=each_product['xsmall'], small=each_product['small'],
    #                           medium=each_product['medium'], large=each_product['large'], xlarge=each_product['xlarge'],
    #                           xxlarge=each_product['xxlarge'], price=each_product['price'], desc=each_product['desc'],
    #                           product_image=each_product['product_image'])
    # db.session.add(a_product)
    # db.session.commit()

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