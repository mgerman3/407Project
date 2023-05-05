import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from authorize import role_required
from models import *
from sqlalchemy import func

# Path: app.py
basedir = os.path.abspath(os.path.dirname(__file__))

# Path: app.py
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'ATB2.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'beyond_course_scope'
db.init_app(app)

# Manage log in sessions
login_manager = LoginManager()
login_manager.login_view = 'LogIn' # default login route
login_manager.init_app(app)


# Product image parameters
app.config['PRODUCT_UPLOAD_PATH'] = 'static/products'


# Product order restrictions
app.config['MAX_QUANTITY_PER_ITEM'] = 10


# user loader for flask_login
@login_manager.user_loader
def load_user(account_id):
    return Credentials.query.get(account_id)

# home page route
@app.route('/')
def homePage():
    return render_template('homePage.html')

# route for error page
@app.errorhandler(404)
def errorPage(error):
    return render_template('404.html'), 404

# route for shop page
@app.route('/Shop')
def Shop():
    items = InventoryInfo.query.order_by(InventoryInfo.item_name).all()
    return render_template('shop.html', items=items)

# route for about page
@app.route('/About')
def About():
    return render_template('aboutPage.html')

# route for profile page
@app.route('/profile')
def Profile():
    return render_template('profile.html')

# route for requests page
@app.route('/RequestForm', methods=['GET', 'POST'])
def RequestForm():
    if request.method == 'GET':
        return render_template('requestForm.html', action='create')
    elif request.method == 'POST':
        # if user is authenticated, use their account_id, first_name, last_name, and email from the credentials table
        if current_user.is_authenticated:
            account_id = current_user.account_id
            first_name = current_user.first_name
            last_name = current_user.last_name
            email = current_user.email
            message = request.form['message']

            requests = Requests(account_id=account_id, first_name=first_name, last_name=last_name, email=email, message=message)

        # if user is not authenticated, use the info from the request form
        else:
            account_id = None
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            message = request.form['message']

            requests = Requests(account_id=account_id, first_name=first_name, last_name=last_name, email=email, message=message)

        db.session.add(requests)
        db.session.commit()

        flash(f'Your request was received!', 'success')
        return redirect(url_for('RequestForm'))

    flash(f'Invalid request. Please contact support if this problem persists.', 'error')
    return redirect(url_for('homePage'))


# route for confirming requests by deleting them
@app.route('/RequestsLog/Delete/<int:request_id>')
@login_required
@role_required(['ADMIN'])
def requests_fulfilled(request_id):
    request = Requests.query.filter_by(request_id=request_id).first()
    # if theres a request and an admin deletes it, delete it from the database
    if request:
        db.session.delete(request)
        db.session.commit()
        flash(f'{request_id} was successfully deleted!', 'success')
    # if no request is found, flash an error
    else:
        flash(f'Delete failed! Collection could not be found.', 'error')

    return redirect(url_for('requests_view_all'))


# route for the request form
@app.route('/ReviewForm', methods=['GET', 'POST'])
def ReviewForm():
    review = Reviews.query.order_by(Reviews.review_id) \
        .all()
    if request.method == 'GET':
        return render_template('reviewForm.html', action='create', review=review)
    elif request.method == 'POST':

        # if user is logged in, use all the info from their account and take the rest from the form
        if current_user.is_authenticated:
            account_id = current_user.account_id
            first_name = current_user.first_name
            last_name = current_user.last_name
            email = current_user.email
            message = request.form['message']
            rating = request.form['rating']
            posted = False

            reviews = Reviews(account_id=account_id, first_name=first_name, last_name=last_name, email=email,
                               message=message, rating=rating, posted=posted)
        # if user is not logged in, use the info from the form
        else:
            account_id = None
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            message = request.form['message']
            rating = request.form['rating']
            posted = False

            reviews = Reviews(account_id=account_id, first_name=first_name, last_name=last_name, email=email,
                               message=message, rating=rating, posted=posted)
        # add info to database
        db.session.add(reviews)
        db.session.commit()

        flash(f'Your review was received! ATB will post it shortly.', 'success')
        return redirect(url_for('ReviewForm'))

    flash(f'Invalid request. Please contact support if this problem persists.', 'error')
    return redirect(url_for('homePage'))


# route for the reviews log
@app.route('/ReviewsLog')
@login_required
@role_required(['ADMIN', 'EMPLOYEE'])
def reviews_view_all():
    reviews = Reviews.query.order_by(Reviews.review_id) \
        .all()
    return render_template('reviewsLog.html', reviews=reviews)

