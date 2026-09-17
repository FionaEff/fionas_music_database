from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Optional


class EmptyForm(FlaskForm):
    submit = SubmitField("Submit")


class AddAlbumForm(FlaskForm):

    album_name = StringField("Album Name", validators=[DataRequired(), Length(max=64)])
    new_artist = StringField("Artist Name", validators=[Length(max=128)])
    existing_artist = SelectField("Select Artist", coerce=int)
    year = IntegerField("Year (Optional)", validators=[Optional()])
    new_genre = StringField("Genre", validators=[Length(max=32)])
    existing_genre = SelectField("Select Genre", coerce=int)
    format = SelectField(
        "Album Format",
        choices=[("vinyl", "Vinyl"), ("cd", "CD"), ("digital", "Digital")],
        validators=[DataRequired()],
    )
    label = StringField("Label (Optional)", validators=[Length(max=64)])
    discogs_id = IntegerField("Discogs ID (Optional)", validators=[Optional()])
    notes = StringField("Notes (Optional)", validators=[Length(max=256)])
    submit = SubmitField("Add Album")


class AddArtistForm(FlaskForm):

    name = StringField("Artist Name", validators=[DataRequired(), Length(max=128)])
    country = StringField("Country (Optional)", validators=[Length(max=64)])
    year_of_founding = IntegerField(
        "Year of Founding (Optional)", validators=[Optional()]
    )
    notes = StringField("Notes (Optional)", validators=[Length(max=256)])
    submit = SubmitField("Add Artist")


class EditArtistForm(FlaskForm):

    name = StringField("Artist Name", validators=[DataRequired(), Length(max=128)])
    country = StringField("Country (Optional)", validators=[Length(max=64)])
    year_of_founding = IntegerField("Founded (Optional)", validators=[Optional()])
    notes = StringField("Notes (Optional)", validators=[Length(max=256)])
    submit = SubmitField("Save Changes")


class EditAlbumForm(FlaskForm):

    title = StringField("Album Name", validators=[DataRequired(), Length(max=64)])
    year = IntegerField("Year (Optional)", validators=[Optional()])
    format = SelectField(
        "Album Format",
        choices=[("vinyl", "Vinyl"), ("cd", "CD"), ("digital", "Digital")],
        validators=[DataRequired()],
    )
    label = StringField("Label (Optional)", validators=[Length(max=64)])
    discogs_id = IntegerField("Discogs ID (Optional)", validators=[Optional()])
    notes = StringField("Notes (Optional)", validators=[Length(max=256)])
    submit = SubmitField("Save Changes")


class EditTrackForm(FlaskForm):

    title = StringField("Title", validators=[DataRequired(), Length(max=128)])
    track_number = IntegerField("Track Number", validators=[DataRequired()])
    duration_seconds = IntegerField(
        "Duration in Seconds (Optional)", validators=[Optional()]
    )
    submit = SubmitField("Save Track")
