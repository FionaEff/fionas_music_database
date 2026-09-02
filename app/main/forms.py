from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length


class EmptyForm(FlaskForm):
    submit = SubmitField("Submit")


class AddAlbumForm(FlaskForm):

    album_name = StringField("Album Name", validators=[DataRequired(), Length(max=64)])
    new_artist = StringField(
        "Artist Name", validators=[DataRequired(), Length(max=128)]
    )
    existing_artist = SelectField("Select Artist", coerce=int)
    year = IntegerField("Year (Optional)")
    new_genre = StringField("Genre", validators=[DataRequired(), Length(max=32)])
    existing_genre = SelectField("Select Genre", coerce=int)
    format = SelectField(
        "Album Format",
        choices=[("vinyl", "Vinyl"), ("cd", "CD"), ("digital", "Digital")],
        validators=[DataRequired()],
    )
    label = StringField("Label (Optional)", validators=[Length(max=64)])
    discogs_id = IntegerField("Discogs ID")
    notes = StringField("Notes (Optional)", validators=[Length(max=256)])
    submit = SubmitField("Add Album")
