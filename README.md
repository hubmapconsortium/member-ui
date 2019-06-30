# The HuBMAP User Registration Portal

This repo contains code that handles the HuBMAP user registration and profile management. It's built on top of Python Flask micro-framework.

## Installation

We use [Pipenv](https://docs.pipenv.org/en/latest/) to manage dependencies for this application. Pipenv is recommended for collaborative projects as it's a higher-level tool that simplifies dependency management for common use cases.

Just follow the Pipenv instructions to install Pipenv. You can also install via `pip install --user pipenv`. After that, clone this repo and create a virtualenv for this project:

````
git clone https://github.com/hubmapconsortium/registration.git
cd registration
pipenv shell
````

Then install all the project dependencies:

````
pipenv install
````

## Configuration

The confiuration file `app.cfg` is located under `instance` folder. You can read more about [Flask Instance Folders](http://flask.pocoo.org/docs/1.0/config/#instance-folders). In this config file, you can specify the following items:

````
# App name and deployment URI
FLASK_APP_NAME = 'HuBMAP User Profile'
# Works regardless the trailing slash /
FLASK_APP_BASE_URI = 'http://localhost:5000'

# Flask app session key
SECRET_KEY = ''

# Globus app client ID and secret
GLOBUS_APP_ID = ''
GLOBUS_APP_SECRET = ''

# Google reCAPTCHA v2 ("I'm not a robot" Checkbox) keys
GOOGLE_RECAPTCHA_SITE_KEY = ''
GOOGLE_RECAPTCHA_SECRET_KEY = ''
GOOGLE_RECAPTCHA_VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'

# DB connection and settings
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/wp_dev'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# IMAGE DIRECTORIES, works regardless the trailing slash /
STAGE_USER_IMAGE_DIR = '/path/registration/avatar/'
CONNECTION_IMAGE_DIR = '/path/images/'
CONNECTION_IMAGE_URL = 'https://hubmapconsortium.org/wp-content/uploads/connections-images/'

# Email settings for Flask-Mail extension
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your gmail address'
MAIL_PASSWORD = 'your gmail password'
MAIL_DEFAULT_SENDER = ('HuBMAP User Profile', 'your gmail address')
MAIL_DEBUG = False

# Admin emails, not part of Flask-Mail configuration
MAIL_ADMIN_LIST = []
````

There's an example configuration file named `app.cfg.example` for your quick start.

## Start Flask development server

```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

## Deactivate current Pipenv shell

Simply run `exit`.


### Production Deployment

Flask's built-in server is not suitable for production as it doesn't scale well. Here are the [Deployment Options](http://flask.pocoo.org/docs/1.0/deploying/). In our case, we installed `mod_wsgi` to run the flask app on Apache httpd. On your production server.