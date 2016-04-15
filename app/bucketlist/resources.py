from flask import Blueprint, g, jsonify, make_response, request
from flask_restful import Api, Resource
from app.bucketlist.models import BucketLists, BucketListsSchema, db, Items, ItemsSchema, UsersSchema, User
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from marshmallow import ValidationError
from flask.ext.httpauth import HTTPBasicAuth
from flask_restful import reqparse
from functools import wraps

# Define blueprint
bucket_list = Blueprint('bucketlists', __name__)

# Initialize flask application
api = Api(bucket_list)

# Define schemas for the models
bucket_list_schema = BucketListsSchema()
items_schema = ItemsSchema()
users_schema = UsersSchema()

# Initialize auth
auth = HTTPBasicAuth()


def handle_exceptions(f):
    """Decorator to handle Validation and SQLAlchemyErrors"""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 400
            return resp
        except IntegrityError as e:
            resp = jsonify({"error": "The username is already taken"})
            resp.status_code = 401
            return resp
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 400
            return resp
    return decorated


class BucketList(Resource):
    """
    Handles requests to bucketlists.

    Resource urls:
        '/bucketlists/'
        '/bucketlists/<bucket_id>'

    Requests Allowed:
        'GET', 'POST', 'PUT', 'DELETE'
    """

    @auth.login_required
    def get(self, bucket_id=0):
        """
        Queries bucketlists.

        Args:
            self,bucket_id

        Return:
            All or specific bucketlists belonging to the logged in user.
        """

        search = False  # Flag to determine whether to search.

        # Get page and limit from request url.
        try:
            page = int(request.args.get('page'))
            limit = int(request.args.get('limit'))
        except:
            page = 1
            limit = 20

        # Get search parameter from request.
        q = request.args.get('q')
        if q is not None:
            search = True

        if bucket_id == 0:  # Bucket id is not specified in request
            if search:  # Search for specific bucket list for user
                record_query = BucketLists.query.filter_by(
                    name=q, created_by=g.user.id).paginate(
                    page, limit, False)
            else:  # Query all bucket lists for user
                record_query = BucketLists.query.filter_by(
                    created_by=g.user.id).paginate(page, limit, False)

            # Serialize the query results in the JSON API format
            results = bucket_list_schema.dump(
                record_query.items, many=True).data

        else:  # Bucket id is specified in request
            bucket_list_query = BucketLists.query.get_or_404(bucket_id)
            if bucket_list_query.created_by == g.user.id:
                # return results if they were created by user else return error
                # message
                results = bucket_list_schema.dump(
                    bucket_list_query, many=False).data
            else:
                return {"message": "Unauthorized"}, 401
            # Serialize the query results in the JSON API format

        return results, 200

    @handle_exceptions
    @auth.login_required
    def post(self, bucket_id=0):
        """
        Creates bucketlists.

        Args:
            self, bucket_id

        Return:
            Creates a bucket for a logged in user
        """

        # parse incoming request data
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        args = parser.parse_args()
        name = args['name']

       # Validate the data or raise a Validation error if incorrect
        bucket_list_schema.validate(args)
        # Create a BucketList with the API data recieved
        bucketlist = BucketLists(
            name, g.user.id)
        # Commit data
        bucketlist.add(bucketlist)
        # Serialize the query results in the JSON API format
        results = bucket_list_schema.dump(bucketlist).data
        return results, 201

    @auth.login_required
    @handle_exceptions
    def put(self, bucket_id=0):
        """
        Updates bucketlists.

        Args:
            self, bucket_id

        Return:
            Updated bucket list for a logged in user
        """
        # Bucket id not supplied
        if bucket_id != 0:
            # query for bucket list by its id
            bucketlist = BucketLists.query.get_or_404(bucket_id)

            # parse incoming request data
            parser = reqparse.RequestParser()
            parser.add_argument('name')
            args = parser.parse_args()

            # Validate the data or raise a Validation error if incorrect
            bucket_list_schema.validate(args)
            # Set BucketList object values with the API data recieved
            for key, value in args.items():
                setattr(bucketlist, key, value)
            bucketlist.update()
            # Serialize the query results in the JSON API format
            return bucket_list_schema.dump(bucketlist).data, 200

        else:
            resp = jsonify({"error": "Bucket id missing"})
            resp.status_code = 401
            return resp

    @auth.login_required
    @handle_exceptions
    def delete(self, bucket_id=0):
        """
        Deletes a bucketlist.

        Args:
            self, bucket_id
        Return:
            Delete successfully message
        """
        bucket_list = BucketLists.query.get_or_404(bucket_id)
        bucket_list.delete(bucket_list)
        return jsonify({'message': 'Bucketlist ' + bucket_id +
                        ' deleted successfully.'})


