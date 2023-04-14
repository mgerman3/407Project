from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()


class User(UserMixin, db.Model):
   __tablename__ = "User"

   user_id = db.Column(db.Integer, primary_key=True)
   first_name = db.Column(db.String(30), nullable=False)
   last_name = db.Column(db.String(50), nullable=False)
   email = db.Column(db.String(60), nullable=False)
   address = db.Column(db.String(100), nullable=False)
   state = db.Column(db.String(2), nullable=False)
   zipcode = db.Column(db.Integer, nullable=False)


   def __init__(self, first_name, last_name, email, address, state, zipcode):
       self.first_name = first_name
       self.last_name = last_name
       self.email = email
       self.address = address
       self.state = state
       self.zipcode = zipcode


   def __repr__(self):
       return f"{self.first_name} {self.last_name}"


class Requests(db.Model):
   __tablename__ = "Requests"


   request_id = db.Column(db.Integer, primary_key=True)
   customer_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
   request_info = db.Column(db.String(200), nullable=False)


   def __init__(self, customer_id, request_info):
       self.customer_id = customer_id
       self.request_info = request_info


   def __repr__(self):
       return f"{self.request_info}"


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

class Size(db.Model):
   __tablename__ = "Size"


   size_id = db.Column(db.Integer, primary_key=True)
   size = db.Column(db.String(30), nullable=False)
   items = db.relationship('Inventory', backref='items')


   def __init__(self, size):
       self.size = size


   def __repr__(self):
       return f"{self.size}"

class Inventory(db.Model):
    __tablename__ = "Inventory"

    product_id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('Collections.collection_id'))
    size = db.Column(db.String(6), db.ForeignKey('Size.size_id'), nullable=False)
    color = db.Column(db.String(12), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, collection_id, size, color, quantity):
        self.collection_id = collection_id
        self.size = size
        self.color = color
        self.quantity = quantity


    def __repr__(self):
        return f"{self.size} {self.color} {self.quantity}"



class Cart(db.Model):
    __tablename__ = "Cart"

    order_id = db.Column(db.Integer, db.ForeignKey('OrderInfo.order_id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Inventory.product_id'), primary_key=True)

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


class Credentials(db.Model):
    __tablename__ = "Credentials"

    username = db.Column(db.String(40), primary_key=True)
    password = db.Column(db.String(40), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    def __init__(self, username, password, role='PUBLIC'):
        self.username = username
        self.password = password
        self.role = role

    def get_id(self):
        return (self.username)

    def __repr__(self):
       return f"({self.username}){self.password}{self.role}"

   # Only execute once! Initial load of sizes
   #db.engine.execute("INSERT INTO sizes(size) VALUES ('XS');")
