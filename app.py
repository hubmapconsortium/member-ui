from flask import Flask, request, jsonify, Response, render_template, session, redirect, url_for
from globus_sdk import AuthClient, AccessTokenAuthorizer, ConfidentialAppAuthClient
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug import secure_filename
from phpserialize import dumps
import json
import os
import random
from shutil import copyfile
from datetime import datetime
import pathlib
import sys, traceback
import requests
from PIL import Image
from io import BytesIO
import ast
from shutil import copy2
import urllib.parse
import urllib.request
import requests
import string
import random
from flask_mail import Mail, Message
from pprint import pprint
from phpserialize import *


# Init app and use the config from instance folder
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('app.cfg')

# Flask-Mail instance
mail = Mail(app)

# Init DB
db = SQLAlchemy(app)

# Init MA
ma = Marshmallow(app)


connects = db.Table('user_connection',
        db.Column('user_id', db.Integer, db.ForeignKey('wp_users.id')),
        db.Column('connection_id', db.Integer, db.ForeignKey('wp_connections.id'))
)

# WPUser Class/Model
class StageUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    globus_user_id = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    component = db.Column(db.String(200))
    other_component = db.Column(db.String(200))
    organization = db.Column(db.String(200))
    other_organization = db.Column(db.String(200))
    role = db.Column(db.String(100))
    other_role = db.Column(db.String(200))
    working_group = db.Column(db.String(500)) # Checkboxes
    photo = db.Column(db.String(500))
    photo_url = db.Column(db.String(500))
    access_requests = db.Column(db.String(500)) # Checkboxes
    google_email = db.Column(db.String(200))
    github_username = db.Column(db.String(200))
    slack_username = db.Column(db.String(200))
    phone = db.Column(db.String(100))
    website = db.Column(db.String(500))
    biosketch = db.Column(db.String(200))
    expertise = db.Column(db.Text)
    orcid = db.Column(db.String(100))
    pm = db.Column(db.Boolean)
    pm_name = db.Column(db.String(100))
    pm_email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    deny = db.Column(db.Boolean)

    def __init__(self, a_dict):
        try:
            self.globus_user_id = a_dict['globus_user_id'] if 'globus_user_id' in a_dict else ''
            self.email = a_dict['email'] if 'email' in a_dict else ''
            self.first_name = a_dict['first_name'] if 'first_name' in a_dict else ''
            self.last_name = a_dict['last_name'] if 'last_name' in a_dict else ''
            self.component = a_dict['component'] if 'component' in a_dict else ''
            self.other_component = a_dict['other_component'] if 'other_component' in a_dict else ''
            self.organization = a_dict['organization'] if 'organization' in a_dict else ''
            self.other_organization = a_dict['other_organization'] if 'other_organization' in a_dict else ''
            self.role = a_dict['role'] if 'role' in a_dict else ''
            self.other_role = a_dict['other_role'] if 'other_role' in a_dict else ''
            self.working_group = str(a_dict['working_group']) if 'working_group' in a_dict else ''
            self.photo = a_dict['photo'] if 'photo' in a_dict else ''
            self.photo_url = a_dict['photo_url'] if 'photo_url' in a_dict else ''
            self.access_requests = str(a_dict['access_requests']) if 'access_requests' in a_dict else ''
            self.google_email = a_dict['google_email'] if 'google_email' in a_dict else ''
            self.github_username = a_dict['github_username'] if 'github_username' in a_dict else ''
            self.slack_username = a_dict['slack_username'] if 'slack_username' in a_dict else ''
            self.phone = a_dict['phone'] if 'phone' in a_dict else ''
            self.website = a_dict['website'] if 'website' in a_dict else ''
            self.biosketch = a_dict['biosketch'] if 'biosketch' in a_dict else ''
            self.expertise = a_dict['expertise'] if 'expertise' in a_dict else ''
            self.orcid = a_dict['orcid'] if 'orcid' in a_dict else ''
            self.pm = a_dict['pm'] if 'pm' in a_dict else ''
            self.pm_name = a_dict['pm_name'] if 'pm_name' in a_dict else ''
            self.pm_email = a_dict['pm_email'] if 'pm_email' in a_dict else ''
        except e:
            raise e

# StageUser Schema
class StageUserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'globus_user_id', 'email', 'first_name', 'last_name', 'component', 'other_component', 'organization', 'other_organization',
                    'role', 'other_role', 'working_group', 'photo', 'photo_url', 'access_requests', 'google_email', 'github_username', 'slack_username', 'phone', 'website',
                    'biosketch', 'orcid', 'pm', 'pm_name', 'pm_email', 'created_at', 'deny')

# WPUserMeta Class/Model
class WPUserMeta(db.Model):
    __tablename__ = 'wp_usermeta'

    umeta_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('wp_users.id'), nullable=False)
    meta_key = db.Column(db.String(255), nullable=False)
    meta_value = db.Column(db.Text)

# WPUserMeta Schema
class WPUserMetaSchema(ma.Schema):
    class Meta:
        model = WPUserMeta
        fields = ('umeta_id', 'user_id', 'meta_key', 'meta_value')

