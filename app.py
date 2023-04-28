import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from authorize import role_required
from models import *

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'ATB2.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'beyond_course_scope'
db.init_app(app)


login_manager = LoginManager()
login_manager.login_view = 'LogIn' # default login route
login_manager.init_app(app)

# Product image parameters
app.config['PRODUCT_UPLOAD_PATH'] = 'static/products'

# Product order restrictions
app.config['MAX_QUANTITY_PER_ITEM'] = 99

@login_manager.user_loader
def load_user(account_id):
   return Credentials.query.get(account_id)

@app.route('/')
def homePage():
    return render_template('Home Page.html')

@app.route('/404')
def errorPage():
    return render_template('Inventory.html'), 404

@app.route('/Shop')
def Shop():
    items = InventoryInfo.query.order_by(InventoryInfo.item_name).all()
    return render_template('Shop.html', items=items)


@app.route('/Inventory')
def Inventory():
    return render_template('Inventory.html')

# @app.route('/EnterItems')
# def EnterItems():
#     return render_template('Input_Inventory.html')

@app.route('/About')
def About():
    return render_template('About Page.html')


@app.route('/profile')
def Profile():
    return render_template('profile.html')

@app.route('/RequestForm', methods=['GET', 'POST'])
def RequestForm():
    if request.method == 'GET':
        return render_template('RequestForm.html', action='create')
    elif request.method == 'POST':

        if current_user.is_authenticated:

            account_id = current_user.account_id
            first_name = None
            last_name = None
            email = None
            message = request.form['message']

            requests = Requests(account_id=account_id, first_name=first_name, last_name=last_name, email=email, message=message)

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

    # Address issue where unsupported HTTP request method is attempted
    flash(f'Invalid request. Please contact support if this problem persists.', 'error')
    return redirect(url_for('homePage'))

@app.route('/RequestsLog/Delete/<int:request_id>')
@login_required
@role_required(['ADMIN'])
def requests_fulfilled(request_id):
   request = Requests.query.filter_by(request_id=request_id).first()
   if request:
       db.session.delete(request)
       db.session.commit()
       flash(f'{request_id} was successfully deleted!', 'success')
   else:
       flash(f'Delete failed! Collection could not be found.', 'error')

   return redirect(url_for('requests_view_all'))

@app.route('/Reviews', methods=['GET', 'POST'])
def Reviews():
    if request.method == 'GET':
        return render_template('Reviews.html', action='create')
    elif request.method == 'POST':

        if current_user.is_authenticated:

            account_id = current_user.account_id
            first_name = None
            last_name = None
            email = None
            review = request.form['review']

            reviews = Reviews(account_id=account_id, first_name=first_name, last_name=last_name, email=email, review=review)

        else:
            account_id = None
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            review = request.form['review']

            reviews = Reviews(account_id=account_id, first_name=first_name, last_name=last_name, email=email, review=review)

        db.session.add(reviews)
        db.session.commit()
        flash(f'Your review was received!', 'success')
        return redirect(url_for('Reviews'))

    # Address issue where unsupported HTTP request method is attempted
    flash(f'Invalid request. Please contact support if this problem persists.', 'error')
    return redirect(url_for('homePage'))

@app.route('/ReviewsLog')
@login_required
@role_required(['ADMIN', 'EMPLOYEE'])
def reviews_view_all():
   # review = Reviews.query.order_by(Reviews.review_id) \
   #     .all()
   return render_template('ReviewsLog.html')

@app.route('/ReviewsLog/Delete/<int:review_id>')
@login_required
@role_required(['ADMIN'])
def review_delete(review_id):
   review = Reviews.query.filter_by(review_id=review_id).first()
   if review:
       db.session.delete(review)
       db.session.commit()
       flash(f'{review_id} was successfully deleted!', 'success')
   else:
       flash(f'Delete failed! Review could not be found.', 'error')

   return redirect(url_for('reviews_view_all'))

@app.route('/LogIn', methods = ['GET', 'POST'])
# def LogInScreen():
#     if request.method == 'POST':
#         return render_template('Log-In-Screen.html', form_submitted=True)
#     else:
#         return render_template('Log-In-Screen.html')
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
           return render_template('Log-In-Screen.html', redirect_route=redirect_route)

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

