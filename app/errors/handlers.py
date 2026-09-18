from flask import render_template, flash
from app import db
from app.errors import bp
from app.errors import exceptions


@bp.app_errorhandler(400)
def not_found_error(error):

    return render_template("errors/404.html"), 404


@bp.app_errorhandler(500)
def internal_error(error):

    db.session.rollback()
    return render_template("errors/500.html"), 500

@bp.app_errorhandler(exceptions.NoDataError)
def no_data_error(error):

    return render_template("errors/no_discogs_data.html")