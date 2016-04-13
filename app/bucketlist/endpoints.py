from flask import Blueprint, request, jsonify, make_response
from flask_restful import Resource, Api, abort
from app.bucketlist.models import BucketLists, BucketListsSchema, db, Items, ItemsSchema, UsersSchema, User
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from marshmallow import ValidationError
from flask.ext.httpauth import HTTPBasicAuth
# from flask_httpauth import HTTPTokenAuth
bucket_list = Blueprint('bucketlists', __name__)

api = Api(bucket_list)

bucket_list_schema = BucketListsSchema()
items_schema = ItemsSchema()
users_schema = UsersSchema()

auth = HTTPBasicAuth()


class BucketList(Resource):

    @auth.login_required
    def get(self, bucket_id=0, limit=20, page=1):
        try:
            page = int(request.args.get('page'))
            limit = int(request.args.get('limit'))
        except:
            page = 1
            limit = 20

        if bucket_id == 0:
            # bucket_list_query = BucketLists.query.all()
            record_query = BucketLists.query.paginate(
                page, limit, False)
            # print record_query.items
            # Serialize the query results in the JSON API format
            # results = bucket_list_schema.dump(
            #     bucket_list_query, many=True).data
            results = bucket_list_schema.dump(
                record_query.items, many=True).data
        else:
            bucket_list_query = BucketLists.query.get_or_404(bucket_id)
            # Serialize the query results in the JSON API format
            results = bucket_list_schema.dump(
                bucket_list_query, many=False).data

        return results

    @auth.login_required
    def post(self, bucket_id=0):
        raw_dict = request.get_json(force=True)
        try:
           # Validate the data or raise a Validation error if
           # incorrect
            bucket_list_schema.validate(raw_dict)
            # Create a BucketList object with the API data recieved
            bucketlist = BucketLists(
                raw_dict['name'], raw_dict['created_by'])
            # Commit data
            bucketlist.add(bucketlist)
            query = BucketLists.query.get(bucketlist.id)
            results = bucket_list_schema.dump(query).data
            return results, 201

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 403
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            return resp

    @auth.login_required
    def put(self, bucket_id=0):
        if bucket_id != 0:
            bucketlist = BucketLists.query.get_or_404(bucket_id)
            raw_dict = request.get_json(force=True)
            try:
                bucket_list_schema.validate(raw_dict)
                for key, value in raw_dict.items():
                    setattr(bucketlist, key, value)
                bucketlist.update()
                return bucket_list_schema.dump(bucketlist).data, 201
            except ValidationError as err:
                resp = jsonify({"error": err.messages})
                resp.status_code = 401
                return resp
            except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp
        else:
            resp = jsonify({"error": "Bucket id missing"})
            resp.status_code = 401
            return resp

    @auth.login_required
    def delete(self, bucket_id=0):
        bucket_list = BucketLists.query.get_or_404(bucket_id)
        try:
            bucket_list.delete(bucket_list)
            response = make_response()
            response.status_code = 204
            response.message = "Deleted"
            return response

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp


class BucketListItem(Resource):

    @auth.login_required
    def post(self, bucket_id, item_id=0):
        raw_dict = request.get_json(force=True)
        print raw_dict
        try:
           # Validate the data or raise a Validation error if
           # incorrect
            items_schema.validate(raw_dict)
            # Create a User object with the API data recieved
            print raw_dict['done']
            bucket_items = Items(
                raw_dict['name'], raw_dict['done'], bucket_id)
            # Commit data
            bucket_items.add(bucket_items)
            query = Items.query.get(bucket_items.id)
            results = items_schema.dump(query).data
            return results, 201

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 403
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            return resp

    @auth.login_required
    def delete(self, bucket_id, item_id):
        item = Items.query.get_or_404(item_id)
        try:
            item.delete(item)
            response = make_response()
            response.status_code = 204
            response.message = "Deleted"
            return response

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp

    @auth.login_required
    def put(self, bucket_id, item_id):
        if bucket_id != 0:
            item = Items.query.get_or_404(item_id)
            raw_dict = request.get_json(force=True)
            try:
                items_schema.validate(raw_dict)
                for key, value in raw_dict.items():
                    setattr(item, key, value)
                item.update()
                return items_schema.dump(item).data, 201
            except ValidationError as err:
                resp = jsonify({"error": err.messages})
                resp.status_code = 401
                return resp
            except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp
        else:
            resp = jsonify({"error": "Item id missing"})
            resp.status_code = 401
            return resp


class Register(Resource):

    def post(self):
        raw_dict = request.get_json(force=True)
        try:
            users_schema.validate(raw_dict)
            user = User(username=raw_dict['username'])
            user.hash_password(raw_dict['password'])
            user.add(user)
            query = User.query.get(user.id)
            print query
            results = items_schema.dump(query).data
            return results, 201
        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 403
            return resp
        except IntegrityError as e:
            resp = jsonify({"error": "The username is already taken"})
            resp.status_code = 403
            return resp
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            return resp


class Login(Resource):

    def post(self):
        raw_dict = request.get_json(force=True)
        try:
            # users_schema.validate(raw_dict)
            # user = User(username=raw_dict['username'])
            user = User.query.filter_by(username=raw_dict['username']).first()
            if user.verify_password(raw_dict['password']):
                token = user.generate_auth_token()

            # user.add(user)
            # query = User.query.get_or_404(user.id)
            # print query
            # results = items_schema.dump(query).data
            return token, 201
        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 403
            return resp
        except IntegrityError as e:
            resp = jsonify({"error": "The username is already taken"})
            resp.status_code = 403
            return resp
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            return resp


@auth.verify_password
def verify_password(token, password):
    token = request.headers.get('token')
    if token is None:
        return False
    # first try to authenticate by token
    user = User.verify_auth_token(token)
    print user
    if not user:
        # try to authenticate with username / password
        user = User.query.filter_by(username=token).first()
        if not user or not user.verify_password(password):
            return False
    return True


# def authenticate(func):
#     @auth.verify_token
#     def verify_token(token):
#         return True
#     return verify_token


class Stuff(Resource):

    @auth.login_required
    def post(self):
        return "haha"


# api.add_resource(BucketList, 'bucketlists/', 'bucketlists/<bucket_id>')
# api.add_resource(BucketListItem, 'bucketlists/<bucket_id>/items/',
#                  'bucketlists/<bucket_id>/items/<item_id>')
api.add_resource(BucketList, '/bucketlists/',
                 '/bucketlists/<bucket_id>')
api.add_resource(BucketListItem, '/bucketlists/<bucket_id>/items/',
                 '/bucketlists/<bucket_id>/items/<item_id>')
api.add_resource(Register, '/auth/register/')
api.add_resource(Login, '/auth/login/')
api.add_resource(Stuff, '/auth/stuff/')