# ConnectionMeta
class ConnectionMeta(db.Model):
    __tablename__ = 'wp_connections_meta'

    meta_id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('wp_connections.id'), nullable=False)
    meta_key = db.Column(db.String(255), nullable=False)
    meta_value = db.Column(db.Text)

# ConnectionMeta Schema
class ConnectionMetaSchema(ma.Schema):
    class Meta:
        fields = ('meta_id', 'entry_id', 'meta_key', 'meta_value')

# Connection
class Connection(db.Model):
    __tablename__ = 'wp_connections'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    organization = db.Column(db.Text)
    options = db.Column(db.Text)
    phone_numbers = db.Column(db.Text)
    date_added = db.Column(db.Text)
    entry_type = db.Column(db.Text)
    visibility = db.Column(db.Text)
    slug = db.Column(db.Text)
    family_name = db.Column(db.Text)
    honorific_prefix = db.Column(db.Text)
    middle_name = db.Column(db.Text)
    honorific_suffix = db.Column(db.Text)
    title = db.Column(db.Text)
    department = db.Column(db.Text)
    contact_first_name = db.Column(db.Text)
    contact_last_name = db.Column(db.Text)
    addresses = db.Column(db.Text)
    im = db.Column(db.Text)
    social = db.Column(db.Text)
    links = db.Column(db.Text)
    dates = db.Column(db.Text)
    birthday = db.Column(db.Text)
    anniversary = db.Column(db.Text)
    bio = db.Column(db.Text)
    notes = db.Column(db.Text)
    excerpt = db.Column(db.Text)
    added_by = db.Column(db.Integer)
    edited_by = db.Column(db.Integer)
    owner = db.Column(db.Integer)
    user = db.Column(db.Integer)
    status = db.Column(db.String(20))
    metas = db.relationship('ConnectionMeta', backref='connection', lazy='joined')

# Connection Schema
class ConnectionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'first_name', 'last_name', 'organization', 'options', 'phone_numbers', 'metas')

    metas = ma.Nested(ConnectionMetaSchema, many=True)

# WPUser Class/Model
class WPUser(db.Model):
    __tablename__ = 'wp_users'

    id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(60), nullable=False)
    user_pass = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(500), nullable=False)
    metas = db.relationship('WPUserMeta', backref='user', lazy='joined')
    connection = db.relationship('Connection', secondary=connects, backref=db.backref('owners', lazy='dynamic'))

# WPUser Schema
class WPUserSchema(ma.Schema):
    class Meta:
        model = WPUser
        fields = ('id', 'user_login', 'user_email', 'metas', 'connection')
    
    metas = ma.Nested(WPUserMetaSchema, many=True)
    connection = ma.Nested(ConnectionSchema, many=True)

# Init schema
stage_user_schema = StageUserSchema(strict=True)
stage_users_schema = StageUserSchema(many=True, strict=True)

wp_user_schema = WPUserSchema(strict=True)
wp_users_schema = WPUserSchema(many=True, strict=True)

wp_user_meta_schema = WPUserMetaSchema(strict=True)
wp_user_metas_schema = WPUserMetaSchema(many=True, strict=True)

connection_schema = ConnectionSchema(strict=True)
connections_schema = ConnectionSchema(many=True, strict=True)


# Send email confirmation of new user registration to admins
def send_new_user_registration_mail(data):
    msg = Message('New user registration submitted', app.config['MAIL_ADMIN_LIST'])
    msg.html = render_template('email/new_user_registration_email.html', data = data)
    mail.send(msg)

# Send email to admins once user profile updated
def send_user_profile_update_mail(data):
    msg = Message('User profile updated', app.config['MAIL_ADMIN_LIST'])
    msg.html = render_template('email/user_profile_update_email.html', data = data)
    mail.send(msg)

# Once admin approves the new user registration, email the new user as well as the admins
def send_new_user_approval_mail(recipient, data):
    msg = Message('New user registration approved', [recipient] + app.config['MAIL_ADMIN_LIST'])
    msg.html = render_template('email/new_user_approval_email.html', data = data)
    mail.send(msg)

# Send user email once registration is denied
def send_new_user_approval_mail(recipient, data):
    msg = Message('New user registration denied', [recipient] + app.config['MAIL_ADMIN_LIST'])
    msg.html = render_template('email/new_user_denied_email.html', data = data)
    mail.send(msg)

# Routing

# Default
@app.route("/")
def hello():
    return "Welcome to HuBMAP User Registration!"