class BucketListItem(Resource):
    """
    Handles requests to bucketlist items.

    Resource urls:
        '/bucketlists/<bucket_id>/items/'
        '/bucketlists/<bucket_id>/items/<item_id>'

    Requests Allowed:
        'POST', 'PUT', 'DELETE'
    """
    @auth.login_required
    @handle_exceptions
    def post(self, bucket_id, item_id=0):
        """
        Creates bucketlist items.

        Args:
            self, bucket_id, item_id

        Return:
            Creates a bucket item for a logged in user
        """

        # parse incoming request data
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('done')
        args = parser.parse_args()
        name = args['name']
        done = args['done']

        # Validate the data or raise a Validation error if incorrect
        items_schema.validate(args)
        # Check if bucket list exists
        BucketLists.query.get_or_404(bucket_id)

        # Create a Bucket item object with the API data recieved
        bucket_items = Items(
            name, bool(done), bucket_id)
        # Commit data
        bucket_items.add(bucket_items)

        # Serialize the query results in the JSON API format
        results = items_schema.dump(bucket_items).data
        return results, 201

    @auth.login_required
    @handle_exceptions
    def delete(self, bucket_id, item_id):
        """
        Deletes a bucketlist item.

        Args:
            self, bucket_id, item_id

        Return:
           Delete successfully message
        """
        item = Items.query.get_or_404(item_id)  # get the item by id
        item.delete(item)
        return jsonify({'message': 'Bucketlist item ' + item_id +
                        ' deleted successfully.'})

    @auth.login_required
    @handle_exceptions
    def put(self, bucket_id, item_id):
        """
        Updates bucketlist item.

        Args:
            self, bucket_id, item_id

        Return:
            Updated bucket item for a logged in user
        """
        # bucket id is not specified

        # query for specific item by id
        item = Items.query.get_or_404(item_id)

        # parse incoming request data
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('done')
        args = parser.parse_args()

        # Validate the data or raise a Validation error if incorrect
        items_schema.validate(args)
        item.done = bool(args['done'])
        item.name = args['name']
        item.update()
        return items_schema.dump(item).data, 200


class Register(Resource):
    """
    Handles register requests.

    Resource url:
        '/auth/register'

    Requests Allowed:
        'POST'
    """

    def post(self):
        """
        Register a user.

        Args:
            self

        Returns:
            A 201 status code user created.

        Raises:
            401 error when invalid credentials given
        """

        # parse incoming request data
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')
        args = parser.parse_args()
        username = args['username']
        password = args['password']

        users_schema.validate(args)
        user = User(username)
        user.hash_password(password)
        user.add(user)
        results = items_schema.dump(user).data
        return results, 201


class Login(Resource):
    """
    Handles login requests.

    Resource url:
        '/auth/login'

    Requests Allowed:
        'POST'
    """

    def post(self):
        """
        Login a user.

        Args:
            self

        Returns:
            A token to be used to authenticate requests.

        Raises:
            401 error when invalid credentials given
        """

        # parse incoming request data
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')
        args = parser.parse_args()
        username = args['username']
        password = args['password']

        user = User.query.filter_by(username=username).first()
        if user:
            if user.verify_password(password):
                token = user.generate_auth_token()
            return {"token": token}, 200
        return {"error": "Incorrect Login credentials"}, 400


@auth.verify_password
def verify_password(token, password):
    """
    Verifies if token is valid

    Args:
        token: The token generated
        password: (optional) The users password

    Returns:
        True if user exists and token is valid
        False if user is nonexistent or token is invalid
    """

    token = request.headers.get('token')
    if token is None:
        return False
    # first try to authenticate by token
    user = User.verify_auth_token(token)
    g.user = user
    if not user:
        # try to authenticate with username / password
        user = User.query.filter_by(username=token).first()
        if not user or not user.verify_password(password):
            return False
    return True


# ADD RESOURCES TO API OBJECT
api.add_resource(BucketList, '/bucketlists/',
                 '/bucketlists/<bucket_id>')
api.add_resource(BucketListItem, '/bucketlists/<bucket_id>/items/',
                 '/bucketlists/<bucket_id>/items/<item_id>')
api.add_resource(Register, '/auth/register/')
api.add_resource(Login, '/auth/login/')
