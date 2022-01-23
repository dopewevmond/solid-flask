from cackle import app
from flask import render_template, flash, redirect, url_for
from cackle.forms import LoginForm

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for {}, remember me={}'.format(form.username.data, form.remember_me.data), 'success')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

# verifying my secret key
# @app.route('/verify')
# def verify():
#     return '<p>{}</p>'.format(app.config['SECRET_KEY'])