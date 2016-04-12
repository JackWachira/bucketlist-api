from flask import request, jsonify, make_response
from flask_restful import Resource, Api, abort
from models.bucket_models import app, BucketLists, BucketListsSchema, db, Items, ItemsSchema
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

api = Api(app, prefix="/api/v1/")

bucket_list_schema = BucketListsSchema()
items_schema = ItemsSchema()


class BucketList(Resource):

    def get(self, bucket_id=0):
        if bucket_id == 0:
            bucket_list_query = BucketLists.query.all()
            # Serialize the query results in the JSON API format
            results = bucket_list_schema.dump(
                bucket_list_query, many=True).data
        else:
            bucket_list_query = BucketLists.query.get_or_404(bucket_id)
            # Serialize the query results in the JSON API format
            results = bucket_list_schema.dump(
                bucket_list_query, many=False).data

        return results

    def post(self, bucket_id=0):
        raw_dict = request.get_json(force=True)
        try:
           # Validate the data or raise a Validation error if
           # incorrect
            bucket_list_schema.validate(raw_dict)
            # Create a User object with the API data recieved
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


api.add_resource(BucketList, 'bucketlists/', 'bucketlists/<bucket_id>')
api.add_resource(BucketListItem, 'bucketlists/<bucket_id>/items/',
                 'bucketlists/<bucket_id>/items/<item_id>')