# Redirect users from react app login page to Globus auth login widget then redirect back
@app.route('/login')
def login():
    redirect_uri = url_for('login', _external=True)
    #redirect_uri = app.config['FLASK_APP_BASE_URI'] + 'login'

    confidential_app_auth_client = ConfidentialAppAuthClient(app.config['GLOBUS_APP_ID'], app.config['GLOBUS_APP_SECRET'])
    confidential_app_auth_client.oauth2_start_flow(redirect_uri)

    # If there's no "code" query string parameter, we're in this route
    # starting a Globus Auth login flow.
    # Redirect out to Globus Auth
    if 'code' not in request.args:                                        
        auth_uri = confidential_app_auth_client.oauth2_get_authorize_url(additional_params={"scope": "openid profile email urn:globus:auth:scope:transfer.api.globus.org:all urn:globus:auth:scope:auth.globus.org:view_identities urn:globus:auth:scope:nexus.api.globus.org:groups" })
        return redirect(auth_uri)
    # If we do have a "code" param, we're coming back from Globus Auth
    # and can start the process of exchanging an auth code for a token.
    else:
        auth_code = request.args.get('code')

        token_response = confidential_app_auth_client.oauth2_exchange_code_for_tokens(auth_code)
        
        # Get all Bearer tokens
        auth_token = token_response.by_resource_server['auth.globus.org']['access_token']
        nexus_token = token_response.by_resource_server['nexus.api.globus.org']['access_token']
        transfer_token = token_response.by_resource_server['transfer.api.globus.org']['access_token']

        # Also get the user info (sub, email, name, preferred_username) using the AuthClient with the auth token
        user_info = get_user_info(auth_token)

        print(user_info)

        # Store the resulting tokens in server session
        session['isAuthenticated'] = True
        session['globus_user_id'] = user_info['sub']
        session['name'] = user_info['name']
        session['email'] = user_info['email']
        session['auth_token'] = auth_token
        session['nexus_token'] = nexus_token
        session['transfer_token'] = transfer_token
      
        # Finally redirect back to the registeration page
        return redirect(url_for('register'))

@app.route('/logout')
def logout():
    """
    - Revoke the tokens with Globus Auth.
    - Destroy the session state.
    - Redirect the user to the Globus Auth logout page.
    """
    confidential_app_auth_client = ConfidentialAppAuthClient(app.config['GLOBUS_APP_ID'], app.config['GLOBUS_APP_SECRET'])

    # Revoke the tokens with Globus Auth
    if 'tokens' in session:    
        for token in (token_info['access_token']
            for token_info in session['tokens'].values()):
                confidential_app_auth_client.oauth2_revoke_token(token)

    # Destroy the session state
    session.clear()

    # build the logout URI with query params
    # there is no tool to help build this (yet!)
    globus_logout_url = (
        'https://auth.globus.org/v2/web/logout' +
        '?client={}'.format(app.config['GLOBUS_APP_ID']) +
        '&redirect_uri={}'.format(app.config['FLASK_APP_BASE_URI'] + 'register') +
        '&redirect_name={}'.format(app.config['FLASK_APP_NAME']))

    # Redirect the user to the Globus Auth logout page
    return redirect(globus_logout_url)


def get_user_info(token):
    auth_client = AuthClient(authorizer=AccessTokenAuthorizer(token))
    return auth_client.oauth2_userinfo()

# Create user info based on submitted form data
def construct_user(request):
    photo_file = None
    imgByteArr = None
    if 'photo' in request.files and request.files['photo']:
        photo_file = request.files['photo']
    
    url = request.form['photo_url']
    if photo_file is None and url:
        response = requests(url)
        img = Image.open(BytesIO(response.content))
        imgByteArr = BytesIO()
        img.save(imgByteArr, format=img.format)
        imgByteArr = imgByteArr.getvalue()

    new_user = {
        # Get the globus user id from session data
        "globus_user_id": session['globus_user_id'],
        # All others are from the form data
        "email": request.form['email'],
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "phone": request.form['phone'],
        "component": request.form['component'],
        "other_component": request.form['other_component'],
        "organization": request.form['organization'],
        "other_organization": request.form['other_organization'],
        "role": request.form['role'],
        "other_role": request.form['other_role'],
        # multiple checkboxes
        "working_group": request.form.getlist('working_group'),
        "photo": '',
        "photo_url": request.form['photo_url'],
        # multiple checkboxes
        "access_requests": ['Collaboration Portal'] + request.form.getlist('access_requests'),
        "google_email": request.form['google_email'],
        "github_username": request.form['github_username'],
        "slack_username": request.form['slack_username'],
        "website": request.form['website'],
        "expertise": request.form['expertise'],
        "orcid": request.form['orcid'],
        "pm": get_pm_selection(request.form),
        "pm_name": request.form['pm_name'],
        "pm_email": request.form['pm_email']
    }

    img_to_upload = photo_file if photo_file is not None else imgByteArr if imgByteArr is not None else None

    return new_user, img_to_upload

def get_pm_selection(form):
    value = form.get('pm', '')
    if value == 'yes':
        return True
    elif value == 'no':
        return False
    else:
        return None

