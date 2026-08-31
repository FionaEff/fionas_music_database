import sqlalchemy as sa
from flask import render_template, flash, redirect, url_for
from app import db
from app.main import bp


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html", title="Home")


@bp.route("/albums", methods=["GET"])
def albums():
    return render_template("albums.html", title="Albums")


@bp.route("/artists", methods=["GET"])
def artists():
    return render_template("artists.html", title="Artists")


@bp.route("/add_album", methods=["GET", "POST"])
def add_album():
    return render_template("add_albums.html", title="Add Album")
