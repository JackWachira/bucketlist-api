from flask_sqlalchemy import SQLAlchemy
from config.config import DevelopmentConfig
import datetime
from marshmallow import validate, Schema, fields
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

# creates the database instance object
db = SQLAlchemy()


class DbOperations():
    """
    Class to do database operations

    Methods:
        add:    Saves a record to database.
        update: Updates a record in the database.
        delete: Deletes a record in the database.
    """

    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()


class BucketLists(db.Model, DbOperations):
    """
    BucketList model class
    Attributes:
        id: The id of the bucketlist.
        name: The name of the bucketlist.
        created_by: The ID of the creator(user) of the bucketlist.
        date_created: The date the bucketlist was created.
        date_modified: The date the bucketlist was modified.
        items: A relationship object between the bucketlist and its items.

    Methods:
        __init__: Initializes a new bucketlist.
        __repr__: Creates a representation of a bucketlist.
    """

    # sets a predefined tablename
    __tablename__ = "bucketlists"

    # print(current_time, file=sys.stderr)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    items = db.relationship(
        'Items', backref='bucket', lazy='dynamic')

    def __init__(self, name, created_by):
        """
        Initialize a bucketlist.
        Args:
           self
           name: Name of the bucketlist.
           created_by: The ID of the creator(user) of the bucketlist.
        """
        self.name = name
        self.created_by = created_by

    def __repr__(self):
        """
        Create a string representation of a bucketlist.
        Args:
            self
        Returns:
            The bucketlist name as a String
        """
        return '<Name %r>' % self.name


class Date(fields.Field):
    """
    Overrides Marshmallow Date serialize method

    Return:
        All or specific bucketlists belonging to the logged in user.
    """

    def _serialize(self, value, attr, obj):
        """
        Serialize a datetime.date object to a formatted string
        """
        if value is None:
            return None
        try:
            return value.strftime("%Y-%m-%d %H:%M:%S")
        except AttributeError:
            self.fail('format', input=value)
        return value


class ItemsSchema(Schema):
    """
    Class for serializing and deserializing Items model class

    Attributes:
        id: The id of the bucketlist item.
        name: The name of the bucketlist item.
        date_created: The date the bucketlist item was created.
        date_modified: The date the bucketlist item was modified.
        done: Boolean to indicate whether the item has been completed or not.
    """
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    name = fields.String(
        required=True, error_messages={'required': 'Name is required'})
    done = fields.Boolean(
        required=True, error_messages={'required': 'Done is required'})
    date_created = Date()
    date_modified = Date()

    class Meta:
        """
        Options object for a Schema.

        Available options:
        - ``strict``: If `True`, raise errors during marshalling rather than
            storing them.
        -
        """
        strict = True


class BucketListsSchema(Schema):

    """
    Class for serializing and deserializing BucketList model class

    Attributes:
        id: The id of the bucketlist.
        name: The name of the BucketList.
        date_created: The date the bucketlist was created.
        date_modified: The date the bucketlist was modified.
        created_by: The ID of the creator(user) of the bucketlist.
        items: Items in the bucketlist
    """
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    created_by = fields.Integer()
    name = fields.String(
        required=True, error_messages={'required': 'Name is required'})
    date_created = Date()
    date_modified = Date()
    items = fields.Nested(ItemsSchema, many=True)

    class Meta:
        """
        Options object for a Schema.

        Available options:
        - ``strict``: If `True`, raise errors during marshalling rather than
            storing them.
        -
        """
        strict = True


class Items(db.Model, DbOperations):
    """
    BucketListItems model class
    Attributes:
        id: The id of the bucketlist item.
        name: The name of the bucketlist item.
        date_created: The date the bucketlist item was created.
        date_modified: The date the bucketlist item was modified.
        done: Boolean to indicate whether the item has been completed or not.
        bid: The id of the bucket which the item is in

    Methods:
        __init__: Initializes a new bucketlist item.
        __repr__: Creates a representation of a bucketlist item.
    """

    # sets a predefined tablename
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    done = db.Column(db.Boolean)
    bid = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def __init__(self, name, done, bid):
        """
        Initialize a bucketlist item.
        Args:
           self
           name: Name of the bucketlist item.
           done: Boolean to indicate whether the item has been completed or not.
        """
        self.name = name
        self.done = done
        self.bid = bid

    def __repr__(self):
        """
        Create a string representation of a bucketlist.
        Args:
            self
        Returns:
            The bucketlist item's name as a String
        """
        return '<Name %r>' % self.name


class UsersSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    username = fields.String(
        required=True, error_messages={'required': 'Username is required'})
    password = fields.String(
        required=True, error_messages={'required': 'Password is required'}, load_only=True)
    date_created = fields.Date()
    date_modified = fields.Date()

    class Meta:
        type_ = 'users'
        strict = True


class User(db.Model, DbOperations):
    """
    User model class
    Attributes:
        id: The id of the user.
        username: The name of the user.

    Methods:
        __init__: Initializes a new user.
        __repr__: Creates a representation of a user.
    """

    # sets a predefined tablename
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __init__(self, username):
        """
        Initialize a user.
        Args:
           self
           name: Name of the user.
        """
        self.username = username

    def __repr__(self):
        """
        Create a string representation of a user.
        Args:
            self
        Returns:
            The user's name as a String
        """
        return 'Name : %s ' % self.username

    def hash_password(self, password):
        """
        Encrypts password
        Args:
            self, password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Verifies password
        Args:
            self, password
        """
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=3000):
        """
        Generates auth token
        Args:
            self, expiration
        Returns:
            The authentication token
        """
        s = Serializer(DevelopmentConfig.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        """
        Verifies auth token
        Args:
            token
        Returns:
            A user object
        """
        s = Serializer(DevelopmentConfig.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user
