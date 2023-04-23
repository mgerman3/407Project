import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
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


@login_manager.user_loader
def load_user(account_id):
   return Credentials.query.get(account_id)

@app.route('/')
def homePage():
    return render_template('Home Page.html')

@app.route('/Shop')
def Shop():
    return render_template('Shop.html')

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
    if request.method == 'POST':
        return render_template('RequestForm.html', form_submitted=True)
    else:
        return render_template('RequestForm.html')

@app.route('/Reviews', methods=['GET', 'POST'])
def Reviews():
    if request.method == 'POST':
        return render_template('Reviews.html', form_submitted=True)
    else:
        return render_template('Reviews.html')

@app.route('/LogIn', methods = ['GET', 'POST'])
# def LogInScreen():
#     if request.method == 'POST':
#         return render_template('Log-In-Screen.html', form_submitted=True)
#     else:
#         return render_template('Log-In-Screen.html')
def LogIn():
   default_route_function = 'Shop'
   default_student_route_function = 'homePage'


   if request.method == 'GET':
       # Determine where to redirect user if they are already logged in
       if current_user and current_user.is_authenticated:
           if current_user.role in ['MANAGER', 'ADMIN']:
               return redirect(url_for(default_route_function))
           elif current_user.role == 'STUDENT':
               return redirect(url_for(default_student_route_function, user_id=0))
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

           if current_user.role in ['MANAGER', 'ADMIN']:
               return redirect(redirect_route if redirect_route else url_for(default_route_function))
           elif current_user.role == 'STUDENT':
               return redirect(redirect_route if redirect_route else url_for(default_student_route_function, user_id=0))
       else:
           flash(f'Your login information was not correct. Please try again.', 'error')

       return redirect(url_for('LogIn'))

   return redirect(url_for('LogIn'))


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

@app.route('/InventoryInput', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN', 'MANAGER'])
def inventory_entry():
   if request.method == 'GET':
       return render_template('Input_Inventory.html', action='create')
   elif request.method == 'POST':
       item_name = request.form['item_name']
       xsmall = request.form['xsmall']
       small = request.form['small']
       medium = request.form['medium']
       large = request.form['large']
       xlarge = request.form['xlarge']
       xxlarge = request.form['xxlarge']
       color = request.form['color']
       price = request.form['price']
       description = request.form['desc']

       items = Inventory(item_name=item_name, xsmall=xsmall, small=small, medium=medium, large=large, xlarge=xlarge,
                         xxlarge=xxlarge, color=color, price=price, description=description)

       db.session.add(items)
       db.session.commit()
       flash(f'{items} was successfully added!', 'success')
       return redirect(url_for('homePage'))


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

@app.route('/signup')
def SignUp():
    if request.method == 'GET':
        return render_template('sign-up-page.html')

    elif request.method == 'POST':
       username = request.form['username']
       password = request.form['password']
       first_name = request.form['first_name']
       last_name = request.form['last_name']
       email = request.form['email']

       users = User(first_name=first_name, last_name=last_name, email=email)
       user_credentials = Credentials(username=username, password=password)

       db.session.add(users)
       db.session.add(user_credentials)
       db.session.commit()
       flash(f'{username} was successfully added!', 'success')
       return redirect(url_for('homePage'))


   # Address issue where unsupported HTTP request method is attempted
# flash(f'Invalid request. Please contact support if this problem persists.', 'error')
# return redirect(url_for('SignUp'))

@app.route('/banner')
def Banner():
    return render_template('Banner.html')

@app.route('/cart')
def Cart():
    return render_template('cart.html')

@app.route('/InventoryLog')
def InventoryLog():
    return render_template('Inventory Log.html')

if __name__ == '__main__':
    app.run()