@app.route('/signup', methods=['GET', 'POST'])
def SignUp():

    if request.method == 'GET':
        return render_template('sign-up-page.html', action='create')

    elif request.method == 'POST':
       username = request.form['username']
       password = request.form['password']
       first_name = request.form['first_name']
       last_name = request.form['last_name']
       email = request.form['email']

       sha_password = generate_password_hash(password, method='sha256', salt_length=8)

       user = Credentials(username=username, password=sha_password, first_name=first_name, last_name=last_name,
                           email=email)

       db.session.add(user)
       db.session.commit()
       login_user(user)
       flash(f'{username} was successfully added!', 'success')
       return redirect(url_for('homePage'))


   # Address issue where unsupported HTTP request method is attempted
# flash(f'Invalid request. Please contact support if this problem persists.', 'error')
# return redirect(url_for('SignUp'))

@app.route('/logout')
@login_required
def logout():
   logout_user()
   flash(f'You have been logged out.', 'success')
   return redirect(url_for('homePage'))

@app.route('/CheckOut', methods=['GET', 'POST'])
def CheckOut():
    if request.method == 'POST':
        # return render_template('CheckoutPage.html', form_submitted=True)
        return render_template('Order Confirmation.html')
    else:
        return render_template('CheckoutPage.html')

@app.route('/GenericProduct')
def GenProduct():
    return render_template('GenericProductPage.html')

@app.route('/RequestsLog')
@login_required
@role_required(['ADMIN', 'EMPLOYEE'])
def requests_view_all():
   requests = Requests.query.order_by(Requests.request_id) \
       .all()
   return render_template('Request Log.html', requests=requests)


@app.route('/InventoryLog')
@login_required
@role_required(['ADMIN', 'MANAGER'])
def items_view_all():
  items = InventoryInfo.query.order_by(InventoryInfo.item_name) \
      .all()
  return render_template('Inventory Log.html', items=items)


