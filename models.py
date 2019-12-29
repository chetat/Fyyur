# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
from . import db
from . import create_app
from datetime import datetime
from . import config

# DONE: connect to a local postgresql database

app = create_app(config)

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

Shows = db.Table("Shows",
                 db.Column("id", db.Integer, primary_key=True),
                 db.Column("artist_id", db.Integer, db.ForeignKey("Artist.id")),
                 db.Column("venue_id", db.Integer, db.ForeignKey("Venue.id")),
                 db.Column("start_time", db.DateTime, default=datetime.utcnow()))


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

db.create_all(app=app)