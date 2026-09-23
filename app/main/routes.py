import sqlalchemy as sa
import os
from flask import render_template, flash, redirect, url_for
from app import db
from app.main import bp
from app.main.forms import (
    AddAlbumForm,
    EditArtistForm,
    EditAlbumForm,
    EditTrackForm,
    AddArtistForm,
)
from app.models import Artist, Album, Track, Genre
from app.services import api


def create_folder(artist_name):

    album_cover_path = "./app/static/album_cover/"

    if not os.path.exists(album_cover_path + artist_name.replace(" ", "_")):
        os.makedirs(album_cover_path + artist_name.replace(" ", "_"))


def rename_folder(artist_name, new_artist_name):

    album_cover_path = "./app/static/album_cover/"

    if os.path.exists(album_cover_path + artist_name):
        os.rename(
            album_cover_path + artist_name,
            album_cover_path + new_artist_name,
        )


@bp.route("/", methods=["GET"])
@bp.route("/index", methods=["GET"])
def index():

    albums = db.session.scalars(sa.select(Album).order_by(Album.id.desc()).limit(5))

    return render_template("index.html", title="Home", albums=albums)


@bp.route("/artists", methods=["GET"])
def artists():

    artists = db.session.scalars(sa.select(Artist).order_by(Artist.name)).all()

    return render_template("artists.html", title="Artists", artists=artists)


@bp.route("/artist_details/<int:artist_id>", methods=["GET"])
def artist_details(artist_id):

    artist = db.session.scalar(sa.select(Artist).where(Artist.id == artist_id))
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

    artist = db.session.scalar(sa.select(Artist).where(Artist.id == artist_id))
    artist_name = artist.name

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

        if artist.name != artist_name:
            rename_folder(
                artist_name.lower().replace(" ", "_"),
                artist.name.lower().replace(" ", "_"),
            )

        flash("Artist updated.")

        return redirect(url_for("main.artist_details", artist_id=artist.id))

    return render_template(
        "edit_artist.html", title=f"Edit {artist.name}", form=form, artist=artist
    )


@bp.route("/add_artist", methods=["Get", "POST"])
def add_artist():

    form = AddArtistForm()

    if form.validate_on_submit():
        new_artist = Artist(
            name=form.name.data,
            country=form.country.data,
            year_of_founding=form.year_of_founding.data,
            notes=form.notes.data,
        )

        db.session.add(new_artist)
        db.session.commit()

        create_folder(new_artist.name.lower().replace(" ", "_"))

        flash("The artist has been added.")

        return redirect(url_for("main.artist_details", artist_id=new_artist.id))

    return render_template("add_artist.html", title="Add Artist", form=form)


@bp.route("/artists/<int:artist_id>/delete", methods=["GET", "POST"])
def delete_artist(artist_id):

    artist = db.session.scalar(sa.select(Artist).where(Artist.id == artist_id))

    if not artist:
        flash("Artist not found.")
        return redirect(url_for("main.artists"))

    if artist.albums:
        flash("Cannot delete an artist with existing albums.")
        return redirect(url_for("main.albums"))

    db.session.delete(artist)
    db.session.commit()

    flash("Artist deleted.")

    return redirect(url_for("main.artists"))


@bp.route("/albums", methods=["GET"])
def albums():

    albums = db.session.scalars(sa.select(Album).order_by(Album.id.desc())).all()

    return render_template("albums.html", title="Albums", albums=albums)


