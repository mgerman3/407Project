from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def homePage():
    return render_template('Home Page.html')

@app.route('/Shop')
def Shop():
    return render_template('Shop.html')

@app.route('/About')
def About():
    return render_template('About Page.html')

@app.route('/ContactUs')
def ContactUsPage():
    return render_template('Contact Us Page.html')

@app.route('/login', methods = ['GET', 'POST'])
def LogInScreen():
    if request.method == 'POST':
        return render_template('Log-In-Screen.html', form_submitted=True)
    else:
        return render_template('Log-In-Screen.html')

@app.route('/CheckOut')
def CheckOut():
    return render_template('CheckoutPage.html')

@app.route('/GenericProduct')
def GenProduct():
    return render_template('GenericProductPage.html')

@app.route('/Inventory')
def Inventory():
    return render_template('Inventory Management.html')

@app.route('/OrderConfim')
def OrderConfirm():
    return render_template('Order Confirmation.html')

@app.route('/OrderDetails')
def OrderDetails():
    return render_template('OrderDetails.html')


@app.route('/SalesTracker')
def SalesTracker():
    return render_template('Sales Tracker.html')

@app.route('/signup', methods = ['GET', 'POST'])
def SignUp():
    if request.method == 'POST':
        return render_template('sign-up-page.html', form_submitted=True)
    else:
        return render_template('sign-up-page.html')

@app.route('/banner')
def Banner():
    return render_template('Banner.html')


if __name__ == '__main__':
    app.run()
