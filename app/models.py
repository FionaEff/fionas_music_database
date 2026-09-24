from typing import Optional
from enum import Enum
from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so


class AlbumFormat(Enum):
    vinyl = "vinyl"
    cd = "cd"
    digital = "digital"


album_genres = sa.Table(
    "album_genres",
    db.metadata,
    sa.Column(
        "album_id",
        sa.ForeignKey("album.id", name="fk_album_genres_album_id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sa.Column(
        "genre_id",
        sa.ForeignKey("genre.id", name="fk_album_genres_genre_id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Artist(db.Model):
    __tablename__ = "artist"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    country: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    year_of_founding: so.Mapped[Optional[int]] = so.mapped_column(
        sa.SmallInteger, index=True
    )
    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    albums: so.Mapped[list["Album"]] = so.relationship(back_populates="artist")


class Album(db.Model):
    __tablename__ = "album"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    discogs_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, unique=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    year: so.Mapped[Optional[int]] = so.mapped_column(sa.SmallInteger)
    format: so.Mapped[AlbumFormat] = so.mapped_column(
        sa.Enum(AlbumFormat, name="album_format")
    )
    label: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    cover_path: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))
    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    artist_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Artist.id), index=True)

    artist: so.Mapped["Artist"] = so.relationship(back_populates="albums")
    tracks: so.Mapped[list["Track"]] = so.relationship(
        back_populates="album", cascade="all, delete-orphan"
    )
    genres: so.Mapped[list["Genre"]] = so.relationship(
        secondary=album_genres, back_populates="albums"
    )


class Track(db.Model):
    __tablename__ = "track"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
    track_number: so.Mapped[int] = so.mapped_column(sa.SmallInteger)
    duration_seconds: so.Mapped[int] = so.mapped_column(sa.SmallInteger)

    album_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Album.id), index=True)

    album: so.Mapped["Album"] = so.relationship(back_populates="tracks")


class Genre(db.Model):
    __tablename__ = "genre"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    albums: so.Mapped[list["Album"]] = so.relationship(
        secondary=album_genres, back_populates="genres"
    )