@bp.route("/add_album", methods=["GET", "POST"])
def add_album():

    artist = None
    genre = None

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
            if any(
                form.new_artist.data in artist
                for artist in form.existing_artist.choices
            ):
                flash(
                    "Artist already exists, please select them from the existing artist list."
                )

                return render_template("add_album.html", title="Add Album", form=form)

            else:
                artist = Artist(name=form.new_artist.data)
                db.session.add(artist)
                db.session.flush()
                create_folder(artist.name.lower())

        elif form.existing_artist.data != 0 and not form.new_artist.data:
            artist = db.session.get(Artist, form.existing_artist.data)

        elif not form.new_artist.data and form.existing_artist == 0:
            flash(
                "Please enter a new artist or select one from the existing artist list."
            )

            return render_template("add_album.html", title="Add Album", form=form)

        else:
            flash(
                "You can either enter a new artist or select one from the list of existing artists."
            )

            return render_template("add_album.html", title="Add Album", form=form)

        if form.new_genre.data and form.existing_genre.data == 0:
            if any(
                form.new_genre.data in genre for genre in form.existing_genre.choices
            ):
                flash(
                    "Genre already exists, please select it from the existing genre list."
                )

                return render_template("add_album.html", title="Add Album", form=form)

            else:
                genre = Genre(name=form.new_genre.data)
                db.session.add(genre)
                db.session.flush()

        elif form.existing_genre.data != 0 and not form.new_genre.data:
            genre = db.session.get(Genre, form.existing_genre.data)

        elif not form.new_genre.data and form.existing_genre == 0:
            flash(
                "Please eneter a new genre or select one from the existing genre list."
            )

            return render_template("add_album.html", title="Add Album", form=form)

        else:
            flash(
                "You can either enter a new genre or select one from the list of existing genres."
            )

            return render_template("add_album.html", title="Add Album", form=form)

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
        db.session.flush()

        if form.discogs_id.data:
            release_details = api.get_release_details(str(form.discogs_id.data))

            if not release_details:
                flash("No Discogs data found.")
                return redirect(url_for("main.add_album"))

            if release_details["title"] != form.album_name.data:
                flash("Discogs ID doens't match album title.")
                return render_template("add_album.html", title="Add Album", form=form)

            new_album.title = release_details["title"]
            new_album.year = release_details["year"]
            new_album.label = release_details["labels"][0]["name"]

            track_number = 1

            for track in release_details["tracklist"]:
                if track["duration"]:
                    minutes = track["duration"].split(":")
                    duration = int(minutes[0]) * 60 + int(minutes[1])
                else:
                    duration = 0

                new_track = Track(
                    title=track["title"],
                    track_number=track_number,
                    duration_seconds=duration,
                    album_id=new_album.id,
                )

                track_number += 1

                db.session.add(new_track)
                db.session.flush()

            cover_path = f"./app/static/album_cover/{new_album.artist.name.lower().replace(" ", "_")}/{new_album.title.lower().replace(" ", "_")}.jpg"
            cover_url = f"{release_details["images"][0]["resource_url"]}"
            cover_image = api.download_cover_image(cover_url)

            if cover_image:
                with open(cover_path, "wb") as file:
                    file.write(cover_image)

                    new_album.cover_path = f"album_cover/{new_album.artist.name.lower().replace(" ", "_")}/{new_album.title.lower().replace(" ", "_")}.jpg"

        db.session.commit()

        flash("The album has been added.")

        return redirect(url_for("main.album_details", album_id=new_album.id))

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
        album.discogs_id = form.discogs_id.data
        album.notes = form.notes.data

        if form.discogs_id.data:
            # if album.discogs_id != form.discogs_id.data:
            release_details = api.get_release_details(str(form.discogs_id.data))

            if not release_details:
                flash("No Discogs data found.")
                return redirect(url_for("main.edit_album", album_id=album_id))

            if release_details["title"] != form.title.data:
                flash("Discogs ID doens't match album title.")
                return redirect(url_for("main.edit_album", album_id=album_id))

            album.title = release_details["title"]
            album.year = release_details["year"]
            album.label = release_details["labels"][0]["name"]

            track_number = 1

            for track in release_details["tracklist"]:
                if track["duration"]:
                    minutes = track["duration"].split(":")
                    duration = int(minutes[0]) * 60 + int(minutes[1])
                else:
                    duration = 0

                new_track = Track(
                    title=track["title"],
                    track_number=track_number,
                    duration_seconds=duration,
                    album_id=album_id,
                )

                track_number += 1

                db.session.add(new_track)
                db.session.flush()

            cover_path = f"./app/static/album_cover/{album.artist.name.lower().replace(" ", "_")}/{album.title.lower().replace(" ", "_")}.jpg"
            cover_url = f"{release_details["images"][0]["resource_url"]}"
            cover_image = api.download_cover_image(cover_url)

            if cover_image:
                with open(cover_path, "wb") as file:
                    file.write(cover_image)

                    album.cover_path = f"album_cover/{album.artist.name.lower().replace(" ", "_")}/{album.title.lower().replace(" ", "_")}.jpg"

        db.session.commit()

        flash("Album updated.")

        return redirect(url_for("main.album_details", album_id=album.id))

    return render_template("edit_album.html", title=album.title, form=form, album=album)


@bp.route("/albums/<int:album_id>/delete", methods=["GET", "POST"])
def delete_album(album_id):

    album = db.session.scalar(sa.select(Album).where(Album.id == album_id))

    if not album:
        flash("Album not found.")
        return redirect(url_for("main.albums"))

    db.session.delete(album)
    db.session.commit()

    flash("Album deleted.")

    return redirect(url_for("main.albums"))


@bp.route("/tracks/<int:album_id>", methods=["GET", "POST"])
def tracks(album_id):

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

        return redirect(url_for("main.tracks", album_id=album.id))

    return render_template(
        "tracks.html",
        title=f"{album.title} - Add Tracks",
        album=album,
        tracks=tracks,
        form=form,
    )


@bp.route("/edit_track/<int:track_id>", methods=["GET", "POST"])
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

    return render_template(
        "edit_track.html", title="Edit Tracks", form=form, track=track
    )


@bp.route("/tracks/<int:track_id>/delete", methods=["GET", "POST"])
def delete_track(track_id):

    track = db.session.scalar(sa.select(Track).where(Track.id == track_id))

    if not track:
        flash("Track not found.")
        return redirect(url_for("main.tracks", album_id=track.album_id))

    db.session.delete(track)
    db.session.commit()

    flash("Track deleted.")

    return redirect(url_for("main.tracks", album_id=track.album_id))
