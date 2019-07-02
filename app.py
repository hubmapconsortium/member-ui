from flask import Flask, request, jsonify, Response, render_template, session, redirect, url_for
from globus_sdk import AuthClient, AccessTokenAuthorizer, ConfidentialAppAuthClient
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug import secure_filename
import phpserialize
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
from functools import wraps

# For debugging
from pprint import pprint


# Init app and use the config from instance folder
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('app.cfg')

# Remove trailing slash / from URL base to avoid "//" caused by config with trailing slash
app.config['FLASK_APP_BASE_URI'] = app.config['FLASK_APP_BASE_URI'].strip('/')
app.config['CONNECTION_IMAGE_URL'] = app.config['CONNECTION_IMAGE_URL'].strip('/')

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
            self.working_group = json.dumps(a_dict['working_group']) if 'working_group' in a_dict else ''
            self.photo = a_dict['photo'] if 'photo' in a_dict else ''
            self.photo_url = a_dict['photo_url'] if 'photo_url' in a_dict else ''
            self.access_requests = json.dumps(a_dict['access_requests']) if 'access_requests' in a_dict else ''
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

# Define output format with marshmallow schema
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
def send_new_user_registered_mail(data):
    msg = Message('New user registration submitted', app.config['MAIL_ADMIN_LIST'])
    msg.html = render_template('email/new_user_registered_email.html', data = data)
    mail.send(msg)

# Send email to admins once user profile updated
def send_user_profile_updated_mail(data):
    msg = Message('User profile updated', app.config['MAIL_ADMIN_LIST'])
    msg.html = render_template('email/user_profile_updated_email.html', data = data)
    mail.send(msg)

# Once admin approves the new user registration, email the new user as well as the admins
def send_new_user_approved_mail(recipient, data):
    msg = Message('New user registration approved', [recipient] + app.config['MAIL_ADMIN_LIST'])
    msg.html = render_template('email/new_user_approved_email.html', data = data)
    mail.send(msg)

# Send user email once registration is denied
def send_new_user_denied_mail(recipient, data):
    msg = Message('New user registration denied', [recipient] + app.config['MAIL_ADMIN_LIST'])
    msg.html = render_template('email/new_user_denied_email.html', data = data)
    mail.send(msg)



# Get user info from globus with the auth access token
def get_globus_user_info(token):
    auth_client = AuthClient(authorizer=AccessTokenAuthorizer(token))
    return auth_client.oauth2_userinfo()

# Create user info based on submitted form data
def construct_user(request):
    photo_file = None
    imgByteArr = None

    # Users can only choose to upload image ,pull image from URL, or just the default image
    # Values: "upload", "url", "default"
    profile_pic_option = request.form['profile_pic_option'].lower()

    if profile_pic_option == 'upload':
        if 'photo' in request.files and request.files['photo']:
            photo_file = request.files['photo']
    elif profile_pic_option == 'url':
        photo_url = request.form['photo_url']
        if photo_url:
            response = requests.get(photo_url)
            img = Image.open(BytesIO(response.content))
            imgByteArr = BytesIO()
            img.save(imgByteArr, format=img.format)
            imgByteArr = imgByteArr.getvalue()
    elif profile_pic_option == 'existing':
        # This only happends for updating profile
        pass
    else:
        # use default image
        photo_file = None

    user_info = {
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
        "access_requests": request.form.getlist('access_requests'),
        "google_email": request.form['google_email'],
        "github_username": request.form['github_username'],
        "slack_username": request.form['slack_username'],
        "website": request.form['website'],
        "expertise": request.form['expertise'],
        "orcid": request.form['orcid'],
        "pm": get_pm_selection(request.form['pm']),
        "pm_name": request.form['pm_name'],
        "pm_email": request.form['pm_email']
    }

    img_to_upload = photo_file if photo_file is not None else imgByteArr if imgByteArr is not None else None

    return user_info, profile_pic_option, img_to_upload


def get_pm_selection(value):
    # Make comparison case insensitive
    value = value.lower()
    if value == 'yes':
        return True
    elif value == 'no':
        return False
    else:
        return None

# Generate CSRF tokens for registration form and profile form
def generate_csrf_token(stringLength = 10):
    if 'csrf_token' not in session:
        letters = string.ascii_lowercase
        session['csrf_token'] = ''.join(random.choice(letters) for i in range(stringLength))
    return session['csrf_token']


def show_registration_form():
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

# Three different types of message for authenticated users
def show_user_error(message):
    context = {
        'isAuthenticated': True,
        'username': session['name'],
        'message': message
    }
    return render_template('user_message/user_error.html', data = context)

def show_user_confirmation(message):
    context = {
        'isAuthenticated': True,
        'username': session['name'],
        'message': message
    }
    return render_template('user_message/user_confirmation.html', data = context)

def show_user_info(message):
    context = {
        'isAuthenticated': True,
        'username': session['name'],
        'message': message
    }
    return render_template('user_message/user_info.html', data = context)

# Admin messages
def show_admin_error(message):
    context = {
        'isAuthenticated': True,
        'username': session['name'],
        'message': message
    }
    return render_template('admin_message/admin_error.html', data = context)

def show_admin_confirmation(message):
    context = {
        'isAuthenticated': True,
        'username': session['name'],
        'message': message
    }
    return render_template('admin_message/admin_confirmation.html', data = context)

def show_admin_info(message):
    context = {
        'isAuthenticated': True,
        'username': session['name'],
        'message': message
    }
    return render_template('admin_message/admin_info.html', data = context)

# Check if the user is registered and approved
# meaning this user is in `wp_users`, `wp_connections`, and `user_connection` tables and 
# the user has the role of "member" or "administrator", the role is assigned when the user is approved
# A use with a submitted registration but pending is not consodered to be an approved user
def user_is_approved(globus_user_id):
    user_meta = WPUserMeta.query.filter(WPUserMeta.meta_key.like('openid-connect-generic-subject-identity'), WPUserMeta.meta_value == globus_user_id).first()
    if not user_meta:
        print('No user found with globus_user_id: ' + globus_user_id)
        return False
    users = [user_meta.user]
    result = wp_users_schema.dump(users)
    user = result[0][0]
    capabilities = next((meta for meta in user['metas'] if meta['meta_key'] == 'wp_capabilities'), {})
    if (('meta_value' in capabilities) and ('member' in capabilities['meta_value'])):
        return True
    else:
        return False

