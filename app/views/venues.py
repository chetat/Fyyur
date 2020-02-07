



#!/usr/bin/env python3
# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from models import Shows, Venue, Artist, db
from . import bp
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from datetime import datetime
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from app.forms import *


@bp.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
@bp.route("/venues")
def venues():
    # DONE: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = []
    try:
        venues = Venue.query.distinct(Venue.city, Venue.state).all()
        if venues:
            for venue in venues:
                upcoming_shows = len(Venue.query.join(Shows).filter(Shows.c.start_time > datetime.utcnow(), Shows.c.venue_id == venue.id).all())
                data.append({
                        "city": venue.city,
                        "state": venue.state,
                        "venues": [{"id": v.id, "name": v.name,
                            "num_upcoming_shows": upcoming_shows }
                                for v in Venue.query.filter_by(city=venue.city,
                                                           state=venue.state).all()]
                        })
    except Exception as e:
        print(e)
        pass
    return render_template("pages/venues.html", areas=data)



@bp.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on Venues //artists// with partial string search. Ensure it is case-insensitive.
    # search for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get("search_term", "")
    search_response = Venue.query.filter(Venue.name.ilike(f"%{search_term}%")).all()
    data = []
    for venue in search_response:
        data.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(Venue.query.join(Shows).filter(Shows.c.start_time > datetime.utcnow(), Shows.c.venue_id == venue.id).all())
        })
        print(data)

    response = {
        "count": len(search_response),
        "data":data
    }
    return render_template("pages/search_venues.html", results=response,
                           search_term=request.form.get("search_term", ""))

@bp.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    venue = Venue.query.filter_by(id=venue_id).first()

    # shows = db.session.query(Shows).filter(Shows.c.venue_id == venue.id).all()
    upcoming_shows = Artist.query.join(Shows).filter(Shows.c.start_time > datetime.utcnow(), Shows.c.venue_id == venue_id).all()
    past_shows = Artist.query.join(Shows).filter(Shows.c.start_time < datetime.utcnow(), Shows.c.venue_id == venue_id).all()
    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "upcoming_shows":[{
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            } for artist in upcoming_shows],
        "upcoming_shows_count": len(upcoming_shows),
        "past_shows": [{
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time":str(show.start_time)} for artist in past_shows],
        "past_shows_count": len(past_shows),

        }
    return render_template("pages/show_venue.html", venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@bp.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)


@bp.route('/venues/create', methods=['POST'])
def create_venue_submission():
    venue_form = VenueForm()
    # venue_form.validate()
    name = venue_form.name.data
    phone = venue_form.phone.data
    address = venue_form.address.data
    city = venue_form.city.data
    image_url = venue_form.image_link.data
    facebook_url = venue_form.facebook_link.data
    state = venue_form.state.data
    genres = venue_form.genres.data
    seeking_talent = venue_form.seeking_talent.data
    seeking_description = venue_form.seeking_description.data
    website = venue_form.website_link.data

    # DONE: insert form data as a new Venue record in the db, instead
    venue = Venue(name=name, city=city, state=state, address=address, phone=phone, image_link=image_url,
                            facebook_link=facebook_url, genres=genres,
                    website_link=website,seeking_talent=seeking_talent,
                        seeking_description=seeking_description)
    try:
        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash("Venue " + name + " was successfully listed!")
        # Done: modify data to be the data object returned from db insertion
    except Exception as e:
        # Done: on unsuccessful db insert, flash an error instead.
        # e.g., flash("An error occurred. Venue " + data.name + " could not be listed.")
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        db.session.rollback()
        flash("An error occurred. Venue " +
              name + " could not be listed.")
        db.session.flush()
        print(e)
    
    return render_template("pages/home.html")


@bp.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # DONE: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        venue = Venue.query.filter_by(id=venue_id).first()
        db.session.delete(venue)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.close()

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return redirect(url_for("bp.index"))


@bp.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))


@bp.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = {
      "id": 1,
      "name": "The Musical Hop",
      "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
      "address": "1015 Folsom Street",
      "city": "San Francisco",
      "state": "CA",
      "phone": "123-123-1234",
      "website": "https://www.themusicalhop.com",
      "facebook_link": "https://www.facebook.com/TheMusicalHop",
      "seeking_talent": True,
      "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
      "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)