from cackle import app
from flask import render_template, flash

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    flash('You need to login', 'danger')
    return render_template('login.html')

# verifying my secret key
@app.route('/verify')
def verify():
    return '<p>{}</p>'.format(app.config['SECRET_KEY'])