# Check if user has the "administrator" role
def user_is_admin(globus_user_id):
    user_meta = WPUserMeta.query.filter(WPUserMeta.meta_key.like('openid-connect-generic-subject-identity'), WPUserMeta.meta_value == globus_user_id).first()
    if not user_meta:
        print('No user found with globus_user_id: ' + globus_user_id)
        return False
    users = [user_meta.user]
    result = wp_users_schema.dump(users)
    user = result[0][0]
    capabilities = next((meta for meta in user['metas'] if meta['meta_key'] == 'wp_capabilities'), {})
    if (('meta_value' in capabilities) and ('administrator' in capabilities['meta_value'])):
        return True
    else:
        return False


# Check if the user registration is still pending for approval in `stage_user` table
def user_in_pending(globus_user_id):
    stage_user = StageUser.query.filter(StageUser.globus_user_id == globus_user_id)
    if stage_user.count() == 0:
    	return False
    return True

# Add new user reigstration to `stage_user` table
def add_new_stage_user(user_info, profile_pic_option, img_to_upload):
    # First handle the profile image and save it to target directory
    user_info['photo'] = handle_stage_user_profile_pic(user_info, profile_pic_option, img_to_upload)

    try:
        stage_user = StageUser(user_info)
    except Exception as e:
        print('User data is invalid')
        print(e)
    
    if StageUser.query.filter(StageUser.globus_user_id == stage_user.globus_user_id).first():
        print('The same stage user exists')
    else:
        try:
            db.session.add(stage_user)
            db.session.commit()
        except Exception as e:
            print('Failed to add a new stage user')
            print(e)
            

# Query the user data to populate into profile form
# This is different from get_wp_user() in that it also returns the meta and connection data
# from where we can parse all the profile data
def get_user_profile(globus_user_id):
    user_meta = WPUserMeta.query.filter(WPUserMeta.meta_key.like('openid-connect-generic-subject-identity'), WPUserMeta.meta_value == globus_user_id).first()
    if not user_meta:
        print('No WP user found with globus_user_id: ' + globus_user_id)
        return None
    users = [user_meta.user]
    result = wp_users_schema.dump(users)
    user = result[0][0]
    return user

# Only save image to the stage dir, once approved, will copy to target dir
def handle_stage_user_profile_pic(user_info, profile_pic_option, img_to_upload):
    save_path = None
    
    if profile_pic_option == 'upload':
        _, extension = img_to_upload.filename.rsplit('.', 1)
        img_file = img_to_upload

        save_path = os.path.join(app.config['STAGE_USER_IMAGE_DIR'], secure_filename(f"{user_info['globus_user_id']}.{extension}"))
        img_file.save(save_path)
    elif profile_pic_option == 'url':
        response = requests.get(user_info['photo_url'])
        img_file = Image.open(BytesIO(response.content))
        extension = img_file.format

        save_path = os.path.join(app.config['STAGE_USER_IMAGE_DIR'], secure_filename(f"{user_info['globus_user_id']}.{extension}"))
        img_file.save(save_path)
    else:
        # Use default image
        save_path = os.path.join(app.config['STAGE_USER_IMAGE_DIR'], secure_filename(f"{user_info['globus_user_id']}.jpg"))
        copy2(os.path.join(app.root_path, 'static', 'images', 'default_profile.jpg'), save_path)

    return save_path

# Save the profile image to target dir directly per user, no need to use stage image dir 
def update_user_profile_pic(user_info, profile_pic_option, img_to_upload, profile_images_folder_name):
    save_path = None
    
    if profile_pic_option == 'upload':
        _, extension = img_to_upload.filename.rsplit('.', 1)
        img_file = img_to_upload

        save_path = os.path.join(app.config['CONNECTION_IMAGE_DIR'], profile_images_folder_name, secure_filename(f"{user_info['globus_user_id']}.{extension}"))
        img_file.save(save_path)
    elif profile_pic_option == 'url':
        response = requests.get(user_info['photo_url'])
        img_file = Image.open(BytesIO(response.content))
        extension = img_file.format

        save_path = os.path.join(app.config['CONNECTION_IMAGE_DIR'], profile_images_folder_name, secure_filename(f"{user_info['globus_user_id']}.{extension}"))
        img_file.save(save_path)
    else:
        # Use default image
        save_path = os.path.join(app.config['CONNECTION_IMAGE_DIR'], profile_images_folder_name, secure_filename(f"{user_info['globus_user_id']}.jpg"))
        copy2(os.path.join(app.root_path, 'static', 'images', 'default_profile.jpg'), save_path)

    return save_path

# Update user profile with user-provided information 
def update_user_profile(user_info, profile_pic_option, img_to_upload):
    # First get the exisiting wp_user record with globus id
    # this has no connection data
    wp_user = get_wp_user(session['globus_user_id'])

    # Get the connection and meta data record by globus id
    result = get_user_profile(session['globus_user_id'])

    connection_id = result['connection'][0]['id']

    # Get connection profile by connection id
    connection_profile = get_connection_profile(connection_id)

    # User connection images folder name, AKA slug
    profile_images_folder_name = connection_profile.slug

    # Handle the profile image and save it to target directory
    # Do nothing if user wants to keep the exisiting image
    if profile_pic_option != "existing":
        user_info['photo'] = update_user_profile_pic(user_info, profile_pic_option, img_to_upload, profile_images_folder_name)

    # will this stage_user be added to database?
    stage_user = StageUser(user_info)
    edit_connection(stage_user, wp_user, connection_profile)
    db.session.commit()



# This is user approval without using existing mathicng profile
# Approving by moving user data from `stage_user` into `wp_user` and `wp_connections`
# also add the ids to the `user_connection` table
def approve_stage_user_by_creating_new(stage_user):
    # First need to check if there's an exisiting wp_user record with the same globus id
    wp_user = get_wp_user(stage_user.globus_user_id)

    if not wp_user:
        # Create new user and meta
        new_wp_user = create_new_user(stage_user)

        # Create profile in `wp_connections`
        create_new_connection(stage_user, new_wp_user)

        db.session.add(new_wp_user)
        db.session.delete(stage_user)
        db.session.commit()
    else:
        edit_wp_user(stage_user)
        create_new_connection(stage_user, wp_user)
        db.session.delete(stage_user)
        db.session.commit()
        

def approve_stage_user_by_editing_matched(stage_user, connection_profile):
    # First need to check if there's an exisiting wp_user record with the same globus id
    wp_user = get_wp_user(stage_user.globus_user_id)

    if not wp_user:
        # Create new user and meta
        new_wp_user = create_new_user(stage_user)

        # Edit profile in `wp_connections`
        edit_connection(stage_user, new_wp_user, connection_profile, True)

        db.session.add(new_wp_user)
        db.session.delete(stage_user)
        db.session.commit()
    else:
        edit_wp_user(stage_user)
        edit_connection(stage_user, wp_user, connection_profile, True)
        db.session.delete(stage_user)
        db.session.commit()


