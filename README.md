# HuBMAP Member Registration and Profile Portal

This repo contains code that handles the HuBMAP member registration and profile management. It's built on top of Python Flask micro-framework and has a tight-coupling with Wordpress and the Connections plugin.


## Install dependencies

Create a new Python 3.x virtual environment:

````
python3 -m venv venv-member-ui
source venv-member-ui/bin/activate
````

Upgrade pip:
````
python3 -m pip install --upgrade pip
````

Then install the dependencies:

````
pip install -r requirements.txt
````

## Configuration

The confiuration file `app.cfg` is located under `instance` folder. You can read more about [Flask Instance Folders](http://flask.pocoo.org/docs/1.0/config/#instance-folders). 

There's an example configuration file `instance/app.cfg.example` for your quick start.

## Start the server

Either methods below will run the search-api web service at `http://localhost:5005`. Choose one:

### Directly via Python

````
python3 app.py
````

### With the Flask Development Server

````
cd src
export FLASK_APP=app.py
export FLASK_ENV=development
python3 -m flask run -p 5005
````

## Deployment

For deployment on remote VM, we'll use Nignx to serve this Python program via uWSGI server. 

First copy the `nginx/conf.d/member-ui.conf` to `/etc/nginx/conf.d`, then start the program:

```
uwsgi --ini /opt/hubmap/member-ui/uwsgi.ini
```