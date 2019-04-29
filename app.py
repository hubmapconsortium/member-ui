from flask import Flask, request, jsonify, Response
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

# Init app
app = Flask(__name__)

# Database
app.config.from_pyfile('config.cfg')

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
    role = db.Column(db.String(100))
    group = db.Column(db.String(500)) # Checkboxes
    photo = db.Column(db.String(500))
    photo_url = db.Column(db.String(500))
    access_requests = db.Column(db.String(500)) # Checkboxes
    alt_email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    website = db.Column(db.String(500))
    biosketch = db.Column(db.String(200))
    expertise = db.Column(db.String(500))
    orcid = db.Column(db.String(100))
    github = db.Column(db.String(200))
    slack = db.Column(db.String(200))
    stack = db.Column(db.String(200))
    assistant = db.Column(db.Boolean)
    assistant_email = db.Column(db.String(100))

    def __init__(self, a_dict):
        try:
            self.globus_user_id = a_dict['globus_user_id'] if 'globus_user_id' in a_dict else ''
            self.email = a_dict['email'] if 'email' in a_dict else ''
            self.first_name = a_dict['first_name'] if 'first_name' in a_dict else ''
            self.last_name = a_dict['last_name'] if 'last_name' in a_dict else ''
            self.component = a_dict['component'] if 'component' in a_dict else ''
            self.other_component = a_dict['other_component'] if 'other_component' in a_dict else ''
            self.organization = a_dict['organization'] if 'organization' in a_dict else ''
            self.role = a_dict['role'] if 'role' in a_dict else ''
            self.group = str(a_dict['group']) if 'group' in a_dict else ''
            self.photo = a_dict['photo'] if 'photo' in a_dict else ''
            self.photo_url = a_dict['photo_url'] if 'photo_url' in a_dict else ''
            self.access_requests = str(a_dict['access_requests']) if 'access_requests' in a_dict else ''
            self.alt_email = a_dict['alt_email'] if 'alt_email' in a_dict else ''
            self.phone = a_dict['phone'] if 'phone' in a_dict else ''
            self.website = a_dict['website'] if 'website' in a_dict else ''
            self.biosketch = a_dict['biosketch'] if 'biosketch' in a_dict else ''
            self.expertise = a_dict['expertise'] if 'expertise' in a_dict else ''
            self.orcid = a_dict['orcid'] if 'orcid' in a_dict else ''
            self.github = a_dict['github'] if 'github' in a_dict else ''
            self.slack = a_dict['slack'] if 'slack' in a_dict else ''
            self.stack = a_dict['stack'] if 'stack' in a_dict else ''
            self.assistant = a_dict['assistant'] if 'assistant' in a_dict else ''
            self.assistant_email = a_dict['assistant_email'] if 'assistant_email' in a_dict else ''
        except e:
            raise e

# StageUser Schema
class StageUserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'globus_user_id', 'email', 'first_name', 'last_name', 'component', 'other_component', 'organization', 
                    'role', 'group', 'photo', 'photo_url', 'access_requests', 'alt_email', 'phone', 'website',
                    'biosketch', 'orcid', 'github', 'slack', 'stack', 'assistant', 'assistant_email')

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

# APIs
@app.route('/stage_user', methods=['GET'])
def get_stage_users():
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