# Edit the exisiting wp_user role as "member"
def edit_wp_user(stage_user):
    wp_user = get_wp_user(stage_user.globus_user_id)
    wp_user.user_login = stage_user.email
    wp_user.user_email = stage_user.email

    meta_capabilities = next((meta for meta in wp_user.metas if meta.meta_key == "wp_capabilities"), None)
    if meta_capabilities:
        meta_capabilities.meta_value = "a:1:{s:6:\"member\";b:1;}"
    
def create_new_user(stage_user):
    # Create a new wp_user record
    new_wp_user = WPUser()
    new_wp_user.user_login = stage_user.email
    new_wp_user.user_email = stage_user.email
    new_wp_user.user_pass = generate_password()

    # Create new usermeta for "member" role
    meta_capabilities = WPUserMeta()
    meta_capabilities.meta_key = "wp_capabilities"
    meta_capabilities.meta_value = "a:1:{s:6:\"member\";b:1;}"
    new_wp_user.metas.append(meta_capabilities)
    
    # Create new usermeta for globus id
    meta_globus_user_id = WPUserMeta()
    meta_globus_user_id.meta_key = "openid-connect-generic-subject-identity"
    meta_globus_user_id.meta_value = stage_user.globus_user_id
    new_wp_user.metas.append(meta_globus_user_id)

    return new_wp_user

def generate_password():
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    passlen = 16
    return "".join(random.sample(s, passlen))

def create_new_connection(stage_user, new_wp_user):
    # First get the id of admin user in `wp_usermeta` table
    admin_id = WPUserMeta.query.filter(WPUserMeta.meta_key.like('openid-connect-generic-subject-identity'), WPUserMeta.meta_value == session['globus_user_id']).first().user_id

    connection = Connection()
    connection.owners.append(new_wp_user)

    # Need to handle email and phone metas first
    connection_meta_email = ConnectionMeta()
    connection_meta_email.meta_key = 'email'
    connection_meta_email.meta_value = stage_user.email
    connection.metas.append(connection_meta_email)
    
    connection_meta_phone = ConnectionMeta()
    connection_meta_phone.meta_key = 'phone'
    connection_meta_phone.meta_value = stage_user.phone
    connection.metas.append(connection_meta_phone)

    # TO-DO: add new record to `wp_connections_email` and `wp_connections_phone` then get the id and update `wp_connections` email/phone fields
    # Currectly hard-coded id
    connection.email = f"a:1:{{i:0;a:7:{{s:2:\"id\";i:2199;s:4:\"type\";s:4:\"work\";s:4:\"name\";s:10:\"Work Email\";s:10:\"visibility\";s:6:\"public\";s:5:\"order\";i:0;s:9:\"preferred\";b:0;s:7:\"address\";s:{len(stage_user.email)}:\"{stage_user.email}\";}}}}"
    # Currectly hard-coded id
    connection.phone_numbers = f"a:1:{{i:0;a:7:{{s:2:\"id\";i:417;s:4:\"type\";s:9:\"workphone\";s:4:\"name\";s:10:\"Work Phone\";s:10:\"visibility\";s:6:\"public\";s:5:\"order\";i:0;s:9:\"preferred\";b:0;s:6:\"number\";s:{len(stage_user.phone)}:\"{stage_user.phone}\";}}}}"
    
    connection.first_name = stage_user.first_name
    connection.last_name = stage_user.last_name
    connection.organization = stage_user.organization
    connection.date_added = str(datetime.today().timestamp())
    connection.entry_type = 'individual'
    connection.visibility = 'public'
    connection.slug = stage_user.first_name.lower() + '-' + stage_user.last_name.lower()
    connection.family_name = ''
    connection.honorific_prefix = ''
    connection.middle_name = ''
    connection.honorific_suffix = ''
    connection.title = ''
    connection.department = ''
    connection.contact_first_name = ''
    connection.contact_last_name = ''
    connection.addresses = 'a:0:{}'
    connection.im = 'a:0:{}'
    connection.social = 'a:0:{}'
    connection.links = 'a:0:{}'
    connection.dates = 'a:0:{}'
    connection.birthday = ''
    connection.anniversary = ''
    connection.bio = stage_user.expertise
    connection.notes = ''
    connection.excerpt = ''
    connection.added_by = admin_id
    connection.edited_by = admin_id
    connection.owner = admin_id
    connection.user = 0
    connection.status = 'approved'

    # Handle profile image
    photo_file_name = stage_user.photo.split('/')[-1]
    pathlib.Path(os.path.join(app.config['CONNECTION_IMAGE_DIR'], connection.slug)).mkdir(parents=True, exist_ok=True)
    copyfile(stage_user.photo, os.path.join(app.config['CONNECTION_IMAGE_DIR'], connection.slug, photo_file_name))
    # Delete stage image file
    os.unlink(stage_user.photo)

    # Both "path" and "url" use the same url
    image_url = app.config['CONNECTION_IMAGE_URL'] + "/" + connection.slug + "/" + photo_file_name
    connection.options = "{\"entry\":{\"type\":\"individual\"},\"image\":{\"linked\":true,\"display\":true,\"name\":{\"original\":\"" + photo_file_name + "\"},\"meta\":{\"original\":{\"name\":\"" + photo_file_name + "\",\"path\":\"" + image_url + "\",\"url\": \"" + image_url + "\",\"width\":200,\"height\":200,\"size\":\"width=\\\"200\\\" height=\\\"200\\\"\",\"mime\":\"image/jpeg\",\"type\":2}}}}"

    google_email = stage_user.google_email
    github_username = stage_user.github_username
    slack_username = stage_user.slack_username

    # Other connections metas
    connection_meta_component = ConnectionMeta()
    connection_meta_component.meta_key = 'component'
    connection_meta_component.meta_value = stage_user.component
    connection.metas.append(connection_meta_component)

    connection_meta_other_component = ConnectionMeta()
    connection_meta_other_component.meta_key = 'other_component'
    connection_meta_other_component.meta_value = stage_user.other_component
    connection.metas.append(connection_meta_other_component)

    connection_meta_organization = ConnectionMeta()
    connection_meta_organization.meta_key = 'organization'
    connection_meta_organization.meta_value = stage_user.organization
    connection.metas.append(connection_meta_organization)

    connection_meta_other_organization = ConnectionMeta()
    connection_meta_other_organization.meta_key = 'other_organization'
    connection_meta_other_organization.meta_value = stage_user.other_organization
    connection.metas.append(connection_meta_other_organization)

    connection_meta_role = ConnectionMeta()
    connection_meta_role.meta_key = 'role'
    connection_meta_role.meta_value = stage_user.role
    connection.metas.append(connection_meta_role)

    connection_meta_other_role = ConnectionMeta()
    connection_meta_other_role.meta_key = 'other_role'
    connection_meta_other_role.meta_value = stage_user.other_role
    connection.metas.append(connection_meta_other_role)

    connection_meta_working_group = ConnectionMeta()
    connection_meta_working_group.meta_key = 'working_group'
    connection_meta_working_group.meta_value = stage_user.working_group
    connection.metas.append(connection_meta_working_group)

    connection_meta_access_requests = ConnectionMeta()
    connection_meta_access_requests.meta_key = 'access_requests'
    connection_meta_access_requests.meta_value = stage_user.access_requests
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
    connection_meta_website.meta_value = stage_user.website
    connection.metas.append(connection_meta_website)

    # need biosketch?
    connection_meta_biosketch = ConnectionMeta()
    connection_meta_biosketch.meta_key = 'biosketch'
    connection_meta_biosketch.meta_value = stage_user.biosketch
    connection.metas.append(connection_meta_biosketch)

    connection_meta_expertise = ConnectionMeta()
    connection_meta_expertise.meta_key = 'expertise'
    connection_meta_expertise.meta_value = stage_user.expertise
    connection.metas.append(connection_meta_expertise)

    connection_meta_orcid = ConnectionMeta()
    connection_meta_orcid.meta_key = 'orcid'
    connection_meta_orcid.meta_value = stage_user.orcid
    connection.metas.append(connection_meta_orcid)

    connection_meta_pm = ConnectionMeta()
    connection_meta_pm.meta_key = 'pm'
    connection_meta_pm.meta_value = stage_user.pm
    connection.metas.append(connection_meta_pm)

    connection_meta_pm_name = ConnectionMeta()
    connection_meta_pm_name.meta_key = 'pm_name'
    connection_meta_pm_name.meta_value = stage_user.pm_name
    connection.metas.append(connection_meta_pm_name)

    connection_meta_pm_email = ConnectionMeta()
    connection_meta_pm_email.meta_key = 'pm_email'
    connection_meta_pm_email.meta_value = stage_user.pm_email
    connection.metas.append(connection_meta_pm_email)