def generate_csrf_token(stringLength = 10):
    if 'csrf_token' not in session:
        letters = string.ascii_lowercase
        session['csrf_token'] = ''.join(random.choice(letters) for i in range(stringLength))
    return session['csrf_token']

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # reCAPTCHA validation
        # Use request.args.get() instead of request.form[''] since esponse' is not the form
        recaptcha_response = request.args.get('g-recaptcha-response')
        values = {
            'secret': app.config['GOOGLE_RECAPTCHA_SECRET_KEY'],
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(app.config['GOOGLE_RECAPTCHA_VERIFY_URL'], data = data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())

        # For testing only
        result['success'] = True

        # Currently no backend form validation
        # Only front end validation and reCAPTCHA - Zhou
        if result['success']:
            # CSRF check
            session_csrf_token = session.pop('csrf_token', None)

            if not session_csrf_token or session_csrf_token != request.form['csrf_token']:
                context={
                    'isAuthenticated': True,
                    'username': session['name'],
                    'status': 'danger',
                    'message': 'Invalid CSRF token!'
                }
                return render_template('error.html', data = context)
            else:
                new_user, img_to_upload = construct_user(request)
                pprint(new_user)
                send_new_user_registration_mail(new_user)

                # # Send user info to web services API
                # rspns = requests.post(app.config['FLASK_APP_BASE_URI'] + "stage_user", files = {'json': (None, json.dumps(new_user), 'application/json'), 'img': img_to_upload})
                
                # if rspns.ok:
                #     try:
                #         # Send email to admin for new user approval
                #         send_new_user_registration_mail(new_user)
                #     except Exception as e: 
                #         print(e)
                #         print("send email failed")
                #         pass
                context = {
                    'isAuthenticated': True,
                    'username': session['name'],
                    'status': "success",
                    'message': "Your registration has been completed and has been sent for approval. Please contact <a href='mailto:admin@hubmapconsortium.org'>admin@hubmapconsortium.org</a> if you have any questions.",
                }

                return render_template('confirmation.html', data = context)
        # Show reCAPTCHA error
        else:
            context={
                'isAuthenticated': True,
                'username': session['name'],
                'status': 'danger',
                'message': 'reCAPTCHA error'
            }
            return render_template('error.html', data = context)
    # Handle GET
    else:
        if 'isAuthenticated' in session:
            context = {
                'isAuthenticated': True,
                'username': session['name'],
                'csrf_token': generate_csrf_token(),
                'first_name': session['name'].split(" ")[0],
                'last_name': session['name'].split(" ")[1],
                'email': session['email'],
                'recaptcha_site_key': app.config['GOOGLE_RECAPTCHA_SITE_KEY']
            }

            return render_template('register.html', data = context)
        else:
            context = {
                'isAuthenticated': False
            }

            return render_template('register.html', data = context)


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        # CSRF check
        session_csrf_token = session.pop('csrf_token', None)

        if not session_csrf_token or session_csrf_token != request.form['csrf_token']:
            context={
                'isAuthenticated': True,
                'username': session['name'],
                'status': 'danger',
                'message': 'Invalid CSRF token!'
            }
            return render_template('error.html', data = context)
        else:
            new_user, img_to_upload = construct_user(request)
            wp_user_id = request.POST['wp_user_id']

            # Send user info to web services API for updating
            # rspns = requests.put(app.config['FLASK_APP_BASE_URI'] + "wp_user/" + wp_user_id, files={'json': (None, json.dumps(new_user), 'application/json'), 'img': img_to_upload})
            
            # if rspns.ok:
            #     try:
            #         # Send email to admin for user profile update
            #         send_user_profile_update_mail(new_user)
            #     except Exception as e: 
            #         print(e)
            #         print("send email failed")
            #         pass
            context = {
                'isAuthenticated': True,
                'username': session['name'],
                'status': "success",
                'message': "Your profile information has been updated successfully.",
            }

            return render_template('confirmation.html', data = context)
              
    else:
        if 'isAuthenticated' in session:
            # Fetch user profile data from API service
            #rspns = requests.get(app.config['FLASK_APP_BASE_URI'] + "wp_user", params = {'globus_user_id': session['globus_user_id']})
            
            # if rspns.ok:
            #     # Render the user data in profile
            #     context = {
            #         'isAuthenticated': True,
            #         'username': session['name'],
            #         'csrf_token': generate_csrf_token()
            #     }

            #     return render_template('profile.html', data = context)
            # else:
            #     context = {
            #         'isAuthenticated': True,
            #         'username': session['name'],
            #         'status': 'warning',
            #         'message': 'An unexpected error occurred while trying to load your profile.  Please contact <a href="mailto:admin@hubmapconsortium.org">admin@hubmapconsortium.org</a> for help resolving the problem.'
            #     }
            #     return render_template('error.html', data = context)

            # for testing only
            with open('wp_user.json', 'r') as f:
                wp_user = json.load(f)

            # Parsing the json to get initial user profile data
            initial_data = {
                'first_name': wp_user['connection'][0]['first_name'],
                'last_name': wp_user['connection'][0]['last_name'],
                'email': wp_user['connection'][0]['email'],
                'phone': loads(wp_user['connection'][0]['phone_numbers'].encode())[0][b'number'].decode(),
                'component': next((meta for meta in wp_user['connection'][0]['metas'] if meta['meta_key'] == 'component'), {'meta_value': ''})['meta_value'],
                'other_component': next((meta for meta in wp_user['connection'][0]['metas'] if meta['meta_key'] == 'other_component'), {'meta_value': ''})['meta_value'],
                'organization': next((meta for meta in wp_user['connection'][0]['metas'] if meta['meta_key'] == 'organization'), {'meta_value': ''})['meta_value'],
                'other_organization': next((meta for meta in wp_user['connection'][0]['metas'] if meta['meta_key'] == 'other_organization'), {'meta_value': ''})['meta_value'],
                'role': next((meta for meta in wp_user['connection'][0]['metas'] if meta['meta_key'] == 'role'), {'meta_value': ''})['meta_value'],
                'other_role': next((meta for meta in wp_user['connection'][0]['metas'] if meta['meta_key'] == 'other_role'), {'meta_value': ''})['meta_value'],
                'working_group': next((meta for meta in wp_user['connection'][0]['metas'] if meta['meta_key'] == 'working_group'), {'meta_value': ''})['meta_value'],
                'access_requests': next((meta for meta in wp_user['connection'][0]['metas'] if meta['meta_key'] == 'access_requests'), {'meta_value': ''})['meta_value'],
                'google_email': next((meta for meta in wp_user['connection'][0]['metas'] if meta['meta_key'] == 'google_email'), {'meta_value': ''})['meta_value'],
                'github_username': next((meta for meta in wp_user['connection'][0]['metas'] if meta['meta_key'] == 'github_username'), {'meta_value': ''})['meta_value'],
                'slack_username': next((meta for meta in wp_user['connection'][0]['metas'] if meta['meta_key'] == 'slack_username'), {'meta_value': ''})['meta_value'],
                'website': next((meta for meta in wp_user['connection'][0]['metas'] if meta['meta_key'] == 'website'), {'meta_value': ''})['meta_value'],
                'expertise': next((meta for meta in wp_user['connection'][0]['metas'] if meta['meta_key'] == 'expertise'), {'meta_value': ''})['meta_value'],
                'orcid': next((meta for meta in wp_user['connection'][0]['metas'] if meta['meta_key'] == 'orcid'), {'meta_value': ''})['meta_value'],
                'pm': 'Yes' if next((meta for meta in wp_user['connection'][0]['metas'] if meta['meta_key'] == 'pm'), {'meta_value': ''})['meta_value'] == '1' else 'No',
                'pm_name': next((meta for meta in wp_user['connection'][0]['metas'] if meta['meta_key'] == 'pm_name'), {'meta_value': ''})['meta_value'],
                'pm_email': next((meta for meta in wp_user['connection'][0]['metas'] if meta['meta_key'] == 'pm_email'), {'meta_value': ''})['meta_value'],
            }

            pprint(initial_data)
            # if not initial_data['working_group'].strip() == '':
            #     initial_data['working_group'] = ast.literal_eval(initial_data['working_group'])
            # if not initial_data['access_requests'].strip() == '':
            #     initial_data['access_requests'] = ast.literal_eval(initial_data['access_requests'])

            context = {
                'isAuthenticated': True,
                'username': session['name'],
                'csrf_token': generate_csrf_token(),
                'wp_user_id': wp_user['id']
            }

            d = {**context, **initial_data}
            pprint(d)
            return render_template('profile.html', data = {**context, **initial_data})
        else:
            context = {
                'isAuthenticated': False
            }

            return render_template('profile.html', data = context)


@app.route("/match_user", methods=['GET', 'POST'])
def match_user():
    return render_template("match_user.html")

# APIs
@app.route('/stage_user', methods=['GET'])
def get_stage_users():
    try:
        args = request.args
        globus_user_id = args['globus_user_id'] if 'globus_user_id' in args else None
        if globus_user_id:
            stage_users = StageUser.query.filter(StageUser.globus_user_id == globus_user_id)
            if stage_users.count() == 0:
                return Response('No stage user found', status=400)
        else:
            stage_users = StageUser.query.all()
        m_result = stage_users_schema.dump(stage_users)
        return jsonify(m_result)
    except Exception as e:
        print(e)
        print("Exception in user code:")
        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)
        return Response('Stage user update failed', status=500)

