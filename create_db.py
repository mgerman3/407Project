from app import app, db
from models import Credentials
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

# Initial loading of products
#     products = [
#         {'item_name': 'Quarter-Zip', 'product_id': '1',
#          'desc': 'ATB warm and comfy quarter-zip',
#          'product_image': 'Shop_QuarterZip.png', 'product_price': 45.00},
#         {'item_name': 'Crewneck', 'product_id': '2',
#          'desc': 'ATB warm and comfy crewneck',
#          'product_image': 'Shop_Crewneck.png', 'product_price': 40.00},
#         {'item_name': 'Long Sleeve', 'product_id': '3',
#          'desc': 'ATB comfy long sleeve',
#          'product_image': 'Shop_LongSleeve', 'product_price': 36.00},
#         {'item_name': 'Original Tee', 'product_id': '4',
#          'desc': 'ATB comfy original tee',
#          'product_image': 'Shop_OriginalTee', 'product_price': 28.00},
#         {'item_name': 'T-Shirt', 'product_id': '5',
#          'desc': 'ATB comfy t-shirt',
#          'product_image': 'Shop_tshirt', 'product_price': 28.00}
#     ]
#
#     for each_product in products:
#         print(f'{each_product["item_name"]} inserted into product')
#         a_product = InventoryInfo(item_name=each_product['item_name'], product_id=each_product['product_id'],
#                             desc=each_product['product_description'],
#                             image=each_product['product_image'],
#                             price=each_product['product_price'])
#         db.session.add(a_product)
#         db.session.commit()