# Overwrite the existing fields with the ones from user registration or profile update
def edit_connection(stage_user, wp_user, connection, new_user = False):
    # First get the id of admin user in `wp_usermeta` table
    admin_id = WPUserMeta.query.filter(WPUserMeta.meta_key.like('openid-connect-generic-subject-identity'), WPUserMeta.meta_value == session['globus_user_id']).first().user_id

    wp_user.user_login = stage_user.email
    wp_user.user_email = stage_user.email
    
    # TO-DO: add new record to `wp_connections_email` and `wp_connections_phone` then get the id and update `wp_connections` email/phone fields
    # Currectly hard-coded id
    connection.email = f"a:1:{{i:0;a:7:{{s:2:\"id\";i:2199;s:4:\"type\";s:4:\"work\";s:4:\"name\";s:10:\"Work Email\";s:10:\"visibility\";s:6:\"public\";s:5:\"order\";i:0;s:9:\"preferred\";b:0;s:7:\"address\";s:{len(stage_user.email)}:\"{stage_user.email}\";}}}}"
    # Currectly hard-coded id
    connection.phone_numbers = f"a:1:{{i:0;a:7:{{s:2:\"id\";i:417;s:4:\"type\";s:9:\"workphone\";s:4:\"name\";s:10:\"Work Phone\";s:10:\"visibility\";s:6:\"public\";s:5:\"order\";i:0;s:9:\"preferred\";b:0;s:6:\"number\";s:{len(stage_user.phone)}:\"{stage_user.phone}\";}}}}"
    
    connection.first_name = stage_user.first_name
    connection.last_name = stage_user.last_name
    connection.organization = stage_user.organization
    connection.slug = stage_user.first_name.lower() + '-' + stage_user.last_name.lower()
    connection.bio = stage_user.expertise
    connection.edited_by = admin_id
 
    # Handle profile image
    # stage_user.photo is the save path
    photo_file_name = stage_user.photo.split('/')[-1]

    # Profile update for an approved user doesn't need to mkdir and copy image
    # Approving a new user by editing an exisiting profile requires to mkdir and copy the image
    target_image_dir = os.path.join(app.config['CONNECTION_IMAGE_DIR'], connection.slug)
    if new_user:
        pathlib.Path(target_image_dir).mkdir(parents=True, exist_ok=True)
        copyfile(stage_user.photo, os.path.join(app.config['CONNECTION_IMAGE_DIR'], connection.slug , photo_file_name))
        # Delete stage image file
        os.remove(stage_user.photo)
    else:
        # For existing profile image update, remove all the old images and leave the new one there
        # since the one image has already been copied there
        for file in os.listdir(target_image_dir):
            file_path = os.path.join(target_image_dir, file)
            
            if os.path.isfile(file_path) and (file_path != stage_user.photo):
                try:
                    os.unlink(file_path)
                except Exception as e:
                    print("Failed to empty the profile image folder: " + target_image_dir)
                    print(e)

    # Both "path" and "url" use the same url
    image_url = app.config['CONNECTION_IMAGE_URL'] + "/" + connection.slug + "/" + photo_file_name
    connection.options = "{\"entry\":{\"type\":\"individual\"},\"image\":{\"linked\":true,\"display\":true,\"name\":{\"original\":\"" + photo_file_name + "\"},\"meta\":{\"original\":{\"name\":\"" + photo_file_name + "\",\"path\":\"" + image_url + "\",\"url\": \"" + image_url + "\",\"width\":200,\"height\":200,\"size\":\"width=\\\"200\\\" height=\\\"200\\\"\",\"mime\":\"image/jpeg\",\"type\":2}}}}"


    # Update corresponding metas
    connection_meta_component = ConnectionMeta.query.filter(ConnectionMeta.meta_key == 'component', ConnectionMeta.entry_id == connection.id).first()
    if connection_meta_component:
        connection_meta_component.meta_value = stage_user.component
    else:
        connection_meta_component = ConnectionMeta()
        connection_meta_component.meta_key = 'component'
        connection_meta_component.meta_value = stage_user.component
        connection.metas.append(connection_meta_component)

    connection_meta_other_component = ConnectionMeta.query.filter(ConnectionMeta.meta_key == 'other_component', ConnectionMeta.entry_id == connection.id).first()
    if connection_meta_other_component:
        connection_meta_other_component.meta_value = stage_user.other_component
    else:
        connection_meta_other_component = ConnectionMeta()
        connection_meta_other_component.meta_key = 'other_component'
        connection_meta_other_component.meta_value = stage_user.other_component
        connection.metas.append(connection_meta_other_component)

    connection_meta_organization = ConnectionMeta.query.filter(ConnectionMeta.meta_key == 'organization', ConnectionMeta.entry_id == connection.id).first()
    if connection_meta_organization:
        connection_meta_organization.meta_value = stage_user.organization
    else:
        connection_meta_organization = ConnectionMeta()
        connection_meta_organization.meta_key = 'organization'
        connection_meta_organization.meta_value = stage_user.organization
        connection.metas.append(connection_meta_organization)

    connection_meta_other_organization = ConnectionMeta.query.filter(ConnectionMeta.meta_key == 'other_organization', ConnectionMeta.entry_id == connection.id).first()
    if connection_meta_other_organization:
        connection_meta_other_organization.meta_value = stage_user.other_organization
    else:
        connection_meta_other_organization = ConnectionMeta()
        connection_meta_other_organization.meta_key = 'other_organization'
        connection_meta_other_organization.meta_value = stage_user.other_organization
        connection.metas.append(connection_meta_other_organization)

    connection_meta_role = ConnectionMeta.query.filter(ConnectionMeta.meta_key == 'role', ConnectionMeta.entry_id == connection.id).first()
    if connection_meta_role:
        connection_meta_role.meta_value = stage_user.role
    else:
        connection_meta_role = ConnectionMeta()
        connection_meta_role.meta_key = 'role'
        connection_meta_role.meta_value = stage_user.role
        connection.metas.append(connection_meta_role)

    connection_meta_other_role = ConnectionMeta.query.filter(ConnectionMeta.meta_key == 'other_role', ConnectionMeta.entry_id == connection.id).first()
    if connection_meta_other_role:
        connection_meta_other_role.meta_value = stage_user.other_role
    else:
        connection_meta_other_role = ConnectionMeta()
        connection_meta_other_role.meta_key = 'other_role'
        connection_meta_other_role.meta_value = stage_user.other_role
        connection.metas.append(connection_meta_other_role)

    connection_meta_working_group = ConnectionMeta.query.filter(ConnectionMeta.meta_key == 'working_group', ConnectionMeta.entry_id == connection.id).first()
    if connection_meta_working_group:
        connection_meta_working_group.meta_value = stage_user.working_group
    else:
        connection_meta_working_group = ConnectionMeta()
        connection_meta_working_group.meta_key = 'working_group'
        connection_meta_working_group.meta_value = stage_user.working_group
        connection.metas.append(connection_meta_working_group)

    connection_meta_access_requests = ConnectionMeta.query.filter(ConnectionMeta.meta_key == 'access_requests', ConnectionMeta.entry_id == connection.id).first()
    if connection_meta_access_requests:
        connection_meta_access_requests.meta_value = stage_user.access_requests
    else:
        connection_meta_access_requests = ConnectionMeta()
        connection_meta_access_requests.meta_key = 'access_requests'
        connection_meta_access_requests.meta_value = stage_user.access_requests
        connection.metas.append(connection_meta_access_requests)

    connection_meta_google_email = ConnectionMeta.query.filter(ConnectionMeta.meta_key == 'google_email', ConnectionMeta.entry_id == connection.id).first()
    if connection_meta_google_email:
        connection_meta_google_email.meta_value = stage_user.google_email
    else:
        connection_meta_google_email = ConnectionMeta()
        connection_meta_google_email.meta_key = 'google_email'
        connection_meta_google_email.meta_value = stage_user.google_email
        connection.metas.append(connection_meta_google_email)

    connection_meta_github_username = ConnectionMeta.query.filter(ConnectionMeta.meta_key == 'github_username', ConnectionMeta.entry_id == connection.id).first()
    if connection_meta_github_username:
        connection_meta_github_username.meta_value = stage_user.github_username
    else:
        connection_meta_github_username = ConnectionMeta()
        connection_meta_github_username.meta_key = 'github_username'
        connection_meta_github_username.meta_value = stage_user.github_username
        connection.metas.append(connection_meta_github_username)

    connection_meta_slack_username = ConnectionMeta.query.filter(ConnectionMeta.meta_key == 'slack_username', ConnectionMeta.entry_id == connection.id).first()
    if connection_meta_slack_username:
        connection_meta_slack_username.meta_value = stage_user.slack_username
    else:
        connection_meta_slack_username = ConnectionMeta()
        connection_meta_slack_username.meta_key = 'slack_username'
        connection_meta_slack_username.meta_value = stage_user.slack_username
        connection.metas.append(connection_meta_slack_username)

    connection_meta_website = ConnectionMeta.query.filter(ConnectionMeta.meta_key == 'website', ConnectionMeta.entry_id == connection.id).first()
    if connection_meta_website:
        connection_meta_website.meta_value = stage_user.website
    else:
        connection_meta_website = ConnectionMeta()
        connection_meta_website.meta_key = 'website'
        connection_meta_website.meta_value = stage_user.website
        connection.metas.append(connection_meta_website)

    connection_meta_expertise = ConnectionMeta.query.filter(ConnectionMeta.meta_key == 'expertise', ConnectionMeta.entry_id == connection.id).first()
    if connection_meta_expertise:
        connection_meta_expertise.meta_value = stage_user.expertise
    else:
        connection_meta_expertise = ConnectionMeta()
        connection_meta_expertise.meta_key = 'expertise'
        connection_meta_expertise.meta_value = stage_user.expertise
        connection.metas.append(connection_meta_expertise)

    connection_meta_orcid = ConnectionMeta.query.filter(ConnectionMeta.meta_key == 'orcid', ConnectionMeta.entry_id == connection.id).first()
    if connection_meta_orcid:
        connection_meta_orcid.meta_value = stage_user.orcid
    else:
        connection_meta_orcid = ConnectionMeta()
        connection_meta_orcid.meta_key = 'orcid'
        connection_meta_orcid.meta_value = stage_user.orcid
        connection.metas.append(connection_meta_orcid)

    connection_meta_pm = ConnectionMeta.query.filter(ConnectionMeta.meta_key == 'pm', ConnectionMeta.entry_id == connection.id).first()
    if connection_meta_pm:
        connection_meta_pm.meta_value = stage_user.pm
    else:
        connection_meta_pm = ConnectionMeta()
        connection_meta_pm.meta_key = 'pm'
        connection_meta_pm.meta_value = stage_user.pm
        connection.metas.append(connection_meta_pm)

    connection_meta_pm_name = ConnectionMeta.query.filter(ConnectionMeta.meta_key == 'pm_name', ConnectionMeta.entry_id == connection.id).first()
    if connection_meta_pm_name:
        connection_meta_pm_name.meta_value = stage_user.pm_name
    else:
        connection_meta_pm_name = ConnectionMeta()
        connection_meta_pm_name.meta_key = 'pm_name'
        connection_meta_pm_name.meta_value = stage_user.pm_name
        connection.metas.append(connection_meta_pm_name)
        print(stage_user.pm_name)

    connection_meta_pm_email = ConnectionMeta.query.filter(ConnectionMeta.meta_key == 'pm_email', ConnectionMeta.entry_id == connection.id).first()
    if connection_meta_pm_email:
        connection_meta_pm_email.meta_value = stage_user.pm_email
    else:
        connection_meta_pm_email = ConnectionMeta()
        connection_meta_pm_email.meta_key = 'pm_email'
        connection_meta_pm_email.meta_value = stage_user.pm_email
        connection.metas.append(connection_meta_pm_email)

    connection_meta_email = ConnectionMeta.query.filter(ConnectionMeta.meta_key == 'email', ConnectionMeta.entry_id == connection.id).first()
    if connection_meta_email:
        connection_meta_email.meta_value = stage_user.email
    else:
        connection_meta_email = ConnectionMeta()
        connection_meta_email.meta_key = 'email'
        connection_meta_email.meta_value = stage_user.email
        connection.metas.append(connection_meta_email)

    connection_meta_phone = ConnectionMeta.query.filter(ConnectionMeta.meta_key == 'phone', ConnectionMeta.entry_id == connection.id).first()
    if connection_meta_phone:
        connection_meta_phone.meta_value = stage_user.phone
    else:
        connection_meta_phone = ConnectionMeta()
        connection_meta_phone.meta_key = 'phone'
        connection_meta_phone.meta_value = stage_user.phone
        connection.metas.append(connection_meta_phone)

    if not wp_user in connection.owners:
        connection.owners.append(wp_user)

