#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
from flask_babel import Babel
from flask import (
  Flask,
  render_template,
  request,
  Response,
  flash,
  redirect,
  url_for,
  abort
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import (
  Formatter,
  FileHandler
)
from flask_wtf import Form
from forms import *
from flask_migrate import (
  Migrate,
  MigrateCommand
)
import sys
from models import (
  db,
  Venue,
  Artist,
  Shows,
)
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

moment = Moment(app)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  ----------------------------------------------------------------
#  CRUD for Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # Querying for cites and states of all venues distinctively
    areas = db.session.query(Venue.city, Venue.state).distinct(Venue.city, Venue.state)
    response = []
    for area in areas:

        # Querying venues and filter them based on area (city, venue)
        result = Venue.query.filter(Venue.state == area.state).filter(Venue.city == area.city).all()

        venue_data = []

        # Creating venues' response
        for venue in result:
            venue_data.append({
                'id': venue.id,
                'name': venue.name,
                'num_upcoming_shows': len(db.session.query(Shows).filter(Shows.start_time > datetime.now()).all())
            })

            response.append({
                'city': area.city,
                'state': area.state,
                'venues': venue_data
            })

    return render_template('pages/venues.html', areas=response)

# Venue Search functionality
@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    result = db.session.query(Venue).filter(Venue.name.ilike(f'%{search_term}%')).all()
    count = len(result)
    response = {
        "count": count,
        "data": result
    }

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

# Venue Display functionality
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.filter(Venue.id == venue_id).first()
  past = db.session.query(Shows).filter(Shows.venue_id == venue_id).filter(Shows.start_time < datetime.now()).join(Artist, Shows.artist_id == Artist.id).add_columns(Artist.id, Artist.name,Artist.image_link,Shows.start_time).all()
  upcoming = db.session.query(Shows).filter(Shows.venue_id == venue_id).filter(Shows.start_time > datetime.now()).join(Artist, Shows.artist_id == Artist.id).add_columns(Artist.id, Artist.name,Artist.image_link,Shows.start_time).all()

  upcoming_shows = []

  past_shows = []

  for i in upcoming:
      upcoming_shows.append({
          'artist_id': i[1],
          'artist_name': i[2],
          'image_link': i[3],
          'start_time': str(i[4])
      })

  for i in past:
      past_shows.append({
          'artist_id': i[1],
          'artist_name': i[2],
          'image_link': i[3],
          'start_time': str(i[4])
      })

  if venue is None:
      abort(404)

  response = {
      "id": venue.id,
      "name": venue.name,
      "genres": [venue.genres],
      "address": venue.address,
      "city": venue.city,
      "state": venue.state,
      "phone": venue.phone,
      "website": venue.website,
      "facebook_link": venue.facebook_link,
      "seeking_talent": venue.seeking_talent,
      "seeking_description": venue.seeking_description,
      "image_link": venue.image_link,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": len(past),
      "upcoming_shows_count": len(upcoming),
  }
  return render_template('pages/show_venue.html', venue=response)


#  ----------------------------------------------------------------
#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  try:
    venue = Venue()
    form.populate_obj(venue)
    db.session.add(venue)
    db.session.commit()
    flash('Venue created successfully')
  except Exception as e:
    print(e)
    flash('An error occured while creating venue')
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.close()
  return render_template('pages/home.html')

# Venue Edit functionality
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  some_venue = Venue.query.get(venue_id)
  return render_template('forms/edit_venue.html', form=form, venue=some_venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # try:
  form = VenueForm(request.form)
  some_venue = Venue.query.get(venue_id)
  try:
    form.populate_obj(some_venue)
    db.session.add(some_venue)
    db.session.commit()
    flash('Venue edited successfully')
  except Exception as e:
    print(e)
    flash('An error occured while creating venue')
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id = venue_id))

# Venue delete functionality
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    del_venue = Venue.query.get(venue_id)
    db.session.delete(del_venue)
    db.session.commit()
  except Exception as e:
    print(e)
    db.session.rollback()
    flash('There was a problem deleting this venue')
    print(sys.exc_info)
  finally:
    db.session.close()

#  ----------------------------------------------------------------
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  response = Artist.query.all() 
  return render_template('pages/artists.html', artists=response)

# Artist Search functionality
@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  result = db.session.query(Artist).filter(Artist.name.ilike(f'%{search_term}%')).all()
  count = len(result)
  response = {
      "count": count,
      "data": result
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

#Artist display functionality
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  some_artist = Artist.query.filter_by(id=artist_id).first()

  return render_template('pages/show_artist.html', artist=some_artist)

#  Artist Edit functionality
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  some_artist = Artist.query.filter_by(id=artist_id).first()

  return render_template('forms/edit_artist.html', form=form, artist=some_artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm(request.form)
  try:
    some_artist = Artist.query.filter_by(id=artist_id).first()
    form.populate_obj(some_artist)
    db.session.add(some_artist)
    db.session.commit()
    flash('Artist Edited Successfully')
  except Exception as e:
    print(e)
    flash('An error occured while Editing Artist')
    print(sys.exc_info())
    db.session.rollback()    
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  try:
    new_artist = Artist()
    form.populate_obj(new_artist)
    db.session.add(new_artist)
    db.session.commit()
    flash('Artist Created successfully')
  except Exception as e:
    print(e)
    flash('An error occured while creating Artist')
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.close()
    return render_template('pages/home.html')

#  ----------------------------------------------------------------
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  all_shows = Shows.query.join(Artist,Artist.id == Shows.artist_id).join(Venue,Venue.id == Shows.venue_id).all()
  return render_template('pages/shows.html', shows=all_shows)

@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  try:
    artist_id = request.form.get('artist_id')
    venue_id = request.form.get('venue_id')
    start_time = request.form.get('start_time')
    new_show = Shows(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    db.session.add(new_show)
    db.session.commit()

    flash('Show was successfully listed!')
  except Exception as e:
    print(e)
    db.session.rollback()
    flash('An error occured posting a new show')
    print(sys.exc_info())
  finally:
    db.session.close

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(400)
def bad_request(error):
  return render_template('errors/400.html'), 400

@app.errorhandler(401)
def unauthorized(error):
  return render_template('errors/401.html'), 401

@app.errorhandler(403)
def forbidden(error):
  return render_template('errors/403.html'), 403

@app.errorhandler(422)
def not_processable(error):
  return render_template('errors/404.html'), 422

@app.errorhandler(405)
def invalid_method(error):
  return render_template('errors/405.html'), 405

@app.errorhandler(409)
def duplicate_resource(error):
  return render_template('error/409.html'), 409


if not app.debug:
    file_handler = FileHandler(
   )
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
  app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''