@app.route('/stage_user', methods=['POST'])
def add_stage_user():
    if 'json' not in request.form:
        return Response('No user data', status=400)

    j_stage_user = json.loads(request.form['json'])
    
    if 'img' not in request.files:
        BASE = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f"{j_stage_user['globus_user_id']}.jpg"))
        copy2(os.path.join(BASE, 'avatar/', 'noname.jpg'), save_path)
        j_stage_user['photo'] = save_path
    else:
        if j_stage_user['photo_url'] != '':
            response = requests.get(j_stage_user['photo_url'])
            img_file = Image.open(BytesIO(response.content))
            extension = img_file.format
        else:
            _, extension = request.files['img'].filename.rsplit('.', 1)
            img_file = request.files['img']
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f"{j_stage_user['globus_user_id']}.{extension}"))
        img_file.save(save_path)
        j_stage_user['photo'] = save_path
    try:
        new_stage_user = StageUser(j_stage_user)
    except:
        return Response('User data is not valid', status=400)
    
    if StageUser.query.filter(StageUser.globus_user_id == new_stage_user.globus_user_id).first():
        return Response('Stage user created', status=201)
    else:
        try:
            db.session.add(new_stage_user)
            db.session.commit()
        except:
            return Response('Error happend when add a new stage user', status=500)
    return Response('Stage user created', status=201)