# Deny the new user registration
def deny_stage_user(globus_user_id):
    stage_user = get_stage_user(globus_user_id)
    stage_user.deny = True
    db.session.commit()

# Get a list of all the pending registrations
def get_all_stage_users():
    stage_users = StageUser.query.order_by(StageUser.created_at).all()
    return stage_users

# Get a stage user new registration by a given globus_user_id
def get_stage_user(globus_user_id):
    stage_user = StageUser.query.filter(StageUser.globus_user_id == globus_user_id).first()
    return stage_user

# Get the exisiting user from `wp_users` table by looking for the globus id in `wp_usermeta` table
def get_wp_user(globus_user_id):
    wp_user_meta = WPUserMeta.query.filter(WPUserMeta.meta_key.like('openid-connect-generic-subject-identity'), WPUserMeta.meta_value == globus_user_id).first()
    if not wp_user_meta:
        return None
    wp_user = WPUser.query.filter(WPUser.id == wp_user_meta.user_id).first()
    return wp_user

# Find the matching profiles of a given user from the `wp_connections` table
# Scoring: last_name(6), first_name(4), email(10), organization(2)
def get_matching_profiles(last_name, first_name, email, organization):
    last_name_match_score = 6
    first_name_match_score = 4
    email_match_score = 10
    organization_match_score = 2

    # Use user email to search for matching profiles
    profiles_by_last_name = Connection.query.filter(Connection.last_name.like(f'%{last_name}%')).all()
    profiles_by_first_name = Connection.query.filter(Connection.first_name.like(f'%{first_name}%')).all()
    profiles_by_email = Connection.query.filter(Connection.email.like(f'%{email}%')).all()
    profiles_by_organization = Connection.query.filter(Connection.organization.like(f'%{organization}%')).all()
    
    # Now merge the above lists into one big list and pass into a set to remove duplicates
    profiles_set = set(profiles_by_last_name + profiles_by_first_name + profiles_by_email + profiles_by_organization)
    # convert back to a list for sorting later
    profiles_list = list(profiles_set)

    filtered_profiles = list()
    if len(profiles_list) > 0:
        for profile in profiles_list:
            pprint(profile)
            # Add a new aroperty
            profile.score = 0

            # See if the target profile can be found in each search resulting list
            # then add up the corresponding score
            if profile in profiles_by_last_name:
                profile.score = profile.score + last_name_match_score

            if profile in profiles_by_first_name:
                profile.score = profile.score + first_name_match_score

            if profile in profiles_by_email:
                profile.score = profile.score + email_match_score

            if profile in profiles_by_organization:
                profile.score = profile.score + organization_match_score
            
            # Ditch the profile that has matching score <= first_name_match_score
            if profile.score > first_name_match_score:
                # Deserialize the email value to a python dict
                deserilized_email_dict = phpserialize.loads(profile.email.encode('utf-8'), decode_strings=True)
                # Add another new property for display only
                if deserilized_email_dict:
                    profile.deserilized_email = (deserilized_email_dict[0])['address']
                filtered_profiles.append(profile)

    # Sort the filtered results by scoring
    profiles = sorted(filtered_profiles, key=lambda x: x.score, reverse=True)
    # Return a set of sorted matching profiles by score or an empty set if no match
    return profiles

