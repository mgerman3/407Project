from flask import Flask, render_template

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

@app.route('/LogIn')
def LogInScreen():
    return render_template('Log-In-Screen.html')

if __name__ == '__main__':
    app.run()
