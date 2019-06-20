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
from functools import wraps


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
def add_new_stage_user(new_user, img_to_upload):
    # Add user profile image data
    if not img_to_upload:
        BASE = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f"{new_user['globus_user_id']}.jpg"))
        copy2(os.path.join(BASE, 'avatar/', 'noname.jpg'), save_path)
        new_user['photo'] = save_path
    else:
        if new_user['photo_url'] != '':
            response = requests.get(new_user['photo_url'])
            img_file = Image.open(BytesIO(response.content))
            extension = img_file.format
        else:
            _, extension = img_to_upload.filename.rsplit('.', 1)
            img_file = img_to_upload
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f"{new_user['globus_user_id']}.{extension}"))
        img_file.save(save_path)
        new_user['photo'] = save_path
    
    try:
        new_stage_user = StageUser(new_user)
    except:
        print('User data is not valid')
    
    if StageUser.query.filter(StageUser.globus_user_id == new_stage_user.globus_user_id).first():
        print('The same stage user exists')
    else:
        try:
            db.session.add(new_stage_user)
            db.session.commit()
        except:
            print('Failed to add a new stage user')

# Query the user data to populate into profile form
def get_user_profile(globus_user_id):
    user_meta = WPUserMeta.query.filter(WPUserMeta.meta_key.like('openid-connect-generic-subject-identity'), WPUserMeta.meta_value == globus_user_id).first()
    if not user_meta:
        print('No user found with globus_user_id: ' + globus_user_id)
        return False
    users = [user_meta.user]
    result = wp_users_schema.dump(users)
    user = result[0][0]
    
    return user

# TO-DO
def update_user_profile(j_user, img, id):
    """
    Match a wp user to a existing user if id present
    Create a new user if id not present
    """
    wp_user = WPUser.query.get(id)

    if not j_user['photo_url'] == '':
        response = requests.get(j_user['photo_url'])
        img_file = Image.open(BytesIO(response.content))
        extension = img_file.format
    else:
        _, extension = img.filename.rsplit('.', 1)
        img_file = img
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
        print('Failed to update user profile')

    print('User profile updated successfully')

# Approving by moving user data from `stage_user` into `wp_user`` and `wp_connections`
# also add the ids to the `user_connection` table
def approve_stage_user(globus_user_id):
    stage_user = get_stage_user(globus_user_id)
    pprint(stage_user)
    try:
        new_wp_user = WPUser()
        assign_wp_user(new_wp_user, stage_user, None)
        db.session.add(new_wp_user)
        db.session.delete(stage_user)
        db.session.commit()
    except Exception as e:
        print(e)
        print("Exception in user code:")
        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)
        print('Database opertations failed during approving sage user')

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

# Find the matching profiles of a given user from the `wp_connections` table
def get_matching_profiles(last_name, first_name, organization):
    # Use user email to search for matching profiles
    profiles_by_last_name = Connection.query.filter(Connection.email.like(f'%{last_name}%')).all()
    profiles_by_first_name = Connection.query.filter(Connection.email.like(f'%{first_name}%')).all()
    profiles_by_organization = Connection.query.filter(Connection.email.like(f'%{organization}%')).all()
    
    # Now merge the above lists into one big list
    profiles = profiles_by_last_name + profiles_by_first_name + profiles_by_organization
    
    # Return a list of matching profiles or an empty list if no match
    if len(profiles) > 0:
        return profiles
    else:
        return list()

    
def generate_password():
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    passlen = 16
    return "".join(random.sample(s, passlen))

def assign_wp_user(wp_user, user_obj, connection=None, mode='CREATE'):
    # First get the id of admin user in `wp_usermeta` table
    admin_id = WPUserMeta.query.filter(WPUserMeta.meta_key.like('openid-connect-generic-subject-identity'), WPUserMeta.meta_value == session['globus_user_id']).first().user_id

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
        # Disable for now
        #pathlib.Path(app.config.get('CONNECTION_IMAGE_PATH') + user_obj.first_name.lower() + '-' + user_obj.last_name.lower() ).mkdir(parents=True, exist_ok=True)
        #copyfile(user_obj.photo, app.config.get('CONNECTION_IMAGE_PATH') + user_obj.first_name.lower() + '-' + user_obj.last_name.lower() + "/" + photo_file_name)
        connection.options = "{\"entry\":{\"type\":\"individual\"},\"image\":{\"linked\":true,\"display\":true,\"name\":{\"original\":\"" + photo_file_name + "\"},\"meta\":{\"original\":{\"name\":\"" + photo_file_name + "\",\"path\":\"" + app.config.get('CONNECTION_IMAGE_PATH') + user_obj.first_name.lower() + '-' + user_obj.last_name.lower() + "\\/" + photo_file_name + "\",\"url\": \"" + app.config.get('CONNECTION_IMAGE_URL') + user_obj.first_name.lower() + '-' + user_obj.last_name.lower() + "\\/" + photo_file_name + "\",\"width\":200,\"height\":200,\"size\":\"width=\\\"200\\\" height=\\\"200\\\"\",\"mime\":\"image\\/jpeg\",\"type\":2}}}}"
    else:
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

