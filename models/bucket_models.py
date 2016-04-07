from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager
from config.config import DevelopmentConfig
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import datetime

# creates the flask app
app = Flask(__name__)

# configures the app
# app.config.from_pyfile('config.cfg')
app.config.from_object(DevelopmentConfig)


# creates the database instance object
db = SQLAlchemy(app)

migrate = Migrate(app, db, "models/migrations")
migrate_manager = Manager(app)
migrate_manager.add_command('db', MigrateCommand)


class BucketLists(db.Model):
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

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    created_by = db.Column(db.String(), db.ForeignKey('auth.id'))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)

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


class Items(db.Model):
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
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    done = db.Column(db.Boolean)
    bid = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def __init__(self, name, done):
        """
        Initialize a bucketlist item.
        Args:
           self
           name: Name of the bucketlist item.
           done: Boolean to indicate whether the item has been completed or not.
        """
        self.name = name
        self.done = done

    def __repr__(self):
        """
        Create a string representation of a bucketlist.
        Args:
            self
        Returns:
            The bucketlist item's name as a String
        """
        return '<Name %r>' % self.name


class Auth(db.Model):
    """
    Auth model class
    Attributes:
        id: The id of the user.
        name: The name of the user.

    Methods:
        __init__: Initializes a new user.
        __repr__: Creates a representation of a user.
    """

    # sets a predefined tablename
    __tablename__ = "auth"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __init__(self, name):
        """
        Initialize a user.
        Args:
           self
           name: Name of the user.
        """
        self.name = name

    def __repr__(self):
        """
        Create a string representation of a user.
        Args:
            self
        Returns:
            The user's name as a String
        """
        return 'Name : %s ' % self.name

manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(
    BucketLists, methods=['GET', 'POST', 'DELETE', 'PUT'], url_prefix='/v1')
manager.create_api(
    Items, methods=['POST', 'DELETE', 'PUT'], url_prefix='/v1')
manager.create_api(Auth, methods=['GET'], url_prefix='/v1')