# route for deleting reviews
@app.route('/ReviewsLog/Delete/<int:review_id>')
@login_required
@role_required(['ADMIN'])
def review_delete(review_id):
    reviews = Reviews.query.filter_by(review_id=review_id).first()
    # delete the review if the delete button is clicked
    if reviews:
        db.session.delete(reviews)
        db.session.commit()
        flash(f'{review_id} was successfully deleted!', 'success')
    else:
        flash(f'Delete failed! Review could not be found.', 'error')


    return redirect(url_for('reviews_view_all'))

# ability to post reviews that have been submitted to the reviews page
@app.route('/ReviewsLog/Post/<int:review_id>')
@login_required
@role_required(['ADMIN'])
def review_post(review_id):
    reviews = Reviews.query.filter_by(review_id=review_id).first()
    if reviews:
        # if the review is posted then turn it true so that it can appear on the page
        if reviews.posted == False:
            reviews.posted = True
            db.session.commit()
            flash(f'{review_id} was successfully posted!', 'success')
        # if not posted, keep the review false
        else:
            reviews.posted = False
            db.session.commit()
            flash(f'{review_id} was successfully un-posted!', 'success')
    else:
        flash(f'Post failed! Review could not be found.', 'error')

    return redirect(url_for('reviews_view_all'))

# route for the login page
@app.route('/LogIn', methods = ['GET', 'POST'])
def LogIn():
    default_route_function = 'Shop'
    default_user_route_function = 'homePage'

    if request.method == 'GET':
        # Determine where to redirect user if they are already logged in
        if current_user and current_user.is_authenticated:
            if current_user.role in ['EMPLOYEE', 'ADMIN']:
                return redirect(url_for(default_route_function))
            elif current_user.role == 'STUDENT':
                return redirect(url_for(default_user_route_function, user_id=0))
        else:
            redirect_route = request.args.get('next')
            return render_template('logInScreen.html', redirect_route=redirect_route)

    # pull info from the form to match the database
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        redirect_route = request.form.get('redirect_route')

        user = Credentials.query.filter_by(username=username).first()

        # Validate user credentials and redirect them to initial destination
        if user and check_password_hash(user.password, password):
            login_user(user)

            if current_user.role in ['EMPLOYEE', 'ADMIN']:
                return redirect(redirect_route if redirect_route else url_for(default_route_function))
            elif current_user.role == 'STUDENT':
                return redirect(redirect_route if redirect_route else url_for(default_user_route_function, user_id=0))
        else:
            flash(f'Your login information was not correct. Please try again.', 'error')

        return redirect(url_for('LogIn'))

    return redirect(url_for('LogIn'))

# route for sign up page
@app.route('/signup', methods=['GET', 'POST'])
def SignUp():
    if request.method == 'GET':
        return render_template('signUpPage.html', action='create')

    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        # set variable for the password
        sha_password = generate_password_hash(password, method='sha256', salt_length=8)

        user = Credentials(username=username, password=sha_password, first_name=first_name, last_name=last_name,
                          email=email)
        # add to database and log the user in
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f'{username} was successfully added!', 'success')
        return redirect(url_for('homePage'))

# log out route
@app.route('/logout')
@login_required
def logout():
    # if cart exists delete it upon log out
    if 'cart' in session:
        del (session['cart'])
    # sign the user out
    logout_user()
    flash(f'You have been logged out.', category='success')
    return redirect(url_for('homePage'))

# route for checkout page
@app.route('/CheckOut', methods=['GET', 'POST'])
def CheckOut():
    if 'cart' in session:
        # if the cart exists, establish a total value for the products in the cart
        session['cart_total'] = sum(item['price'] * item['product_quantity'] for item in session['cart'])
        return render_template('checkoutPage.html', products=session['cart'], cart_count=len(session['cart']), cart_total=session['cart_total'])
    else:
        return render_template('checkoutPage.html', cart_count=0, cart_total=0)