# Register is only for authenticated users who never registered
@app.route("/register", methods=['GET', 'POST'])
@login_required
def register():
    # A not approved user can be a totally new user or user has a pending registration
    if not user_is_approved(session['globus_user_id']):
        if user_in_pending(session['globus_user_id']):
            return show_user_confirmation("Your registration has been submitted for approval. You'll get an email once it's approved or denied.")
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
                result['success'] = True

                # Currently no backend form validation
                # Only front end validation and reCAPTCHA - Zhou
                if result['success']:
                    # CSRF check
                    session_csrf_token = session.pop('csrf_token', None)

                    if not session_csrf_token or session_csrf_token != request.form['csrf_token']:
                        return show_user_error("Oops! Invalid CSRF token!")
                    else:
                        new_user, img_to_upload = construct_user(request)

                        # Add user info to `stage_user` table for approval
                        try:
                            add_new_stage_user(new_user, img_to_upload)
                        except:
                            print("Failed to add new stage user, something wrong with add_new_stage_user()")

                        # Send email to admin for new user approval
                        try:
                            send_new_user_registered_mail(new_user)
                        except Exception as e: 
                            print(e)
                            print("send email failed")
                            pass

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
                new_user, img_to_upload = construct_user(request)
                wp_user_id = request.POST['wp_user_id']

                # Update user profile in database
                update_user_profile(new_user, img_to_upload, wp_user_id)

                try:
                    # Send email to admin for user profile update
                    # so the admin can do furtuer changes in globus
                    send_user_profile_update_mail(new_user)
                except Exception as e: 
                    print(e)
                    print("Failed to send user profile update email to admin.")
                    pass

                    # Also notify the user
                    return show_user_confirmation("Your profile information has been updated successfully. The admin will do any additional changes to your account is need.")
        # Handle GET
        else:
            # Fetch user profile data
            wp_user = get_user_profile(session['globus_user_id'])

            # Parsing the json to get initial user profile data
            initial_data = {
                'first_name': wp_user['connection'][0]['first_name'],
                'last_name': wp_user['connection'][0]['last_name'],
                #'email': wp_user['connection'][0]['email'],
                'email': wp_user['user_email'],
                #'phone': loads(wp_user['connection'][0]['phone_numbers'].encode())[0][b'number'].decode(),
                'phone': next((meta for meta in wp_user['connection'][0]['metas'] if meta['meta_key'] == 'phone'), {'meta_value': ''})['meta_value'],
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

            # Something wrong with the code below, error

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
            # Populate the user data in profile
            return render_template('profile.html', data = {**context, **initial_data})
    else:
        if user_in_pending(session['globus_user_id']):
            return show_user_info("Your registration is pending for approval, you can view/update your profile once it's approved.")
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
            matching_profiles = get_matching_profiles(stage_user.last_name, stage_user.first_name, stage_user.organization)
            pprint(vars(matching_profiles[0]))
            context = {
                'isAuthenticated': True,
                'username': session['name'],
                'stage_user': stage_user,
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
        approve_stage_user(globus_user_id)
        # Send email
        data = {
            'first_name': stage_user.first_name,
            'last_name': stage_user.last_name
        }
        send_new_user_approved_mail(stage_user.email, data = data)
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
            deny_stage_user(globus_user_id)
            # Send email
            data = {
                'first_name': stage_user.first_name,
                'last_name': stage_user.last_name
            }
            send_new_user_denied_mail(stage_user.email, data = data)
            return show_admin_info("This registration has been denied!")































# APIs, will need to be converted into internal functions later
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
            new_wp_user = WPUser()
            assign_wp_user(new_wp_user, stage_user, connection)
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



# Run Server
if __name__ == "__main__":
    app.run(debug=True)