@app.route('/stage_user/<stage_user_id>', methods=['PUT'])
def update_stage_user(stage_user_id):
    """ put  stage_user into wp_user and wp_connection
    """
    wp_user_id = request.args.get('wp_user_id')
    connection_id = request.args.get('connection_id')
    stage_user = StageUser.query.get(stage_user_id)
    wp_user = WPUser.query.get(wp_user_id) if wp_user_id else None
    connection = Connection.query.get(connection_id) if connection_id else None
    deny = request.args.get('deny')

    if stage_user and wp_user:
        '''match a existing wp_user
        '''
        # update wp_user
        wp_user.user_login = stage_user.email
        wp_user.user_pass = generate_password()
        for meta in wp_user.metas:
            if meta.meta_key == "wp_capabilities":
                meta.meta_value = "a:1:{s:6:\"member\";b:1;}"

        # connection = wp_user.connection[0] if wp_user.connection else None
        assign_wp_user(wp_user, stage_user, connection)
        # delete stage user
        db.session.delete(stage_user)
        db.session.commit()

        m_result = wp_user_schema.dump(wp_user)
        return jsonify(m_result)
    elif deny == 'True':
        stage_user.deny = True
        db.session.commit()

        m_result = stage_user_schema.dump(stage_user)
        return jsonify(m_result)
    else:
        '''create a new wp_user
        '''
        try:
            usermeta = WPUserMeta.query.filter(WPUserMeta.meta_key.like('openid-connect-generic-subject-identity'), WPUserMeta.meta_value == stage_user.globus_user_id).first()
            if not usermeta or usermeta.user:
                wp_user = WPUser()
            else:
                wp_user = usermeta.user
            assign_wp_user(wp_user, stage_user, connection)
            if wp_user.id:
                db.session.add(new_wp_user)
            db.session.delete(stage_user)
            db.session.commit()
        except Exception as e:
            print(e)
            print("Exception in user code:")
            print("-"*60)
            traceback.print_exc(file=sys.stdout)
            print("-"*60)
            return Response('Stage user update failed', status=500)

        m_result = wp_user_schema.dump(new_wp_user)
        return jsonify(m_result)

@app.route('/wp_user', methods=['POST'])
def add_wp_user():
    if 'json' not in request.form:
        return Response('No user data', status=400)

    j_wp_user = json.loads(request.form['json'])
    
    if 'img' not in request.files:
        img_file = open('./avatar/noname.jpg', 'r')
    else:
        img_file = request.files['img']
        img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(img_file.filename)))
    
    try:
        new_wp_user = WPUser(j_wp_user)
    except:
        return Response('User data is not valid', status=400)
    db.session.add(new_wp_user)
    db.session.commit()
    return Response('Stage user created', status=201)

@app.route('/wp_user', methods=['GET'])
def get_wp_users():
    args = request.args
    globus_user_id = args['globus_user_id'] if 'globus_user_id' in args else None
    email = args['email'] if 'email' in args else None
    member = args['member'] if 'member' in args else None
    if globus_user_id:
        usermeta = WPUserMeta.query.filter(WPUserMeta.meta_key.like('openid-connect-generic-subject-identity'), WPUserMeta.meta_value == globus_user_id).first()
        if not usermeta:
            return Response('No wp user found', 400)
        if member is None:
            all_wp_users = [usermeta.user]
        elif member == 'True':
            capability = next(m.meta_value for m in usermeta.user.metas if m.meta_key == 'wp_capabilities')
            if 'member' in capability:
                all_wp_users = [usermeta.user]
            else:
                all_wp_users = []
    elif email:
        all_wp_users = WPUser.query.filter(WPUser.user_email == email)
    else:
        all_wp_users = WPUser.query.all()
    m_result = wp_users_schema.dump(all_wp_users)
    return jsonify(m_result)

@app.route('/wp_user/<id>', methods=['PUT'])
def update_wp_user(id):
    """
    Match a wp user to a existing user if id present
    Create a new user if id not present
    """
    wp_user = WPUser.query.get(id)
    j_user = json.loads(request.form['json'])
    if 'img' not in request.files:
        pass
    else:
        if not j_user['photo_url'] == '':
            response = requests.get(j_user['photo_url'])
            img_file = Image.open(BytesIO(response.content))
            extension = img_file.format
        else:
            _, extension = request.files['img'].filename.rsplit('.', 1)
            img_file = request.files['img']
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f"{j_user['globus_user_id']}.{extension}"))
        img_file.save(save_path)
        j_user['photo'] = save_path
    
    try:
        stage_user = StageUser(j_user)
        assign_wp_user(wp_user, stage_user, wp_user.connection[0], 'EDIT')
        db.session.commit()
    except Exception as e:
        print(e)
        print("Exception in user code:")
        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)
        return Response('WP user update failed', status=500)

    return Response('WP user update completed', status=200)

@app.route('/wp_user_meta', methods=['GET'])
def get_wp_user_metas():
    args = request.args
    globus_user_id = args['globus_user_id'] if 'globus_user_id' in args else None
    if globus_user_id:
        user_metas = WPUserMeta.query.filter(WPUserMeta.meta_key.like('openid-connect-generic-subject-identity'), WPUserMeta.meta_value == globus_user_id)
    else:
        user_metas = WPUserMeta.query.all()
    m_result = wp_user_metas_schema.dump(user_metas)
    return jsonify(m_result)

@app.route('/connection/<id>', methods=['GET'])
def get_connection(id):
    connection = Connection.query.get(id)
    return connection_schema.jsonify(connection)