# Get profile from `wp_connections` for a given connection ID
def get_connection_profile(connection_id):
    connection_profile = Connection.query.filter(Connection.id == connection_id).first()
    return connection_profile
    

# Login Required Decorator
# To use the decorator, apply it as innermost decorator to a view function. 
# When applying further decorators, always remember that the route() decorator is the outermost.
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'isAuthenticated' not in session:
            return render_template('login.html')
        return f(*args, **kwargs)
    return decorated_function

# Admin Required Decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not user_is_admin(session['globus_user_id']):
            return show_user_error("Access denied! You need to login as an admin user to access this page!")
        return f(*args, **kwargs)
    return decorated_function


# Routing

# Default
@app.route("/")
@login_required
def index():
    if user_is_admin(session['globus_user_id']):
        return redirect(url_for('registrations'))
    else:
        return redirect(url_for('register'))

# Redirect users from react app login page to Globus auth login widget then redirect back
@app.route('/login')
def login():
    redirect_uri = url_for('login', _external=True)
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
        user_info = get_globus_user_info(auth_token)

        # Store the resulting tokens in server session
        session['isAuthenticated'] = True
        session['globus_user_id'] = user_info['sub']
        session['name'] = user_info['name']
        session['email'] = user_info['email']
        session['auth_token'] = auth_token
        session['nexus_token'] = nexus_token
        session['transfer_token'] = transfer_token
      
        # Finally redirect back to the home page default route
        return redirect("/")

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
        '&redirect_uri={}'.format(app.config['FLASK_APP_BASE_URI']) +
        '&redirect_name={}'.format(app.config['FLASK_APP_NAME']))

    # Redirect the user to the Globus Auth logout page
    return redirect(globus_logout_url)

