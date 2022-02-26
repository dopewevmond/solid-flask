from flask import render_template
from cackle import db
from cackle.errors import bp

@bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors/error.html', type='404'), 404

@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/error.html', type='500'), 500