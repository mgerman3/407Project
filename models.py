from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

# create user table
class User(db.Model):
   __tablename__ = "User"

   user_id = db.Column(db.Integer, primary_key=True)
   account_id = db.Column(db.Integer, db.ForeignKey('Credentials.account_id'))
   first_name = db.Column(db.String(30), nullable=False)
   last_name = db.Column(db.String(50), nullable=False)
   email = db.Column(db.String(60), nullable=False)

# initialize user table
   def __init__(self, first_name, last_name, email):
       self.first_name = first_name
       self.last_name = last_name
       self.email = email

   def __repr__(self):
       return f"{self.first_name} {self.last_name} {self.email} {self.address} {self.state}"

# create requests table
class Requests(db.Model):
   __tablename__ = "Requests"

   request_id = db.Column(db.Integer, primary_key=True)
   account_id = db.Column(db.Integer, db.ForeignKey('Credentials.account_id'), nullable=True)
   first_name = db.Column(db.String(30), nullable=True)
   last_name = db.Column(db.String(50), nullable=True)
   email = db.Column(db.String(60), nullable=True)
   message = db.Column(db.String(200), nullable=False)

# initialize requests table
   def __init__(self, account_id, first_name, last_name, email, message):
       self.account_id = account_id
       self.first_name = first_name
       self.last_name = last_name
       self.email = email
       self.message = message

   def __repr__(self):
       return f"{self.first_name}{self.last_name}{self.message}"

# create inventory table
class InventoryInfo(db.Model):
    __tablename__ = "InventoryInfo"

    product_id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('Collections.collection_id'))
    item_name = db.Column(db.String(20), nullable=False)
    xsmall = db.Column(db.Integer, nullable=False)
    small = db.Column(db.Integer, nullable=False)
    medium = db.Column(db.Integer, nullable=False)
    large = db.Column(db.Integer, nullable=False)
    xlarge = db.Column(db.Integer, nullable=False)
    xxlarge = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    desc = db.Column(db.String(50), nullable=False)
    product_image = db.Column(db.String(100))

# initialize inventory table
    def __init__(self, collection_id, item_name, xsmall, small, medium, large, xlarge, xxlarge, price, desc, product_image):
       self.collection_id = collection_id
       self.item_name = item_name
       self.xsmall = xsmall
       self.small = small
       self.medium = medium
       self.large = large
       self.xlarge = xlarge
       self.xxlarge = xxlarge
       self.price = price
       self.desc = desc
       self.product_image = product_image

    def __repr__(self):
       return f"{self.item_name}  {self.desc}"

# create order table
class OrderItem(db.Model):
    __tablename__ = 'OrderItem'

    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('StoreOrder.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('InventoryInfo.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_charged = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String(20), nullable=False)
    item_name = db.Column(db.String(20), nullable=False)

# initialize order table
    def __init__(self, order_id, product_id, quantity, size, item_name):
        product = InventoryInfo.query.filter_by(product_id=product_id).first()

        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price_charged = product.price * quantity
        self.price = product.price
        self.size = size
        self.item_name = item_name

# create collection table
class Collections(db.Model):
    __tablename__ = "Collections"

    collection_id = db.Column(db.Integer, primary_key=True)
    collection_name = db.Column(db.String(20), nullable=True)

# initialize collection table
    def __init__(self, collection_name) :
        self.collection_name = collection_name
    def __repr__(self):
       return f"{self.collection_name}"

# create credentials table
class Credentials(UserMixin, db.Model):
    __tablename__ = "Credentials"

    account_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(10), nullable=False)

# initialize credentials table
    def __init__(self, username, password, first_name, last_name, email, role='PUBLIC'):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = role

# get id
    def get_id(self):
        return (self.account_id)

    def __repr__(self):
       return f"({self.username}){self.password}{self.role}"

# create order table with user shipping info
class StoreOrder(db.Model):
    __tablename__ = 'StoreOrder'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('Credentials.account_id'), nullable=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phoneNumber = db.Column(db.String(10))
    email = db.Column(db.String(100))
    address = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(9))
    shipping_method = db.Column(db.String(20))

# initialize order table
    def __init__(self, account_id, first_name, last_name, phoneNumber, email, address, city, state, zipcode, shipping_method):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.phoneNumber = phoneNumber
        self.email = email
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.shipping_method = shipping_method

# create reviews table
class Reviews(db.Model):
    __tablename__ = "Reviews"

    review_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('Credentials.account_id'), nullable=True)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(60), nullable=True)
    message = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.String(20), nullable=False)
    posted = db.Column(db.Boolean, default=False)

# initialize reviews table
    def __init__(self, account_id, first_name, last_name, email, message, rating, posted):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.message = message
        self.rating = rating
        self.posted = posted

    def __repr__(self):
        return f"{self.first_name}{self.last_name}{self.message}"