# Register is only for authenticated users who has never registered
@app.route("/register", methods=['GET', 'POST'])
@login_required
def register():
    # A not approved user can be a totally new user or user has a pending registration
    if not user_is_approved(session['globus_user_id']):
        if user_in_pending(session['globus_user_id']):
            # Check if this pening registration has been denied
            stage_user = get_stage_user(session['globus_user_id'])
            # Note: stage_user.deny stores 1 or 0 in database
            if not stage_user.deny:
                return show_user_info("Your registration has been submitted for approval. You'll get an email once it's approved or denied.")
            else:
                return show_user_info("Sorry, your registration has been denied.")
        else:
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
                #result['success'] = True

                # Currently no backend form validation
                # Only front end validation and reCAPTCHA
                if result['success']:
                    # CSRF check
                    session_csrf_token = session.pop('csrf_token', None)

                    if not session_csrf_token or session_csrf_token != request.form['csrf_token']:
                        return show_user_error("Oops! Invalid CSRF token!")
                    else:
                        user_info, profile_pic_option, img_to_upload = construct_user(request)

                        # Add user info to `stage_user` table for approval
                        try:
                            add_new_stage_user(user_info, profile_pic_option, img_to_upload)
                        except Exception as e: 
                            print("Failed to add new stage user, something wrong with add_new_stage_user()")
                            print(e)
                            return show_user_error("Oops! The system failed to submit your registration!")
                        else:
                            # Send email to admin for new user approval
                            try:
                                send_new_user_registered_mail(user_info)
                            except Exception as e: 
                                print("send email failed")
                                print(e)
                                return show_user_error("Oops! The system has submited your registration but failed to send the confirmation email!")

                        # Show confirmation
                        return show_user_confirmation("Your registration has been submitted for approval. You'll get an email once it's approved or denied.")
                # Show reCAPTCHA error
                else:
                    return show_user_error("Oops! reCAPTCHA error!")
            # Handle GET
            else:
                return show_registration_form()
    else:
        return show_user_info('You have already registered, you can click <a href="/profile">here</a> to view or update your user profile.')


# Profile is only for authenticated users who has an approved registration
@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    if user_is_approved(session['globus_user_id']):
        # Handle POST
        if request.method == 'POST':
            # CSRF check
            session_csrf_token = session.pop('csrf_token', None)
            if not session_csrf_token or session_csrf_token != request.form['csrf_token']:
                return show_user_error("Oops! Invalid CSRF token!")
            else:
                user_info, profile_pic_option, img_to_upload = construct_user(request)
                
                try:
                    # Update user profile in database
                    update_user_profile(user_info, profile_pic_option, img_to_upload)
                except Exception as e: 
                    print("Failed to update user profile!")
                    print(e)
                    return show_user_error("Oops! The system failed to update your profile changes!")
                else:
                    try:
                        # Send email to admin for user profile update
                        # so the admin can do furtuer changes in globus
                        send_user_profile_updated_mail(user_info)
                    except Exception as e: 
                        print("Failed to send user profile update email to admin.")
                        print(e)
                        return show_user_error("Your profile has been updated but the system failed to send confirmation email to admin. No worries, no action needed from you.")

                # Also notify the user
                return show_user_confirmation("Your profile information has been updated successfully. The admin will handle additional changes to your account as needed.")
        # Handle GET
        else:
            # Fetch user profile data
            try:
                wp_user = get_user_profile(session['globus_user_id'])
            except Exception as e: 
                print("Failed to get user profile for globus_user_id: " + session['globus_user_id'])
                print(e)
                return show_user_error("Oops! The system failed to query your profile data!")

            #pprint(wp_user['connection'] )

            # Parsing the json(from schema dump) to get initial user profile data
            connection_data = wp_user['connection'][0]
            initial_data = {
                'first_name': connection_data['first_name'],
                'last_name': connection_data['last_name'],
                #'email': connection_data['email'],
                'email': wp_user['user_email'],
                #'phone': phpserialize.loads(connection_data['phone_numbers'].encode())[0][b'number'].decode(),
                'phone': next((meta for meta in connection_data['metas'] if meta['meta_key'] == 'phone'), {'meta_value': ''})['meta_value'],
                'component': next((meta for meta in connection_data['metas'] if meta['meta_key'] == 'component'), {'meta_value': ''})['meta_value'],
                'other_component': next((meta for meta in connection_data['metas'] if meta['meta_key'] == 'other_component'), {'meta_value': ''})['meta_value'],
                'organization': next((meta for meta in connection_data['metas'] if meta['meta_key'] == 'organization'), {'meta_value': ''})['meta_value'],
                'other_organization': next((meta for meta in connection_data['metas'] if meta['meta_key'] == 'other_organization'), {'meta_value': ''})['meta_value'],
                'role': next((meta for meta in connection_data['metas'] if meta['meta_key'] == 'role'), {'meta_value': ''})['meta_value'],
                'other_role': next((meta for meta in connection_data['metas'] if meta['meta_key'] == 'other_role'), {'meta_value': ''})['meta_value'],
                'working_group': next((meta for meta in connection_data['metas'] if meta['meta_key'] == 'working_group'), {'meta_value': ''})['meta_value'],
                'access_requests': next((meta for meta in connection_data['metas'] if meta['meta_key'] == 'access_requests'), {'meta_value': ''})['meta_value'],
                'google_email': next((meta for meta in connection_data['metas'] if meta['meta_key'] == 'google_email'), {'meta_value': ''})['meta_value'],
                'github_username': next((meta for meta in connection_data['metas'] if meta['meta_key'] == 'github_username'), {'meta_value': ''})['meta_value'],
                'slack_username': next((meta for meta in connection_data['metas'] if meta['meta_key'] == 'slack_username'), {'meta_value': ''})['meta_value'],
                'website': next((meta for meta in connection_data['metas'] if meta['meta_key'] == 'website'), {'meta_value': ''})['meta_value'],
                'expertise': next((meta for meta in connection_data['metas'] if meta['meta_key'] == 'expertise'), {'meta_value': ''})['meta_value'],
                'orcid': next((meta for meta in connection_data['metas'] if meta['meta_key'] == 'orcid'), {'meta_value': ''})['meta_value'],
                'pm': 'Yes' if next((meta for meta in connection_data['metas'] if meta['meta_key'] == 'pm'), {'meta_value': ''})['meta_value'] == '1' else 'No',
                'pm_name': next((meta for meta in connection_data['metas'] if meta['meta_key'] == 'pm_name'), {'meta_value': ''})['meta_value'],
                'pm_email': next((meta for meta in connection_data['metas'] if meta['meta_key'] == 'pm_email'), {'meta_value': ''})['meta_value'],
            }

            # Convert string representation to dict
            if not initial_data['working_group'].strip() == '':
                initial_data['working_group'] = ast.literal_eval(initial_data['working_group'])
            if not initial_data['access_requests'].strip() == '':
                initial_data['access_requests'] = ast.literal_eval(initial_data['access_requests'])
       
            context = {
                'isAuthenticated': True,
                'username': session['name'],
                'csrf_token': generate_csrf_token(),
                'profile_pic_url': json.loads(connection_data['options'])['image']['meta']['original']['url']
            }
            
            # Merge initial_data and context as one dict 
            data = {**context, **initial_data}
            # Populate the user data in profile
            return render_template('profile.html', data = data)
    else:
        if user_in_pending(session['globus_user_id']):
            # Check if this pening registration has been denied
            stage_user = get_stage_user(session['globus_user_id'])
            if not stage_user.deny:
                return show_user_info("Your registration is pending for approval, you can view/update your profile once it's approved.")
            else:
                return show_user_info("Sorry, you don't have a profile because your registration has been denied.")
        else:
            return show_user_info('You have not registered, please click <a href="/register">here</a> to register.')