# route for processing the order once it is placed
@app.route('/process-order', methods=['GET', 'POST'])
def process_order():
    if request.method == 'GET':
        return redirect(url_for('homePage'))
    elif request.method == 'POST':
        # if user is logged in use their account id and get all other info from the form
        if current_user.is_authenticated:
            user = Credentials.query.filter_by(account_id=current_user.account_id).first()

            account_id = user.account_id
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            phoneNumber = request.form['phoneNumber']
            email = request.form['email']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            zipcode = request.form['zipcode']
            shipping_method = request.form['shipping_method']


            store_order = StoreOrder(account_id=account_id, first_name=first_name, last_name=last_name, phoneNumber=phoneNumber,
                                     email=email, address=address, city=city, state=state, zipcode=zipcode,
                                     shipping_method=shipping_method)
        # get all info from form is user not logged in
        else:
            account_id = None
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            phoneNumber = request.form['phoneNumber']
            email = request.form['email']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            zipcode = request.form['zipcode']
            shipping_method = request.form['shipping_method']

            store_order = StoreOrder(account_id=account_id,first_name=first_name, last_name=last_name, phoneNumber=phoneNumber,
                                    email=email, address=address, city=city, state=state, zipcode=zipcode,
                                     shipping_method=shipping_method)
        # add to database
        db.session.add(store_order)
        db.session.flush()
        db.session.refresh(store_order)
        order_id = store_order.order_id

        for each_item in session['cart']:
            # reduce inventory by the number of items purchased
            product = InventoryInfo.query.filter_by(product_id=each_item['product_id']).first()
            if each_item['size'] == 'X-Small':
                product.xsmall -= each_item['product_quantity']
            if each_item['size'] == 'Small':
                product.small -= each_item['product_quantity']
            if each_item['size'] == 'Medium':
                product.medium -= each_item['product_quantity']
            if each_item['size'] == 'Large':
                product.large -= each_item['product_quantity']
            if each_item['size'] == 'X-Large':
                product.xlarge -= each_item['product_quantity']
            if each_item['size'] == 'XX-Large':
                product.xxlarge -= each_item['product_quantity']

            item_ordered = OrderItem(order_id, each_item['product_id'], each_item['product_quantity'],
                                     each_item['size'], each_item['item_name'])
            db.session.add(item_ordered)
            db.session.commit()

        db.session.commit()

    if 'cart' in session:
        del(session['cart'])

    flash(f'Your order has been place! ATB will contact you shortly. Your order number is {order_id}.', 'success')
    db.session.delete(store_order)
    return render_template('homePage.html')

# page for products once user clicks view on the shop page
@app.route('/GenericProduct/<int:product_id>')
def GenProduct(product_id):
    item = InventoryInfo.query.filter_by(product_id=product_id).first()
    collection_id = item.collection_id
    style = Collections.query.filter_by(collection_id=collection_id).first()
    collection = style.collection_name

    if item:
        return render_template('genericProductPage.html', item=item, collection=collection)

    else:
        flash(f'Product attempting to be viewed could not be found! Please contact support for assistance', 'error')
        return redirect(url_for('Shop'))

# route to view the all the request sent by customers
@app.route('/RequestsLog')
@login_required
@role_required(['ADMIN', 'EMPLOYEE'])
def requests_view_all():
    requests = Requests.query.order_by(Requests.request_id) \
        .all()
    return render_template('requestLog.html', requests=requests)

# route to view the inventory
@app.route('/InventoryLog')
@login_required
@role_required(['ADMIN', 'EMPLOYEE'])
def items_view_all():
    items = InventoryInfo.query.order_by(InventoryInfo.item_name) \
        .all()
    dict = {}
    for collection in Collections.query.all():
          dict[collection.collection_id] = collection.collection_name

    return render_template('inventoryLog.html', items=items, dict=dict)

