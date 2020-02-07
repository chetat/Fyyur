#!/usr/bin/env python3
# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from models import Shows, Venue, Artist, db
from . import bp
import json
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from datetime import datetime
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from app.forms import *



#  Artists
#  ----------------------------------------------------------------
@bp.route("/artists", methods=['GET'])
def artists():
    # TODO: replace with real data returned from querying the database
    all_artist = []
    try:
        all_artist = Artist.query.all()
    except:
        db.session.rollback()
        db.session.close()
    data = []
    if all_artist:
        for artist in all_artist:
            data.append({"id": artist.id, "name": artist.name})
    return render_template("pages/artists.html", artists=all_artist)




#  Create Artist
#  ----------------------------------------------------------------
@bp.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@bp.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    artist_form = ArtistForm()

    name = artist_form.name.data
    phone = artist_form.phone.data
    city = artist_form.city.data
    image_url = artist_form.image_link.data
    facebook_url = artist_form.facebook_link.data
    state = artist_form.state.data
    genres = artist_form.genres.data
    website = artist_form.website_link.data
    seeking_venue = artist_form.seeking_venue.data
    seeking_description = artist_form.seeking_description.data
    artist = Artist(name=name, city=city, state=state, phone=phone,website_link=website, genres=genres, image_link=image_url,
                    facebook_link=facebook_url, seeking_venue=seeking_venue, seeking_description=seeking_description)
    # TODO: modify data to be the data object returned from db insertion(DONE)
    try:
        db.session.add(artist)
        db.session.commit()
        flash("Artist " + artist.name + " was successfully listed!")
    except:
        db.session.rollback()
        db.session.flush()
        flash("An error occurred. Artist " +
              artist.name + " could not be listed.")
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash("An error occurred. Artist " + data.name + " could not be listed.")
    # on successful db insert, flash success

    return render_template("pages/home.html")



@bp.route("/artists/search", methods=["POST"])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get("search_term", "")
    search_response = Artist.query.filter(Artist.name.ilike(f"%{search_term}%")).all()
    data = []
    for artist in search_response:
        data.append({
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": len(Artist.query.join(Shows).filter(Shows.c.start_time > datetime.now(), Shows.c.artist_id == artist_id).all())
        })

    response = {
        "count": len(search_response),
        "data":data
    }
    return render_template("pages/search_artists.html", results=response,
                           search_term=request.form.get("search_term", ""))

@bp.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real artist data from the artist table, using artist_id
    shows = db.session.query(Shows).filter(Shows.c.artist_id == artist_id).all()
    # upcoming_shows = Artist.query.join(Shows).filter(Shows.c.start_time > datetime.utcnow()).all()
    # past_shows = Artist.query.join(Shows).filter(Shows.c.start_time < datetime.utcnow(), Shows.c.artist_id == artist_id).all()

    upcoming_shows = Venue.query.join(Shows).filter(Shows.c.start_time > datetime.now(), Shows.c.artist_id == artist_id).all()
    past_shows = Venue.query.join(Shows).filter(Shows.c.start_time < datetime.now(), Shows.c.artist_id == artist_id).all()
    artist = Artist.query.filter_by(id=artist_id).first()

    upcoming_data = []
    for show in shows:
        for venue in upcoming_shows:
            upcoming_data.append({
                    "venue_id": venue.id,
                    "venue_name": venue.name,
                    "venue_image_link": venue.image_link,
                    "start_time":str(show.start_time)})
    data = {
            "id": artist.id,
            "name": artist.name,
            "genres": artist.genres,
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "facebook_link": artist.facebook_link,
            "website": artist.website_link,
            "image_link": artist.image_link,
            "seeking_venue": artist.seeking_venue,
            "seeking_description": artist.seeking_description,
            "upcoming_shows_count": len(upcoming_shows),
            "upcoming_shows":  upcoming_data,
            "past_shows": [{
                "venue_id": venue.id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": str(show.start_time)} for venue in past_shows],
            "past_shows_count": len(past_shows),

        }
    return render_template("pages/show_artist.html", artist=data)

#  Update
#  ----------------------------------------------------------------
@bp.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.filter(id == artist_id).first()
    artist = {
        "id": artist.id,
        "name": artist.name,
        "genres": ["Rock n Roll"],
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid"
                      "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80 "
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template("forms/edit_artist.html", form=form, artist=artist)


@bp.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

