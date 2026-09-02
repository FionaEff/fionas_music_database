import sqlalchemy as sa
from flask import render_template, flash, redirect, url_for
from app import db
from app.main import bp
from app.models import Artist, Album, Track, Genre


@bp.route("/", methods=["GET"])
@bp.route("/index", methods=["GET"])
def index():
    return render_template("index.html", title="Home")


@bp.route("/albums", methods=["GET"])
def albums():

    albums = db.session.scalars(sa.select(Album)).all()

    return render_template("albums.html", title="Albums", albums=albums)


@bp.route("/artists", methods=["GET"])
def artists():

    artists = db.session.scalars(sa.select(Artist)).all()

    return render_template("artists.html", title="Artists", artists=artists)


@bp.route("/add_album", methods=["GET", "POST"])
def add_album():
    return render_template("add_album.html", title="Add Album")
