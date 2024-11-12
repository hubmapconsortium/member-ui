# HuBMAP Member Registration and Profile

This repo contains code that manages the HuBMAP member registration and profile. It's built on top of Python Flask micro-framework and has a tight-coupling with Wordpress and the Connections plugin by sharing the same MySQL database.

## Local development

### Install dependencies

Create a new Python 3.9 or newer virtual environment:

````
python3 -m venv venv-member-ui
source venv-member-ui/bin/activate
````

Upgrade pip:

````
python3 -m pip install --upgrade pip
````

Before installing the dependencies, first comment out `uWSGI` package from `requirements.txt` since the uWSGI server is only used by deployment.

````
pip install -r requirements.txt
````

### Configuration

Creare a new confiuration file `app.cfg` under the `instance` folder. There's an example configuration file `instance/app.cfg.example` for your quick start.

### Start the Flask development server

Either method below will run the app at `http://localhost:5000`. Choose one:

````
python3 app.py
````

````
export FLASK_APP=app.py
export FLASK_ENV=development
python3 -m flask run
````
