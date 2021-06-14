Fyyur
Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.
Dependencies

Dependencies are listed in the requirements.txt file. Run pip3 install -r requirements.txt to install them.
Features

    Creating new venues, artists, and creating new shows.
    Searching for venues and artists.
    Learning more about a specific artist or venue.

Tech Stack

    SQLAlchemy ORM
    PostgreSQL
    Python3 and Flask
    Flask-Migrate
    HTML, CSS, and Javascript with Bootstrap 3 for the website's frontend

Main Files: Project Structure

├── README.md
├── app.py *** the main driver of the app. Includes SQLAlchemy models.
                  "python app.py" to run after installing dependences
├── config.py *** Database URLs, CSRF generation, etc
├── error.log
├── forms.py *** forms used to create new artists, shows, and venues.
├── requirements.txt *** The dependencies which can be installed like this "pip3 install -r requirements.txt"
├── static
│   ├── css 
│   ├── font
│   ├── ico
│   ├── img
│   └── js
└── templates
    ├── errors
    ├── forms
    ├── layouts
    └── pages

Overall:

    Models are located in the MODELS section of app.py.
    Controllers are also located in app.py.
    The web frontend is located in templates/, which builds static assets deployed to the web server at static/.
    Web forms for creating data are located in form.py

Highlight folders:

    templates/pages -- Defines the pages that are rendered to the site. These templates render views based on data passed into the template’s view, in the controllers defined in app.py. These pages successfully represent the data to the user.
    templates/layouts -- Defines the layout that a page can be contained in to define footer and header code for a given page.
    templates/forms -- Defines the forms used to create new artists, shows, and venues.
    app.py -- Defines routes that match the user’s URL, and controllers which handle data and renders views to the user. This is the main file which connects to and manipulates the database and render views with data to the user, based on the URL.
    Models in app.py -- Defines the data models that set up the database tables.
    config.py -- Stores configuration variables and instructions, separate from the main application code. This is where the app connects to the database.

Endpoints
Venues
GET /venues

    Fetches all the venues from the database
    Request arguments: None
    Returns: A list of venues filtered by cities and states

GET /venues/<int:venue_id>

    Fetches a venue matching the venue id
    Request arguments: Venue id
    Returns: a fully detailed venue or 404 Not Found if there's no venue matching that id

POST /venues/search

    Fetches venues matching the search term
    Request arguments: Search term
    Returns: A list of venues matches the search term

POST /venues/create

    Creates a venue using the form values
    Request arguments: Venue Form data
    Returns: back to home

DELETE /venues/<int:venue_id>

    Deletes a venue matching the venue id
    Request arguments: Venue id
    Returns: back to home

Artists
GET /artists

    Fetches all the artists from the database
    Request arguments: None
    Returns: A list of artists


GET /artists/<int:artist_id>

    Fetches an artist matching the artist id
    Request arguments: None
    Returns: an artist matching the artist id or 404 Not Found if there's no artist matching that id

POST /artists/search

    Fetches artists matching the search term
    Request arguments: Search term
    Returns: A list of artists matches the search term
POST /artists/create

    Creates an artist using the form values
    Request arguments: Artist Form data
    Returns: back to home

Shows
GET /shows

    Fetches all shows from the database
    Request arguments: None
    Returns: a list of shows

POST /shows/create

    Creates a show using the form data
    Request arguments: Show Form data
    Returns: back to home

Error Codes

    bad_request - 400
    unauthorized - 401
    forbidden - 403
    not_found - 404
    server_error - 500
    not_processable - 422
    invalid_method - 405
    duplicate_resource - 409

Development Setup

First, install Flask

$ cd ~
$ sudo pip3 install Flask

To start and run the local development server,

    Create virtualenv directory and initialize a virtualenv:

$ cd YOUR_PROJECT_DIRECTORY_PATH/
$ mkdir pythnmkdir python-virtual-environments && cd python-virtual-environments
$ sudo python3 -m venv env
$ source env/bin/activate

    Install the dependencies:

$ pip3 install -r requirements.txt

    Run the development server:

$ export FLASK_APP=app
$ export FLASK_ENV=development # enables debug mode
$ python3 app.py