# Only for admin to see a list of pending new registrations
# Currently only handle approve and deny actions
# globus_user_id is optional
@app.route("/registrations/", defaults={'globus_user_id': None}, methods=['GET']) # need the trailing slash
@app.route("/registrations/<globus_user_id>", methods=['GET'])
@login_required
@admin_required
def registrations(globus_user_id):
    # Show a list of pending registrations if globus_user_id not present
    if not globus_user_id:
        stage_users = get_all_stage_users()
        context = {
            'isAuthenticated': True,
            'username': session['name'],
            'stage_users': stage_users
        }

        return render_template('all_registrations.html', data = context)
    else:
        # Show the individual pending registration
        stage_user = get_stage_user(globus_user_id)

        if not stage_user:
            return show_admin_error("This stage user does not exist!")
        else:
            # Check if there's any matching profiles in the `wp_connections` found
            matching_profiles = get_matching_profiles(stage_user.last_name, stage_user.first_name, stage_user.email, stage_user.organization)
            #pprint(vars(list(matching_profiles)[0]))
            context = {
                'isAuthenticated': True,
                'username': session['name'],
                'stage_user': stage_user,
                # Need to convert string representation of list to Python list
                'working_group_list': ast.literal_eval(stage_user.working_group),
                'access_requests_list': ast.literal_eval(stage_user.access_requests),
                'matching_profiles': matching_profiles
            }

            return render_template('individual_registration.html', data = context)

# Approve a registration
@app.route("/approve/<globus_user_id>", methods=['GET'])
@login_required
@admin_required
def approve(globus_user_id):
    # Check if there's a pending registration for the given globus user id
    stage_user = get_stage_user(globus_user_id)

    if not stage_user:
        return show_admin_error("This stage user does not exist!")
    else:
        try:
            approve_stage_user_by_creating_new(stage_user)
        except Exception as e: 
            print("Failed to approve new registration and create new user record.")
            print(e)
            return show_admin_error("This system failed to approve new registration and create new user record!")
        else:
            try:
                # Send email
                data = {
                    'first_name': stage_user.first_name,
                    'last_name': stage_user.last_name
                }
                send_new_user_approved_mail(stage_user.email, data = data)
            except Exception as e: 
                print("The new registration has been approved, but the system failed to send out user registration approval email.")
                print(e)
                return show_admin_error("The new registration has been approved, but the system failed to send out user registration approval email!")

        return show_admin_info("This registration has been approved successfully!")

# Deny a registration
@app.route("/deny/<globus_user_id>", methods=['GET'])
@login_required
@admin_required
def deny(globus_user_id):
    # Check if there's a pending registration for the given globus user id
    stage_user = get_stage_user(globus_user_id)

    if not stage_user:
        return show_admin_error("This stage user does not exist!")
    else:
        if stage_user.deny:
            return show_admin_info("This registration has already been denied!")
        else:
            try:
                deny_stage_user(globus_user_id)
            except Exception as e: 
                print("The system failed to deny user registration.")
                print(e)
                return show_admin_error("The system failed to deny user registration!")
            else:
                try:
                    # Send email
                    data = {
                        'first_name': stage_user.first_name,
                        'last_name': stage_user.last_name
                    }
                    send_new_user_denied_mail(stage_user.email, data = data)
                except Exception as e: 
                    print("Failed to send user registration denied email.")
                    print(e)
                    return show_admin_error("The user registration has been denied but the system failed to sent out email notification!")

            return show_admin_info("This registration has been denied!")


# Approve a registration by using an exisiting matching profile
@app.route("/match/<globus_user_id>/<connection_id>", methods=['GET'])
@login_required
@admin_required
def match(globus_user_id, connection_id):
    # Check if there's a pending registration for the given globus user id
    stage_user = get_stage_user(globus_user_id)
    if not stage_user:
        return show_admin_error("This stage user does not exist!")

    # Check if there's a connection profile for the given connection id
    connection_profile = get_connection_profile(connection_id)
    if not connection_profile:
        return show_admin_error("This connection profile does not exist!")

    try: 
        approve_stage_user_by_editing_matched(stage_user, connection_profile)
    except Exception as e: 
        print("Failed to approve the registration by using existing matched connection!")
        print(e) 
        return show_admin_error("Failed to approve the registration by using existing matched connection!")
    else:
        try:
            # Send email
            data = {
                'first_name': stage_user.first_name,
                'last_name': stage_user.last_name
            }
            send_new_user_approved_mail(stage_user.email, data = data)
        except Exception as e: 
            print("Failed to send user registration approval email.")
            print(e)
            return show_admin_error("The registration by using existing matched connection has been approved, but the system failed to sent out approval email!")

    return show_admin_info("This registration has been approved successfully by using an exisiting mathcing profile!")





# Run Server
if __name__ == "__main__":
    app.run(debug=True)