@app.route('/stage_user', methods=['POST'])
def add_stage_user():
    if 'json' not in request.form:
        return Response('No user data', status=400)

    j_stage_user = json.loads(request.form['json'])
    
    if 'img' not in request.files:
        img_file = open('./avatar/noname.jpg', 'r')
        j_stage_user['photo'] = './avatar/noname.jpg'
    else:
        filename, exetension = request.files['img'].filename.rsplit('.', 1)
        img_file = request.files['img']
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f"{j_stage_user['globus_user_id']}.{exetension}"))
        img_file.save(save_path)
        j_stage_user['photo'] = save_path
    try:
        new_stage_user = StageUser(j_stage_user)
    except:
        return Response('User data is not valid', status=400)
    
    if StageUser.query.filter(StageUser.globus_user_id == new_stage_user.globus_user_id).first():
        return Response('Stage user created', status=201)
    else:
        db.session.add(new_stage_user)
        db.session.commit()
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
    if stage_user and wp_user:
        # update wp_user
        wp_user.user_login = stage_user.email
        wp_user.user_pass = generate_password()
        for meta in wp_user.metas:
            if meta.meta_key == "wp_capabilities":
                meta.meta_value = "a:1:{s:6:\"member\";b:1;}"

        # delete stage user
        db.session.delete(stage_user)
        db.session.commit()

        m_result = wp_user_schema.dump(wp_user)
        return jsonify(m_result)
    else:
        try:
            new_wp_user = WPUser()
            new_wp_user.user_login = stage_user.email
            new_wp_user.user_email = stage_user.email
            new_wp_user.user_pass = generate_password()
            meta_capabilities = WPUserMeta()
            meta_capabilities.meta_key = "wp_capabilities"
            meta_capabilities.meta_value = "a:1:{s:6:\"member\";b:1;}"
            new_wp_user.metas.append(meta_capabilities)
            meta_globus_user_id = WPUserMeta()
            meta_globus_user_id.meta_key = "openid-connect-generic-subject-identity"
            meta_globus_user_id.meta_value = stage_user.globus_user_id
            new_wp_user.metas.append(meta_globus_user_id)

            if not connection:
                connection = Connection()

            connection.owners.append(new_wp_user)
            connection.email = stage_user.email
            connection.first_name = stage_user.first_name
            connection.last_name = stage_user.last_name
            connection.organization = stage_user.organization

            photo_file_name = stage_user.photo.split('/')[-1]
            pathlib.Path("/home/webadmin/collab-website/wp-site/wp-content/uploads/connections-images/" + stage_user.globus_user_id ).mkdir(parents=True, exist_ok=True)
            copyfile(stage_user.photo, "/home/webadmin/collab-website/wp-site/wp-content/uploads/connections-images/" + stage_user.globus_user_id + "/" + photo_file_name)
            connection.options = "{\"entry\":{\"type\":\"individual\"},\"image\":{\"linked\":true,\"display\":true,\"name\":{\"original\":\"" + photo_file_name + "\"},\"meta\":{\"original\":{\"name\":\"" + photo_file_name + "\",\"path\":\"\\/home\\/webadmin\\/collab-website\\/wp-site\\/wp-content\\/uploads\\/connections-images\\/" + stage_user.globus_user_id + "\\/" + photo_file_name + "\",\"url\":\"https:\\/\\/dev2.hubmapconsortium.org\\/wp-content\\/uploads\\/connections-images\\/" + stage_user.globus_user_id + "\\/" + photo_file_name + "\",\"width\":200,\"height\":200,\"size\":\"width=\\\"200\\\" height=\\\"200\\\"\",\"mime\":\"image\\/jpeg\",\"type\":2}}}}"
            connection.phone_numbers = "a:1:{i:0;a:7:{s:2:\"id\";i:417;s:4:\"type\";s:9:\"workphone\";s:4:\"name\";s:10:\"Work Phone\";s:10:\"visibility\";s:6:\"public\";s:5:\"order\";i:0;s:9:\"preferred\";b:0;s:6:\"number\";s:10:\"" + stage_user.phone + "\";}}"

            connection_meta_role = ConnectionMeta()
            connection_meta_role.meta_key = 'role'
            connection_meta_role.meta_value = stage_user.role
            connection.metas.append(connection_meta_role)
            connection_meta_working_group = ConnectionMeta()
            connection_meta_working_group.meta_key = 'working_group'
            connection_meta_working_group.meta_value = stage_user.group
            connection.metas.append(connection_meta_working_group)
            connection_meta_access_requests = ConnectionMeta()
            connection_meta_access_requests.meta_key = 'access_requests'
            connection_meta_access_requests.meta_value = stage_user.access_requests
            connection.metas.append(connection_meta_access_requests)
            connection_meta_alt_email = ConnectionMeta()
            connection_meta_alt_email.meta_key = 'alt_email'
            connection_meta_alt_email.meta_value = stage_user.alt_email
            connection.metas.append(connection_meta_alt_email)
            connection_meta_website = ConnectionMeta()
            connection_meta_website.meta_key = 'website'
            connection_meta_website.meta_value = stage_user.website
            connection.metas.append(connection_meta_website)
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
            connection_meta_github = ConnectionMeta()
            connection_meta_github.meta_key = 'github'
            connection_meta_github.meta_value = stage_user.github
            connection.metas.append(connection_meta_github)
            connection_meta_slack = ConnectionMeta()
            connection_meta_slack.meta_key = 'slack'
            connection_meta_slack.meta_value = stage_user.slack
            connection.metas.append(connection_meta_slack)
            connection_meta_stack = ConnectionMeta()
            connection_meta_stack.meta_key = 'stack'
            connection_meta_stack.meta_value = stage_user.stack
            connection.metas.append(connection_meta_stack)
            connection_meta_assistant = ConnectionMeta()
            connection_meta_assistant.meta_key = 'assistant'
            connection_meta_assistant.meta_value = stage_user.assistant
            connection.metas.append(connection_meta_assistant)
            connection_meta_assistant_email = ConnectionMeta()
            connection_meta_assistant_email.meta_key = 'assistant_email'
            connection_meta_assistant_email.meta_value = stage_user.assistant_email
            connection.metas.append(connection_meta_assistant_email)
            
            
            ## default value ##
            connection.date_added = str(datetime.today().timestamp())
            connection.entry_type = 'individual'
            connection.visibility = 'public'
            connection.slug = stage_user.first_name.lower() + '-' + stage_user.last_name.lower()
            connection.family_name = ''
            connection.honorific_prefix = ''
            connection.middle_name = ''
            connection.honorific_suffix = ''
            connection.title = stage_user.role
            connection.department = stage_user.component
            connection.contact_first_name = ''
            connection.contact_last_name = ''
            connection.addresses = 'a:0:{}'
            connection.im = 'a:0:{}'
            connection.social = 'a:0:{}'
            connection.links = 'a:0:{}'
            connection.dates = 'a:0:{}'
            connection.birthday = ''
            connection.anniversary = ''
            connection.bio = stage_user.website
            connection.notes = ''
            connection.excerpt = ''
            connection.added_by = WPUser.query.filter(WPUser.user_login == app.config.get('ADMIN_USERNAME')).first().id
            connection.edited_by = WPUser.query.filter(WPUser.user_login == app.config.get('ADMIN_USERNAME')).first().id
            connection.owner = WPUser.query.filter(WPUser.user_login == app.config.get('ADMIN_USERNAME')).first().id
            connection.user = 0
            connection.status = 'approved'

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

        return Response('Stage user updated', status=200)

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
def approve_user(id):
    """
    Match a wp user to a existing user if id present
    Create a new user if id not present
    """
    wp_user = WPUser.query.get(id)
    if 'user_id' in request.form:
        # update user
        user = User.query.get(request.form['user_id'])
    else:
        # new user
        pass

    # update user fields
    return user_schema.jsonify(user)

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

@app.rout('/hello', methods=['GET'])
def hello():
    return Response("Hello world!", 200)

# Run Server
if __name__ == "__main__":
    app.run(debug=True)