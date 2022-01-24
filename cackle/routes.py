from cackle import app, db
from flask import render_template, flash, redirect, url_for
from cackle.forms import LoginForm, SignupForm
from flask_login import current_user, login_user, logout_user, login_required
from cackle.models import User, Post
from datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/home')
@login_required
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
        login_user(user, remember=form.remember_me.data)
        flash('Logged in successfully', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts
    return render_template('user.html', user=user, posts=posts)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():        
        user = User(username=form.username.data)
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You successfully created an account', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

# verifying my secret key
@app.route('/verify')
def verify():
    return '<p>{}</p>'.format(app.config['SECRET_KEY'])