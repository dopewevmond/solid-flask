from email import message
from flask import render_template
from cackle import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', type='404'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', type='500'), 500