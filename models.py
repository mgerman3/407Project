from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()


class User(db.Model):
   __tablename__ = "User"

   user_id = db.Column(db.Integer, primary_key=True)
   account_id = db.Column(db.Integer, db.ForeignKey('Credentials.account_id'))
   first_name = db.Column(db.String(30), nullable=False)
   last_name = db.Column(db.String(50), nullable=False)
   email = db.Column(db.String(60), nullable=False)
   address = db.Column(db.String(100), nullable=True)
   state = db.Column(db.String(2), nullable=True)
   zipcode = db.Column(db.Integer, nullable=True)
   phoneNumber = db.Column(db.Integer, nullable=True)


   def __init__(self, first_name, last_name, email, address, state, zipcode, phoneNumber):
       self.first_name = first_name
       self.last_name = last_name
       self.email = email
       self.address = address
       self.state = state
       self.zipcode = zipcode
       self.phoneNumber = phoneNumber


   def __repr__(self):
       return f"{self.first_name} {self.last_name} {self.email} {self.address} {self.state}"


class Requests(db.Model):
   __tablename__ = "Requests"

   request_id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
   message = db.Column(db.String(200), nullable=False)

   def __init__(self, message):
       self.message = message

   def __repr__(self):
       return f"{self.message}"


class OrderInfo(db.Model):
   __tablename__ = "OrderInfo"

   order_id = db.Column(db.Integer, primary_key=True)
   customer_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
   shipping_mode = db.Column(db.String(30), nullable=False)
   order_total = db.Column(db.Float, nullable=False)
   def __init__(self, customer_id, shipping_mode, order_total, date) :
       self.customer_id = customer_id
       self.shipping_mode = shipping_mode
       self.order_total = order_total
       self.date = date
   def __repr__(self):
       return f"{self.shipping_mode}"

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
    color = db.Column(db.String(12), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.String(50), nullable=False)

    def __init__(self, item_name, xsmall, small, medium, large, xlarge, xxlarge, color, price, desc):
        self.item_name = item_name
        self.xsmall = xsmall
        self.small = small
        self.medium = medium
        self.large = large
        self.xlarge = xlarge
        self.xxlarge = xxlarge
        self.color = color
        self.price = price
        self.desc = desc

    def __repr__(self):
        return f"{self.item_name} {self.color} {self.desc}"


class Cart(db.Model):
    __tablename__ = "Cart"

    order_id = db.Column(db.Integer, db.ForeignKey('OrderInfo.order_id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('InventoryInfo.product_id'), primary_key=True)

    def __init__(self, order_id, product_id) :
        self.order_id = order_id
        self.product_id = product_id


class Collections(db.Model):
    __tablename__ = "Collections"

    collection_id = db.Column(db.Integer, primary_key=True)
    collection_name = db.Column(db.String(20), nullable=False)

    def __init__(self, collection_name) :
        self.collection_name = collection_name
    def __repr__(self):
       return f"{self.collection_name}"


class Credentials(UserMixin, db.Model):
    __tablename__ = "Credentials"

    account_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    def __init__(self, username, password, role='PUBLIC'):
        self.username = username
        self.password = password
        self.role = role

    def get_id(self):
        return (self.account_id)

    def __repr__(self):
       return f"({self.username}){self.password}{self.role}"

   # Only execute once! Initial load of sizes
   #db.engine.execute("INSERT INTO sizes(size) VALUES ('XS');")
