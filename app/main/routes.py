import sqlalchemy as sa
from flask import render_template, flash, redirect, url_for
from app import db
from app.main import bp
from app.main.forms import AddAlbumForm, EditArtistForm, EditAlbumForm, EditTrackForm
from app.models import Artist, Album, Track, Genre


@bp.route("/", methods=["GET"])
@bp.route("/index", methods=["GET"])
def index():
    return render_template("index.html", title="Home")


@bp.route("/artists", methods=["GET"])
def artists():

    artists = db.session.scalars(sa.select(Artist).order_by(Artist.name)).all()

    return render_template("artists.html", title="Artists", artists=artists)


@bp.route("/artist_details/<int:artist_id>", methods=["GET"])
def artist_details(artist_id):

    artist = db.session.scalar(sa.Select(Artist).where(Artist.id == artist_id))
    albums = db.session.scalars(
        sa.Select(Album).where(Album.artist_id == artist_id).order_by(Album.year)
    ).all()

    if not artist:
        flash("Artist not found.")
        return redirect(url_for("main.artists"))

    return render_template(
        "artist_details.html", title=artist.name, artist=artist, albums=albums
    )


@bp.route("/edit_artist/<int:artist_id>", methods=["GET", "POST"])
def edit_artist(artist_id):

    artist = db.session.scalar(sa.Select(Artist).where(Artist.id == artist_id))

    if not artist:
        flash("Artist not found.")
        return redirect(url_for("main.artists"))

    form = EditArtistForm(obj=artist)

    if form.validate_on_submit():
        artist.name = form.name.data
        artist.country = form.country.data
        artist.year_of_founding = form.year_of_founding.data
        artist.notes = form.notes.data

        db.session.commit()

        flash("Artist updated.")

        return redirect(url_for("main.artist_details", artist_id=artist.id))

    return render_template(
        "edit_artist.html", title=f"Edit {artist.name}", form=form, artist=artist
    )


@bp.route("/albums", methods=["GET"])
def albums():

    albums = db.session.scalars(sa.select(Album).order_by(Album.id.desc())).all()

    return render_template("albums.html", title="Albums", albums=albums)


@bp.route("/add_album", methods=["GET", "POST"])
def add_album():

    form = AddAlbumForm()

    artists = db.session.scalars(sa.select(Artist).order_by(Artist.name)).all()
    genres = db.session.scalars(sa.select(Genre).order_by(Genre.name)).all()

    form.existing_artist.choices = [(0, "Select Artist")] + [
        (artist.id, artist.name) for artist in artists
    ]
    form.existing_genre.choices = [(0, "Select Genre")] + [
        (genre.id, genre.name) for genre in genres
    ]

    if form.validate_on_submit():

        if form.new_artist.data and form.existing_artist.data == 0:
            artist = Artist(name=form.new_artist.data)
            db.session.add(artist)
            db.session.flush()

        elif form.existing_artist.data != 0 and not form.new_artist.data:
            artist = db.session.get(Artist, form.new_artist.data)

        else:
            flash(
                "You can either enter a new artist or select one from the list of existing artists."
            )

        if form.new_genre.data and form.existing_genre.data == 0:
            genre = Genre(name=form.new_genre.data)
            db.session.add(genre)
            db.session.flush()

        elif form.existing_genre.data != 0 and not form.existing_genre.data:
            genre = db.session.get(Genre, form.existing_genre.data)

        else:
            flash(
                "You can either enter a new genre or select one from the list of existing genres."
            )

        new_album = Album(
            title=form.album_name.data,
            artist=artist,
            year=form.year.data,
            label=form.label.data,
            format=form.format.data,
            discogs_id=form.discogs_id.data,
            notes=form.notes.data,
        )

        if genre:
            new_album.genres.append(genre)

        db.session.add(new_album)
        db.session.commit()

        flash("The album has been added to the database.")

        return redirect(url_for("main.albums"))

    return render_template("add_album.html", title="Add Album", form=form)


@bp.route("/album_details/<int:album_id>", methods=["GET"])
def album_details(album_id):

    album = db.session.scalar(sa.Select(Album).where(Album.id == album_id))
    tracks = db.session.scalars(sa.select(Track).where(Track.album_id == album_id))

    if not album:
        flash("Album not found.")
        return redirect(url_for("main.albums"))

    return render_template(
        "album_details.html", title=album.title, tracks=tracks, album=album
    )


@bp.route("/edit_album/<int:album_id>", methods=["GET", "POST"])
def edit_album(album_id):

    album = db.session.scalar(sa.select(Album).where(Album.id == album_id))

    if not album:
        flash("Album not found.")
        return redirect(url_for("main.albums"))

    form = EditAlbumForm(obj=album)

    if form.validate_on_submit():
        album.title = form.title.data
        album.year = form.year.data
        album.format = form.format.data
        album.label = form.label.data
        album.notes = form.notes.data

        db.session.commit()

        flash("Album updated.")

        return redirect(url_for("main.album_details", album_id=album.id))

    return render_template("edit_album.html", title=album.title, form=form, album=album)


@bp.route("/add_tracks/<int:album_id>", methods=["GET", "POST"])
def add_tracks(album_id):

    album = db.session.scalar(sa.select(Album).where(Album.id == album_id))
    tracks = db.session.scalars(sa.select(Track).where(Track.album_id == album_id))

    form = EditTrackForm()

    if form.validate_on_submit():
        new_track = Track(
            title=form.title.data,
            track_number=form.track_number.data,
            duration_seconds=form.duration_seconds.data,
            album_id=album_id,
        )

        db.session.add(new_track)
        db.session.commit()

        flash("New track added to album.")

        return redirect(url_for("main.add_tracks", album_id=album.id))

    return render_template(
        "add_tracks.html",
        title=f"{album.title} - Add Tracks",
        album=album,
        tracks=tracks,
        form=form,
    )


@bp.route("/edit_tracks/<int:track_id>", methods=["GET", "POST"])
def edit_track(track_id):

    track = db.session.scalar(sa.select(Track).where(Track.id == track_id))

    form = EditTrackForm(obj=track)

    if form.validate_on_submit():
        track.title = form.title.data
        track.track_number = form.track_number.data
        track.duration_seconds = form.duration_seconds.data

        db.session.commit()

        flash("Tracks updated.")

        return redirect(url_for("main.album_details", album_id=track.album_id))

    return render_template("edit_track.html", title="Edit Tracks", form=form, track=track)