@app.route('/InventoryLog/update/<int:product_id>', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN', 'MANAGER'])
def item_edit(product_id):
  if request.method == 'GET':
      item = InventoryInfo.query.filter_by(product_id=product_id).first()


      if item:
          return render_template('Input_Inventory.html', item=item, action='update')

      else:
          flash(f'Item attempting to be edited could not be found!', 'error')

  elif request.method == 'POST':
      item = InventoryInfo.query.filter_by(product_id=product_id).first()

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
          image = request.files['image']

          if('delete_product_image' in request.form or image != '') and 'current_product_image' != '' :
              try:
                os.remove(os.path.join(basedir, app.config['PRODUCT_UPLOAD_PATH'], item.image))
                item.image = ''
              except:
                pass

              filename = secure_filename(item.item_name + '-' + image.filename)

              if image.filename != '':
                  image.save(os.path.join(basedir, app.config['PRODUCT_UPLOAD_PATH'], filename))
                  item.image = filename if image else ''

          db.session.commit()
          flash(f'{item.item_name} was successfully updated!', 'success')
      else:
          flash(f'Item attempting to be edited could not be found!', 'error')

      return redirect(url_for('items_view_all'))


  # Address issue where unsupported HTTP request method is attempted
  flash(f'Invalid request. Please contact support if this problem persists.', 'error')
  return redirect(url_for('items_view_all'))


@app.route('/InventoryLog/delete/<int:product_id>')
@login_required
@role_required(['ADMIN'])
def item_delete(product_id):
  item = InventoryInfo.query.filter_by(product_id=product_id).first()
  if item:
        try:
            os.remove(os.path.join(app.config['PRODUCT_UPLOAD_PATH'], item.image))
        except FileNotFoundError:
            pass
        db.session.delete(item)
        db.session.commit()
        flash(f'{item} was successfully deleted!', 'success')
  else:
        flash(f'Delete failed! Item could not be found.', 'error')

  return redirect(url_for('items_view_all'))

@app.route('/InventoryInput', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN', 'MANAGER'])
def inventory_entry():

  collections = Collections.query.order_by(Collections.collection_id) \
        .all()

  if request.method == 'GET':
      return render_template('Input_Inventory.html', action='create', collections=collections)
  elif request.method == 'POST':
      item_name = request.form['item_name']
      xsmall = request.form['xsmall']
      small = request.form['small']
      medium = request.form['medium']
      large = request.form['large']
      xlarge = request.form['xlarge']
      xxlarge = request.form['xxlarge']
      price = request.form['price']
      desc = request.form['desc']
      image = request.files['image']
      filename = secure_filename(item_name + '-' + image.filename)

      if image.filename != '':
          image.save(os.path.join(basedir, app.config['PRODUCT_UPLOAD_PATH'], filename))

      items = InventoryInfo(item_name=item_name, xsmall=xsmall, small=small, medium=medium, large=large, xlarge=xlarge,
                        xxlarge=xxlarge, price=price, desc=desc, image=filename if image else '')

      db.session.add(items)
      db.session.commit()
      flash(f'{item_name} was successfully added!', 'success')
      return redirect(url_for('items_view_all'))




  # Address issue where unsupported HTTP request method is attempted
  flash(f'Invalid request. Please contact support if this problem persists.', 'error')
  return redirect(url_for('homePage'))



@app.route('/OrderConfirm')
def OrderConfirm():
    return render_template('Order Confirmation.html')

@app.route('/OrderDetails')
def OrderDetails():
    return render_template('OrderDetails.html')


@app.route('/SalesTracker')
def SalesTracker():
    return render_template('Sales Tracker.html')



@app.route('/banner')
def Banner():
    return render_template('Banner.html')

@app.route('/Admin/Create/LogIn', methods=['GET', 'POST'])
def Admin_Login():

    if request.method == 'GET':
        return render_template('Admin_Login.html', action='create')

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

@app.route('/cart')
def Cart():
    return render_template('cart.html')

@app.route('/CollectionsLog')
@login_required
@role_required(['ADMIN', 'EMPLOYEE'])
def collections_view_all():
   collection = Collections.query.order_by(Collections.collection_id) \
       .all()
   return render_template('Collections Log.html', collection=collection)

@app.route('/CollectionsInput', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN', 'EMPLOYEE'])
def collections_entry():
   if request.method == 'GET':
       return render_template('Input_Collections.html', action='create')
   elif request.method == 'POST':
       collection_name = request.form['collection_name']

       collection = Collections(collection_name=collection_name)

       db.session.add(collection)
       db.session.commit()
       flash(f'{collection_name} was successfully added!', 'success')
       return redirect(url_for('collections_view_all'))

   # Address issue where unsupported HTTP request method is attempted
   flash(f'Invalid request. Please contact support if this problem persists.', 'error')
   return redirect(url_for('homePage'))

@app.route('/CollectionsLog/Update/<int:collection_id>', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN', 'EMPLOYEE'])
def collection_edit(collection_id):
   if request.method == 'GET':
       collection = Collections.query.filter_by(collection_id=collection_id).first()

       if collection:
           return render_template('Input_Collections.html', collection=collection, action='update')

       else:
           flash(f'Collection attempting to be edited could not be found!', 'error')

   elif request.method == 'POST':
       collection = Collections.query.filter_by(collection_id=collection_id).first()

       if collection:
           collection.collection_id = request.form['collection_id']

           db.session.commit()
           flash(f'{collection.collection_id} was successfully updated!', 'success')
       else:
           flash(f'Collection attempting to be edited could not be found!', 'error')


       return redirect(url_for('collections_view_all'))


   # Address issue where unsupported HTTP request method is attempted
   flash(f'Invalid request. Please contact support if this problem persists.', 'error')
   return redirect(url_for('collections_view_all'))


@app.route('/CollectionsLog/Delete/<int:collection_id>')
@login_required
@role_required(['ADMIN'])
def collection_delete(collection_id):
   collection = Collections.query.filter_by(collection_id=collection_id).first()
   if collection:
       db.session.delete(collection)
       db.session.commit()
       flash(f'{collection_id} was successfully deleted!', 'success')
   else:
       flash(f'Delete failed! Collection could not be found.', 'error')

   return redirect(url_for('collections_view_all'))

if __name__ == '__main__':
    app.run()


# @errors.app_errorhandler(404)
# def error_404(error):
#     return render_template('errors/404.html'), 404
#
# @errors.app_errorhandler(403)
# def error_403(error):
#     return render_template('errors/403.html'), 403
#
# @errors.app_errorhandler(500)
# def error_500(error):
#     return render_template('errors/500.html'), 500





