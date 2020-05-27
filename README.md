# HuBMAP Member Registration and Profile Portal

This repo contains code that handles the HuBMAP member registration and profile management. It's built on top of Python Flask micro-framework and has a tight-coupling with Wordpress and the Connections plugin.


## Local standalone development

### Install dependencies

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

### Configuration

The confiuration file `app.cfg` is located under `instance` folder. You can read more about [Flask Instance Folders](http://flask.pocoo.org/docs/1.0/config/#instance-folders). 

There's an example configuration file `instance/app.cfg.example` for your quick start.

### Start Flask development server

```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Simply run `exit` to deactivate current Pipenv shell


### Local development with Docker-Compose

This option comes with MySQL server and phpMyAdmin running on separate docker containers, the member-ui is also running its own container that talks to the MySQL container. This makes setting up the local development environments very easy without needing to setup MySQL server separately.

In the project root, 

````
sudo docker-compose -f docker-compose.dev.yml build
````

This builds the docker images for member-ui and MySQL.

To spin up the containers, 

````
sudo docker-compose -f docker-compose.dev.yml up
````

To stop and remove the containers as well as the volume mounts and network:

````
sudo docker-compose -f docker-compose.dev.yml down
````
