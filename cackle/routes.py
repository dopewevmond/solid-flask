from cackle import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('navbar.html')