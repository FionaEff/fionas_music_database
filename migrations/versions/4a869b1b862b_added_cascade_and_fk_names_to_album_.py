"""added cascade and fk names to album_genres table, changed genre name length to 64

Revision ID: 4a869b1b862b
Revises: 138f91bf4a66
Create Date: 2026-09-24 08:19:50.791457

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4a869b1b862b"
down_revision = "138f91bf4a66"
branch_labels = None
depends_on = None


def upgrade():
    # Recreate album_genres so that the foreign keys can be given
    # names and ON DELETE CASCADE.
    op.create_table(
        "album_genres_new",
        sa.Column("album_id", sa.Integer(), nullable=False),
        sa.Column("genre_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["album_id"],
            ["album.id"],
            name="fk_album_genres_album_id",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["genre_id"],
            ["genre.id"],
            name="fk_album_genres_genre_id",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("album_id", "genre_id"),
    )

    # Copy the existing album/genre assignments.
    op.execute(
        """
        INSERT INTO album_genres_new (album_id, genre_id)
        SELECT album_id, genre_id
        FROM album_genres
        """
    )

    # Replace the old table with the new one.
    op.drop_table("album_genres")

    op.rename_table("album_genres_new", "album_genres")

    # Change genre.name from VARCHAR(32) to VARCHAR(64).
    with op.batch_alter_table("genre", schema=None) as batch_op:
        batch_op.alter_column(
            "name",
            existing_type=sa.VARCHAR(length=32),
            type_=sa.String(length=64),
            existing_nullable=False,
        )


def downgrade():
    # Change genre.name back to VARCHAR(32).
    with op.batch_alter_table("genre", schema=None) as batch_op:
        batch_op.alter_column(
            "name",
            existing_type=sa.String(length=64),
            type_=sa.VARCHAR(length=32),
            existing_nullable=False,
        )

    # Recreate album_genres without named CASCADE foreign keys.
    op.create_table(
        "album_genres_old",
        sa.Column("album_id", sa.Integer(), nullable=False),
        sa.Column("genre_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["album_id"],
            ["album.id"],
        ),
        sa.ForeignKeyConstraint(
            ["genre_id"],
            ["genre.id"],
        ),
        sa.PrimaryKeyConstraint("album_id", "genre_id"),
    )

    # Copy the existing assignments back.
    op.execute(
        """
        INSERT INTO album_genres_old (album_id, genre_id)
        SELECT album_id, genre_id
        FROM album_genres
        """
    )

    # Replace the CASCADE version with the old version.
    op.drop_table("album_genres")

    op.rename_table("album_genres_old", "album_genres")