# route to edit the inventory
@app.route('/InventoryLog/update/<int:product_id>', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN', 'EMPLOYEE'])
def item_edit(product_id):

    if request.method == 'GET':
        collections = Collections.query.order_by(Collections.collection_id) \
            .all()
        item = InventoryInfo.query.filter_by(product_id=product_id).first()

        if item:
            return render_template('inputInventory.html', item=item, action='update', collections=collections)

        else:
            flash(f'Item attempting to be edited could not be found!', 'error')

    elif request.method == 'POST':
        item = InventoryInfo.query.filter_by(product_id=product_id).first()
        # if item update based on what the form says
        if item:
            item.item_name = request.form['item_name']
            item.xsmall = request.form['xsmall']
            item.small = request.form['small']
            item.medium = request.form['medium']
            item.large = request.form['large']
            item.xlarge = request.form['xlarge']
            item.xxlarge = request.form['xxlarge']
            item.price = request.form['price']
            item.desc = request.form['desc']
            product_image = request.files['product_image']

            # if user elected to delete the image, remove it
            if('delete_product_image' in request.form or product_image != '') and 'current_product_image' != '' :
                try:
                    os.remove(os.path.join(basedir, app.config['PRODUCT_UPLOAD_PATH'], item.product_image))
                    item.product_image = ''
                except:
                    pass

                product_filename = secure_filename(item.item_name + '-' + product_image.filename)

                # if the file name does not exist, save it
                if product_image.filename != '':
                    product_image.save(os.path.join(basedir, app.config['PRODUCT_UPLOAD_PATH'], product_filename))
                    item.product_image = product_filename if product_image else ''

            db.session.commit()
            flash(f'{item.item_name} was successfully updated!', 'success')
        else:
            flash(f'Item attempting to be edited could not be found!', 'error')

        return redirect(url_for('items_view_all'))

    flash(f'Invalid request. Please contact support if this problem persists.', 'error')
    return redirect(url_for('items_view_all'))

# delete inventory item route
@app.route('/InventoryLog/delete/<int:product_id>')
@login_required
@role_required(['ADMIN'])
def item_delete(product_id):
    item = InventoryInfo.query.filter_by(product_id=product_id).first()
    # if theres an item delete image
    if item:
        try:
            os.remove(os.path.join(app.config['PRODUCT_UPLOAD_PATH'], item.product_image))
        except FileNotFoundError:
            pass
        db.session.delete(item)
        db.session.commit()
        flash(f'{item} was successfully deleted!', 'success')
    else:
        flash(f'Delete failed! Item could not be found.', 'error')

    return redirect(url_for('items_view_all'))

# input inventory route
@app.route('/InventoryInput', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN', 'EMPLOYEE'])
def inventory_entry():
    collections = Collections.query.order_by(Collections.collection_id) \
        .all()

    if request.method == 'GET':
        return render_template('inputInventory.html', action='create', collections=collections)

    # input inventory based on user input
    elif request.method == 'POST':
        item_name = request.form['item_name']
        collection_id = request.form['collection_id']
        xsmall = request.form['xsmall']
        small = request.form['small']
        medium = request.form['medium']
        large = request.form['large']
        xlarge = request.form['xlarge']
        xxlarge = request.form['xxlarge']
        price = request.form['price']
        desc = request.form['desc']
        product_image = request.files['product_image']
        product_filename = secure_filename(item_name + '-' + product_image.filename)

        # if the filename does not exist, create a new one
        if product_image.filename != '':
            product_image.save(os.path.join(basedir, app.config['PRODUCT_UPLOAD_PATH'], product_filename))


        items = InventoryInfo(item_name=item_name, collection_id=collection_id, xsmall=xsmall, small=small, medium=medium, large=large, xlarge=xlarge,
                           xxlarge=xxlarge, price=price, desc=desc, product_image=product_filename if product_image else '')

        # add info to databse
        db.session.add(items)
        db.session.commit()
        flash(f'{item_name} was successfully added!', 'success')
        return redirect(url_for('items_view_all'))

    flash(f'Invalid request. Please contact support if this problem persists.', 'error')
    return redirect(url_for('homePage'))

# displat details of orders placed
@app.route('/OrderDetails')
def OrderDetails():
    orders = OrderItem.query.order_by(OrderItem.order_id) \
        .all()
    info = StoreOrder.query.order_by(StoreOrder.order_id) \
        .all()
    total_order_sum = 0

    # if order placed establush sum and price
    for each_order in orders:
        item_price = each_order.price_charged
        total_order_sum += item_price

    print(total_order_sum)

    return render_template('orderDetails.html', orders=orders, info=info, total_order_sum=total_order_sum)


# allow admin to create new emoloyee accounts
@app.route('/Admin/Create/LogIn', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN'])
def Admin_Login():
    if request.method == 'GET':
        return render_template('adminLogin.html', action='create')

    # if user created add to database based on form
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        role = request.form['role']

        sha_password = generate_password_hash(password, method='sha256', salt_length=8)

        user = Credentials(username=username, password=sha_password, first_name=first_name, last_name=last_name,
                              email=email, role=role)

        db.session.add(user)
        db.session.commit()
        flash(f'{username} was successfully added!', 'success')
        return redirect(url_for('homePage'))

# clear cart route
@app.route('/cart/clear')
@login_required
def clear_cart():
    if 'cart' in session:
        del(session['cart'])
        flash(f"Cart Cleared", 'success')
    else:
        flash(f"Cart already empty", 'error')
    return redirect(url_for('Shop'))

# add items to cart route
@app.route('/cart/add/<int:product_id>', methods=['GET','POST'])
def cart_add(product_id):
   product = InventoryInfo.query.filter_by(product_id=product_id).first()
    # if product has a quantity add it to the variable
    if 'product_quantity' in request.form:
        product_quantity = int(request.form['product_quantity'])
    elif request.method == 'GET':
        product_quantity = 1


    if product:
        # if product exists and cart not in session, create cart
        if 'cart' not in session:
            session['cart'] = []

        # create variable to define an item based on order id and size
        found_item = next((item for item in session['cart'] if
                           item['product_id'] == product_id and request.form['size'] == item['size']), None)

        if found_item:
            # establish quantity and size for the variavle
            found_item['product_quantity'] += product_quantity
            size = request.form['size']
            found_item['size'] = size
            # allow for size to be taken into serious consideration
            found_item = next((item for item in session['cart'] if item['size'] == size), None)

            if found_item['size'] == 'X-Small':
                # if user wants more than is in stock, do not let them add to cart
                 if found_item['product_quantity'] > product.xsmall:
                     found_item['product_quantity'] -= int(request.form['product_quantity'])
                     flash(f"Sorry, we only have {product.xsmall} X-Small in stock.")
                     return redirect(url_for('GenProduct', product_id=product_id))
                 # if user adds amount of quantity to cart that is acceptable based on inventory levels add it to cart
                 if found_item['size'] == size:
                     flash(f"{product.item_name} has been successfully added to your cart.", 'success')
                     product_quantity += int(request.form['product_quantity'])
                     return redirect(url_for('CheckOut'))
                 # if not, add to cart as a new item
                 else:
                     session['cart'].append(
                         {'product_id': product.product_id, 'item_name': product.item_name, 'size': size,
                          'product_image': product.product_image,
                          'product_quantity': product_quantity, 'price': product.price}
                     )
                     return redirect(url_for('CheckOut'))

            if found_item['size'] == 'Small':
                # if user wants more than is in stock, do not let them add to cart
                 if found_item['product_quantity'] > product.small:
                     found_item['product_quantity'] -= int(request.form['product_quantity'])
                     flash(f"Sorry, we only have {product.small} Small in stock.")
                     return redirect(url_for('GenProduct', product_id=product_id))
                 # if user adds amount of quantity to cart that is acceptable based on inventory levels add it to cart
                 if found_item['size'] == size:
                     flash(f"{product.item_name} has been successfully added to your cart.", 'success')
                     product_quantity += int(request.form['product_quantity'])
                     return redirect(url_for('CheckOut'))
                 # if not, add to cart as a new item
                 else:
                     session['cart'].append(
                         {'product_id': product.product_id, 'item_name': product.item_name, 'size': size,
                          'product_image': product.product_image,
                          'product_quantity': product_quantity, 'price': product.price}
                     )
                     return redirect(url_for('CheckOut'))

            if found_item['size'] == 'Medium':
                # if user wants more than is in stock, do not let them add to cart
                if found_item['product_quantity'] > product.medium:
                    found_item['product_quantity'] -= int(request.form['product_quantity'])
                    flash(f"Sorry, we only have {product.medium} Medium in stock.")
                    return redirect(url_for('GenProduct', product_id=product_id))
                # if user adds amount of quantity to cart that is acceptable based on inventory levels add it to cart
                if found_item['size'] == size:
                    flash(f"{product.item_name} has been successfully added to your cart.", 'success')
                    product_quantity += int(request.form['product_quantity'])
                    return redirect(url_for('CheckOut'))
                # if not, add to cart as a new item
                else:
                    session['cart'].append(
                        {'product_id': product.product_id, 'item_name': product.item_name, 'size': size,
                         'product_image': product.product_image,
                         'product_quantity': product_quantity, 'price': product.price}
                    )
                    return redirect(url_for('CheckOut'))

            if found_item['size'] == 'Large':
                # if user wants more than is in stock, do not let them add to cart
                if found_item['product_quantity'] > product.large:
                    found_item['product_quantity'] -= int(request.form['product_quantity'])
                    flash(f"Sorry, we only have {product.large} Large in stock.")
                    return redirect(url_for('GenProduct', product_id=product_id))
                # if user adds amount of quantity to cart that is acceptable based on inventory levels add it to cart
                if found_item['size'] == size:
                    flash(f"{product.item_name} has been successfully added to your cart.", 'success')
                    product_quantity += int(request.form['product_quantity'])
                    return redirect(url_for('CheckOut'))
                # if not, add to cart as a new item
                else:
                    session['cart'].append(
                        {'product_id': product.product_id, 'item_name': product.item_name, 'size': size,
                         'product_image': product.product_image,
                         'product_quantity': product_quantity, 'price': product.price}
                    )
                    return redirect(url_for('CheckOut'))

            if found_item['size'] == 'X-Large':
                # if user wants more than is in stock, do not let them add to cart
                 if found_item['product_quantity'] > product.xlarge:
                     found_item['product_quantity'] -= int(request.form['product_quantity'])
                     flash(f"Sorry, we only have {product.xlarge} X-Large in stock.")
                     return redirect(url_for('GenProduct', product_id=product_id))
                 # if user adds amount of quantity to cart that is acceptable based on inventory levels add it to cart
                 if found_item['size'] == size:
                     flash(f"{product.item_name} has been successfully added to your cart.", 'success')
                     product_quantity += int(request.form['product_quantity'])
                     return redirect(url_for('CheckOut'))
                 # if not, add to cart as a new item
                 else:
                     session['cart'].append(
                         {'product_id': product.product_id, 'item_name': product.item_name, 'size': size,
                          'product_image': product.product_image,
                          'product_quantity': product_quantity, 'price': product.price}
                     )
                     return redirect(url_for('CheckOut'))

            if found_item['size'] == 'XX-Large':
                # if user wants more than is in stock, do not let them add to cart
                 if found_item['product_quantity'] > product.xxlarge:
                     found_item['product_quantity'] -= int(request.form['product_quantity'])
                     flash(f"Sorry, we only have {product.xxlarge} XX-Large in stock.")
                     return redirect(url_for('GenProduct', product_id=product_id))
                 # if user adds amount of quantity to cart that is acceptable based on inventory levels add it to cart
                 if found_item['size'] == size:
                     flash(f"{product.item_name} has been successfully added to your cart.", 'success')
                     product_quantity += int(request.form['product_quantity'])
                     return redirect(url_for('CheckOut'))
                 # if not, add to cart as a new item
                 else:
                     session['cart'].append(
                         {'product_id': product.product_id, 'item_name': product.item_name, 'size': size,
                         'product_image': product.product_image,
                         'product_quantity': product_quantity, 'price': product.price}
                     )
                     return redirect(url_for('CheckOut'))
        # if item not in cart
        else:
             # let size = size on form
             size = request.form['size']
             if size == 'X-Small':
                 if product_quantity > product.xsmall:
                     # if product is not in stock do not let user order
                     if product.xsmall == 0:
                         flash(f"Sorry, we are out of stock for this size.")
                         return redirect(url_for('GenProduct', product_id=product_id))
                     flash(f"Sorry, we only have {product.xsmall} x-small in-stock.")
                     return redirect(url_for('GenProduct', product_id=product_id))
             if size == 'Small':
                  if product_quantity > product.small:
                      # if product is not in stock do not let user order
                      if product.small == 0:
                             flash(f"Sorry, we are out of stock for this size.")
                             return redirect(url_for('GenProduct', product_id=product_id))
                      flash(f"Sorry, we only have {product.small} small in-stock.")
                      return redirect(url_for('GenProduct', product_id=product_id))
             if size == 'Medium':
                     if product_quantity > product.medium:
                         # if product is not in stock do not let user order
                         if product.medium == 0:
                             flash(f"Sorry, we are out of stock for this size.")
                             return redirect(url_for('GenProduct', product_id=product_id))
                         flash(f"Sorry, we only have {product.medium} medium in-stock.")
                         return redirect(url_for('GenProduct', product_id=product_id))
             if size == 'Large':
                    if product_quantity > product.large:
                         # if product is not in stock do not let user order
                         if product.large == 0:
                             flash(f"Sorry, we are out of stock for this size.")
                             return redirect(url_for('GenProduct', product_id=product_id))
                         flash(f"Sorry, we only have {product.large} large in-stock.")
                         return redirect(url_for('GenProduct', product_id=product_id))
             if size == 'X-Large':
                     if product_quantity > product.xlarge:
                         # if product is not in stock do not let user order
                         if product.xlarge == 0:
                             flash(f"Sorry, we are out of stock for this size.")
                             return redirect(url_for('GenProduct', product_id=product_id))
                         flash(f"Sorry, we only have {product.xlarge} x-large in-stock.")
                         return redirect(url_for('GenProduct', product_id=product_id))
             if size == 'XX-Large':
                     if product_quantity > product.xxlarge:
                         # if product is not in stock do not let user order
                         if product.xxlarge == 0:
                             flash(f"Sorry, we are out of stock for this size.")
                             return redirect(url_for('GenProduct', product_id=product_id))
                         flash(f"Sorry, we only have {product.xxlarge} xx-large in-stock.")
                         return redirect(url_for('GenProduct', product_id=product_id))

             size = request.form['size']

             session['cart'].append(
                {'product_id': product.product_id, 'item_name': product.item_name, 'size':size, 'product_image':product.product_image,
                 'product_quantity': product_quantity, 'price': product.price}
             )

        session['cart_total'] = sum(item['price']*item['product_quantity'] for item in session['cart'])

        flash(f"{product.item_name} has been successfully added to your cart.", 'success')
        return redirect(url_for('CheckOut'))
    else:
        flash(f'Product could not be found. Please contact support if this problem persists.', 'error')

# establish route to remove item from cart
@app.route('/cart/remove/<int:index>', methods=['GET'])
@login_required
def cart_remove(index):
   if 'cart' in session:
       # remove item from cart
       if index < len(session['cart']):
           item_name = session['cart'][index]['item_name']
           session['cart'].pop(index)
           flash(f"{item_name} has been successfully removed from your cart.", 'success')

       else:
           flash(f'Product is not in the cart and could not be removed.', 'error')

   session['cart_total'] = sum(item['price'] * item['product_quantity'] for item in session['cart'])

   return redirect(url_for('CheckOut'))

# show all the collections in a route
@app.route('/CollectionsLog')
@login_required
@role_required(['ADMIN', 'EMPLOYEE'])
def collections_view_all():
    collection = Collections.query.order_by(Collections.collection_id) \
        .all()
    return render_template('collectionsLog.html', collection=collection)

# allow user to input new collections
@app.route('/CollectionsInput', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN', 'EMPLOYEE'])
def collections_entry():
    if request.method == 'GET':
        return render_template('inputCollections.html', action='create')
    # update collections if user inputs new collection
    elif request.method == 'POST':
        collection_name = request.form['collection_name']

        collection = Collections(collection_name=collection_name)

        db.session.add(collection)
        db.session.commit()
        flash(f'{collection_name} was successfully added!', 'success')
        return redirect(url_for('collections_view_all'))

    flash(f'Invalid request. Please contact support if this problem persists.', 'error')
    return redirect(url_for('homePage'))

# allow user to edit collections
@app.route('/CollectionsLog/Update/<int:collection_id>', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN', 'EMPLOYEE'])
def collection_edit(collection_id):
    if request.method == 'GET':
        collection = Collections.query.filter_by(collection_id=collection_id).first()

        if collection:
            return render_template('inputCollections.html', collection_id=collection_id, collection=collection, action='update')

        else:
            flash(f'Collection attempting to be edited could not be found!', 'error')

    elif request.method == 'POST':
        collection = Collections.query.filter_by(collection_id=collection_id).first()
        # allow user to update collections and add to database
        if collection:
            collection.collection_name = request.form['collection_name']

            db.session.commit()
            flash(f'{collection.collection_name} was successfully updated!', 'success')
        else:
            flash(f'Collection attempting to be edited could not be found!', 'error')

        return redirect(url_for('collections_view_all'))

    flash(f'Invalid request. Please contact support if this problem persists.', 'error')
    return redirect(url_for('collections_view_all'))

# let user delete collections
@app.route('/CollectionsLog/Delete/<int:collection_id>')
@login_required
@role_required(['ADMIN'])
def collection_delete(collection_id):
    collection = Collections.query.filter_by(collection_id=collection_id).first()
    # let user delete collection if it exists
    if collection:
        db.session.delete(collection)
        db.session.commit()
        flash(f'{collection_id} was successfully deleted!', 'success')
    # if collection does not exist do not let user delete something
    else:
        flash(f'Delete failed! Collection could not be found.', 'error')

    return redirect(url_for('collections_view_all'))


if __name__ == '__main__':
   app.run()
