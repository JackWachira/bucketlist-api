from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.config import DevelopmentConfig
from utils.utils import Utils
import datetime
from marshmallow import validate, Schema, fields, pre_load, post_load, post_dump
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

# creates the database instance object
db = SQLAlchemy()


class DbOperations():

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
    # date_created = db.Column(db.DateTime, default=current_time)
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
    """Override marshmallow Date serialize method"""

    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        try:
            return value.strftime("%Y-%m-%d %H:%M:%S")
        except AttributeError:
            self.fail('format', input=value)
        return value


class ItemsSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    name = fields.String(
        required=True, error_messages={'required': 'Name is required'})
    done = fields.Boolean(
        required=True, error_messages={'required': 'Done is required'})
    date_created = Date()
    date_modified = Date()

    class Meta:
        type_ = 'items'
        strict = True


class BucketListsSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    created_by = fields.Integer(
        required=True, error_messages={'required': 'Created by is required'})
    name = fields.String(
        required=True, error_messages={'required': 'Name is required'})
    date_created = Date()
    date_modified = Date()
    items = fields.Nested(ItemsSchema, many=True)

    class Meta:
        type_ = 'bucketlists'
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
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=30000000000):
        s = Serializer(DevelopmentConfig.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(DevelopmentConfig.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user
