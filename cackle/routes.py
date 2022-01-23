from cackle import app
from flask import render_template, flash, redirect, url_for
from cackle.forms import LoginForm
from flask_login import current_user, login_user
from cackle.models import User, Post

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if user is already logged in, redirect to index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        flash('Logged in successfully', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

# verifying my secret key
@app.route('/verify')
def verify():
    return '<p>{}</p>'.format(app.config['SECRET_KEY'])