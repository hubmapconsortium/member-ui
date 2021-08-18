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

For deployment on remote VM, we'll use Nignx as a reverse proxy to forward the requests to uWSGI server. 

First copy the `nginx/conf.d/member-ui.conf` to `/etc/nginx/conf.d` and edit the configurations with domain and SSL certificate based on the deployment. For example:

```
server {
    listen 80;
    server_name profile.dev.hubmapconsortium.org;
    
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name profile.dev.hubmapconsortium.org;   
    root /usr/share/nginx/html;

    access_log /var/log/nginx/nginx_access_member-ui.log;
    error_log /var/log/nginx/nginx_error_member-ui.log warn;

    ssl_certificate /etc/letsencrypt/live/profile.dev.hubmapconsortium.org/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/profile.dev.hubmapconsortium.org/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

    # HTTP requests get passed to the uwsgi server using the "uwsgi" protocol on port 5000
    location / { 
        include uwsgi_params;
        uwsgi_pass uwsgi://127.0.0.1:5000;
    }
    
}
```

Copy the `hubmap-member-ui.uwsgi.service` file to `/etc/systemd/system` and we'll create a service. 

To enable the service with system reboot:

```
systemctl enable hubmap-member-ui.uwsgi.service
```

### Start and Stop service

```
systemctl start hubmap-member-ui.uwsgi.service
```

```
systemctl stop hubmap-member-ui.uwsgi.service
```

We can also restart the running service to reflect Python code changes:

```
systemctl restart hubmap-member-ui.uwsgi.service
```