@app.route('/connection', methods=['GET'])
def get_connections():
    args = request.args
    email = args['email'] if 'email' in args else ''
    first_name = args['first_name'] if 'first_name' in args else ''
    last_name = args['last_name'] if 'last_name' in args else ''
    if email == '' and first_name == '' and last_name == '':
        print("no args")
        return Response('No connections', 400)
    else:
        print(f"email: {email}, first_name: {first_name}, last_name: {last_name}")
        connections = Connection.query.filter(Connection.email.like(f'%{email}%')).all()

    if len(connections) <= 0:
        return Response('No connections', 400)

    result = connections_schema.dump(connections)
    return jsonify(result.data)

def generate_password():
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    passlen = 16
    return "".join(random.sample(s, passlen))

def assign_wp_user(wp_user, user_obj, connection=None, mode='CREATE'):
    admin_id = WPUser.query.filter(WPUser.user_login == app.config.get('ADMIN_USERNAME')).first().id

    wp_user.user_login = user_obj.email
    wp_user.user_email = user_obj.email
    wp_user.user_pass = generate_password()
    if not wp_user.id:
        meta_capabilities = WPUserMeta()
        meta_capabilities.meta_key = "wp_capabilities"
        meta_capabilities.meta_value = "a:1:{s:6:\"member\";b:1;}"
        wp_user.metas.append(meta_capabilities)
        meta_globus_user_id = WPUserMeta()
        meta_globus_user_id.meta_key = "openid-connect-generic-subject-identity"
        meta_globus_user_id.meta_value = user_obj.globus_user_id
        wp_user.metas.append(meta_globus_user_id)

    if not connection:
        connection = Connection()
    
    if connection.owners.count() == 0: 
        connection.owners.append(wp_user)
    
    connection.email = f"a:1:{{i:0;a:7:{{s:2:\"id\";i:2199;s:4:\"type\";s:4:\"work\";s:4:\"name\";s:10:\"Work Email\";s:10:\"visibility\";s:6:\"public\";s:5:\"order\";i:0;s:9:\"preferred\";b:0;s:7:\"address\";s:{len(user_obj.email)}:\"{user_obj.email}\";}}}}"
    connection.first_name = user_obj.first_name
    connection.last_name = user_obj.last_name
    connection.organization = user_obj.organization

    if not user_obj.photo == '':
        photo_file_name = user_obj.photo.split('/')[-1]
        pathlib.Path(app.config.get('CONNECTION_IMAGE_PATH') + user_obj.first_name.lower() + '-' + user_obj.last_name.lower() ).mkdir(parents=True, exist_ok=True)
        copyfile(user_obj.photo, app.config.get('CONNECTION_IMAGE_PATH') + user_obj.first_name.lower() + '-' + user_obj.last_name.lower() + "/" + photo_file_name)
        connection.options = "{\"entry\":{\"type\":\"individual\"},\"image\":{\"linked\":true,\"display\":true,\"name\":{\"original\":\"" + photo_file_name + "\"},\"meta\":{\"original\":{\"name\":\"" + photo_file_name + "\",\"path\":\"" + app.config.get('CONNECTION_IMAGE_PATH') + user_obj.first_name.lower() + '-' + user_obj.last_name.lower() + "\\/" + photo_file_name + "\",\"url\": \"" + app.config.get('CONNECTION_IMAGE_URL') + user_obj.first_name.lower() + '-' + user_obj.last_name.lower() + "\\/" + photo_file_name + "\",\"width\":200,\"height\":200,\"size\":\"width=\\\"200\\\" height=\\\"200\\\"\",\"mime\":\"image\\/jpeg\",\"type\":2}}}}"
    connection.phone_numbers = f"a:1:{{i:0;a:7:{{s:2:\"id\";i:417;s:4:\"type\";s:9:\"workphone\";s:4:\"name\";s:10:\"Work Phone\";s:10:\"visibility\";s:6:\"public\";s:5:\"order\";i:0;s:9:\"preferred\";b:0;s:6:\"number\";s:{len(user_obj.phone)}:\"{user_obj.phone}\";}}}}"
    
    access_requests = next((meta.meta_value for meta in connection.metas if meta.meta_key == 'access_requests'), '[]') if mode.upper() == 'EDIT' else '[]'
    working_group = next((meta.meta_value for meta in connection.metas if meta.meta_key == 'working_group'), '[]') if mode.upper() == 'EDIT' else '[]'
    if mode.upper() == 'EDIT' and user_obj.google_email == '':
        google_email = next((meta.meta_value for meta in connection.metas if meta.meta_key == 'google_email'), '')
    else:
        google_email = user_obj.google_email
        
    if mode.upper() == 'EDIT' and user_obj.github_username == '':
        github_username = next((meta.meta_value for meta in connection.metas if meta.meta_key == 'github_username'), '')
    else:
        github_username = user_obj.github_username

    if mode.upper() == 'EDIT' and user_obj.slack_username == '':
        slack_username = next((meta.meta_value for meta in connection.metas if meta.meta_key == 'slack_username'), '')
    else:
        slack_username = user_obj.slack_username

    [db.session.delete(meta) for meta in connection.metas]
    connection_meta_component = ConnectionMeta()
    connection_meta_component.meta_key = 'component'
    connection_meta_component.meta_value = user_obj.component
    connection.metas.append(connection_meta_component)
    connection_meta_other_component = ConnectionMeta()
    connection_meta_other_component.meta_key = 'other_component'
    connection_meta_other_component.meta_value = user_obj.other_component
    connection.metas.append(connection_meta_other_component)
    connection_meta_organization = ConnectionMeta()
    connection_meta_organization.meta_key = 'organization'
    connection_meta_organization.meta_value = user_obj.organization
    connection.metas.append(connection_meta_organization)
    connection_meta_other_organization = ConnectionMeta()
    connection_meta_other_organization.meta_key = 'other_organization'
    connection_meta_other_organization.meta_value = user_obj.other_organization
    connection.metas.append(connection_meta_other_organization)
    connection_meta_role = ConnectionMeta()
    connection_meta_role.meta_key = 'role'
    connection_meta_role.meta_value = user_obj.role
    connection.metas.append(connection_meta_role)
    connection_meta_other_role = ConnectionMeta()
    connection_meta_other_role.meta_key = 'other_role'
    connection_meta_other_role.meta_value = user_obj.other_role
    connection.metas.append(connection_meta_other_role)
    connection_meta_working_group = ConnectionMeta()
    connection_meta_working_group.meta_key = 'working_group'
    connection_meta_working_group.meta_value = str(ast.literal_eval(working_group) + ast.literal_eval(user_obj.working_group)).replace('\'', '"')
    connection.metas.append(connection_meta_working_group)
    connection_meta_access_requests = ConnectionMeta()
    connection_meta_access_requests.meta_key = 'access_requests'
    connection_meta_access_requests.meta_value = str(ast.literal_eval(access_requests) + ast.literal_eval(user_obj.access_requests)).replace('\'', '"')
    connection.metas.append(connection_meta_access_requests)
    connection_meta_google_email = ConnectionMeta()
    connection_meta_google_email.meta_key = 'google_email'
    connection_meta_google_email.meta_value = google_email
    connection.metas.append(connection_meta_google_email)
    connection_meta_github_username = ConnectionMeta()
    connection_meta_github_username.meta_key = 'github_username'
    connection_meta_github_username.meta_value = github_username
    connection.metas.append(connection_meta_github_username)
    connection_meta_slack_username = ConnectionMeta()
    connection_meta_slack_username.meta_key = 'slack_username'
    connection_meta_slack_username.meta_value = slack_username
    connection.metas.append(connection_meta_slack_username)
    connection_meta_website = ConnectionMeta()
    connection_meta_website.meta_key = 'website'
    connection_meta_website.meta_value = user_obj.website
    connection.metas.append(connection_meta_website)
    connection_meta_biosketch = ConnectionMeta()
    connection_meta_biosketch.meta_key = 'biosketch'
    connection_meta_biosketch.meta_value = user_obj.biosketch
    connection.metas.append(connection_meta_biosketch)
    connection_meta_expertise = ConnectionMeta()
    connection_meta_expertise.meta_key = 'expertise'
    connection_meta_expertise.meta_value = user_obj.expertise
    connection.metas.append(connection_meta_expertise)
    connection_meta_orcid = ConnectionMeta()
    connection_meta_orcid.meta_key = 'orcid'
    connection_meta_orcid.meta_value = user_obj.orcid
    connection.metas.append(connection_meta_orcid)
    connection_meta_pm = ConnectionMeta()
    connection_meta_pm.meta_key = 'pm'
    connection_meta_pm.meta_value = user_obj.pm
    connection.metas.append(connection_meta_pm)
    connection_meta_pm_name = ConnectionMeta()
    connection_meta_pm_name.meta_key = 'pm_name'
    connection_meta_pm_name.meta_value = user_obj.pm_name
    connection.metas.append(connection_meta_pm_name)
    connection_meta_pm_email = ConnectionMeta()
    connection_meta_pm_email.meta_key = 'pm_email'
    connection_meta_pm_email.meta_value = user_obj.pm_email
    connection.metas.append(connection_meta_pm_email)
    connection_meta_email = ConnectionMeta()
    connection_meta_email.meta_key = 'email'
    connection_meta_email.meta_value = user_obj.email
    connection.metas.append(connection_meta_email)
    connection_meta_phone = ConnectionMeta()
    connection_meta_phone.meta_key = 'phone'
    connection_meta_phone.meta_value = user_obj.phone
    connection.metas.append(connection_meta_phone)
    
    
    ## default value ##
    connection.date_added = str(datetime.today().timestamp())
    connection.entry_type = 'individual'
    connection.visibility = 'public'
    connection.slug = user_obj.first_name.lower() + '-' + user_obj.last_name.lower()
    connection.family_name = ''
    connection.honorific_prefix = ''
    connection.middle_name = ''
    connection.honorific_suffix = ''
    connection.title = user_obj.role
    connection.department = user_obj.component
    connection.contact_first_name = ''
    connection.contact_last_name = ''
    connection.addresses = 'a:0:{}'
    connection.im = 'a:0:{}'
    connection.social = 'a:0:{}'
    connection.links = 'a:0:{}'
    connection.dates = 'a:0:{}'
    connection.birthday = ''
    connection.anniversary = ''
    connection.bio = user_obj.expertise
    connection.notes = ''
    connection.excerpt = ''
    connection.added_by = admin_id
    connection.edited_by = admin_id
    connection.owner = admin_id
    connection.user = 0
    connection.status = 'approved'

    return connection

# Run Server
if __name__ == "__main__":
    app.run(debug=True)